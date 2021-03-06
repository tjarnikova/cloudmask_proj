from __future__ import print_function,division
import h5py
import numpy as np
import pandas as pd
import glob,os
import numpy.ma as ma
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
from matplotlib.colors import Normalize
import site
site.addsitedir('fortran/lib')
try:
    import petty
    from petty_python import absorb_fortran as absorb
    from petty_python import emiss_fortran as emiss
except ImportError:
    print("can't import fortran module, falling back to python versions")
    from petty_python import absorb
    from petty_python import emiss
from petty_python import wind_speed


def linear_solve(kl19,kv19,kl37,kv37,R1,R2):
    A=[[kl19,kv19],[kl37,kv37]]
    b=[R1,R2]
    return np.linalg.solve(A,b)
    
if __name__ == "__main__":

    correct = False
    output='correct.h5'
    plotdir='{}/{}'.format(os.getcwd(),'plots')
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)

    
    micro_file='./micro_coeffs.h5'
    micro_file=os.path.abspath(micro_file)
    print(micro_file)
    with h5py.File(micro_file,'r') as micro_h5:
        print('here are the top level datasets: ')
        for name,value in micro_h5.items():
            print(' '*8,name)
        #
        # read in the fields
        #
        micro_winds=micro_h5['windspeed'][...]
        micro_ssts=micro_h5['temperature'][...]
        micro_freqs=micro_h5['freq'][...]
        emissv=micro_h5['emissv'][...]
        emissh=micro_h5['emissh'][...]
        
    with pd.HDFStore(micro_file,'r') as df:
        abs_coeffs=df['/abs_coeffs']
        print('df: info:',df)

    #
    # put the data in a dummy class to make it easier to pass around
    #
    class data_holder:
        pass

    data=data_holder()
    data.micro_winds=micro_winds
    data.micro_ssts=micro_ssts
    data.micro_freqs=micro_freqs
    data.emissv=emissv
    data.emissh=emissh
    data.abs_coeffs=abs_coeffs

    #
    # read in the data from micro_coeffs.h5, which was produced by
    # interp_petty.py, and bright_temps.h5, produced by write_data.py
    #

    
    the_temps=dict()
    months=['jan','july']
    for the_month in months:
        the_temps[the_month]=dict()
    fields=['sst','t19h','t19v','t19v','t22v','t37h','t37v']
    bright_file='bright_temps.h5'
    with h5py.File(bright_file) as bright_h5:
        for key in ['lat','lon']:
            the_temps[key]=bright_h5[key][...]
        for the_month in months:
            for the_field in fields:
                the_temps[the_month][the_field]=bright_h5[the_month][the_field][...]
    out_dict={}
    for the_month in ['july','jan']:
        print('gridding {}'.format(the_month))
        sst=the_temps[the_month]['sst'][...]
        t19h=the_temps[the_month]['t19h'][...]
        t19v=the_temps[the_month]['t19v'][...]
        t22v=the_temps[the_month]['t22v'][...]
        t37h=the_temps[the_month]['t37h'][...] + 3.58  #correction for cold bias (Greenwald et al., 1993)
        t37v=the_temps[the_month]['t37v'][...] + 3.58
        wv=np.empty_like(sst)
        wl=np.empty_like(wv)
        nrows,ncols=sst.shape
        mu=np.cos(53.1*np.pi/180.)
        for row in range(nrows):
            for col in range(ncols):
                sstx=sst[row,col]
                if sstx < 400.:
                    abs_dict=absorb(sst[row,col],data)
                    t19hx=t19h[row,col]
                    t19vx=t19v[row,col]
                    t22vx=t22v[row,col]
                    t37hx=t37h[row,col]
                    t37vx=t37v[row,col]
                    args=[sstx,t19vx,t22vx,
                          t37hx - 3.58,t37vx - 3.58] #remove cold bias correction from Goodberlet et al., 1989 regression
                    windspeed=wind_speed(*args)
                    emiss_dict=emiss(sstx,windspeed,data)
                    emiss19h,emiss19v=emiss_dict[19]
                    emiss37h,emiss37v=emiss_dict[37]
                    r37v=(1.0 - emiss37v)
                    r19v=(1.0 - emiss19v)
                    r37h=(1.0 - emiss37h)
                    r19h=(1.0 - emiss19h)
                    Trox19=abs_dict['tox19']
                    Trox37=abs_dict['tox37']
                    DeltaTb19 = t19hx - t19vx
                    DeltaTb37 = t37hx - t37vx
                    F19 = (t19hx - sstx )/(t19vx - sstx)
                    F37 = (t37hx - sstx)/(t37vx - sstx)
                    term19=r19v*(1. - F19)
                    term37=r37v*(1. - F37)
                    kl37,kv37=(abs_dict['kl37'],abs_dict['kv37'])
                    kl19,kv19=(abs_dict['kl19'],abs_dict['kv19'])
                    R1= -mu/2.*np.log(DeltaTb19/(sstx*(r19v-r19h)*Trox19**2.))
                    R2= -mu/2.*np.log(DeltaTb37/(sstx*(r37v-r37h)*Trox37**2.))
                    wlx,wvx=linear_solve(kl19,kv19,kl37,kv37,R1,R2)
                    #if wvx < 25. or not correct:
                    wv[row,col]=wvx
                    wl[row,col]=wlx
                #     else:
                #         gamma= -5.8  # K/km
                #         H=2.2  #km
                #         f=np.exp(50*kv19/mu)
                #         Trw19_2=np.exp(-2.*kv19*wvx/mu)
                #         Tbar=sstx + gamma*H*(1. - f*Trw19_2)*Trox19
                #         F19 = (t19hx - Tbar )/(t19vx - Tbar)
                #         term19=r19v*(1. - F19)
                #         R1= -mu/2.*np.log(DeltaTb19/(sstx*term19*Trox19**2.))
                #         R2= -mu/2.*np.log(DeltaTb37/(sstx*term37*Trox37**2.))
                #         wlx,wvx=linear_solve(kl19,kv19,kl37,kv37,R1,R2)
                #         wv[row,col]=wvx
                #         wl[row,col]=wlx
                # else:
                #     wv[row,col]=np.nan
                #     wl[row,col]=np.nan
        out_dict[the_month]=dict(wv=wv,wl=wl)

    with h5py.File(output,'w') as f:
        group=f.create_group('latlon')
        for key in ['lat','lon']:
            field=the_temps[key]
            dset=group.create_dataset(key,field.shape,dtype=field.dtype)
            dset[...]=field[...]

        for month in out_dict.keys():
            group=f.create_group(month)
            for name,field in out_dict[month].items():
                dset=group.create_dataset(name,field.shape,dtype=field.dtype)
                dset[...]=field[...]
        f.attrs['history']='written by full retrieve.py tag noiter with correc={}'.format(correct)
        f.attrs['correct_flag']=correct
        

    
        
