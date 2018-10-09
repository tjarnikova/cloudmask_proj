from __future__ import division,print_function
import glob
import h5py
from hist2d import hist2d , numba_hist2d
import numpy as np
import numpy.ma as ma
import numba
import os

import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt

from timeit import timeit


plotdir='{}/{}'.format(os.getcwd(),'plots')
if not os.path.exists(plotdir):
    os.makedirs(plotdir)

l1b_file,=glob.glob('./data/scandinavia/MYD021*h5')

with h5py.File(l1b_file) as l1b_file:
  index1=0  #channel 1 is first 250 meter reflective channel
  reflective=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'][0,:,:]
  scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'].attrs['reflectance_scales']
  offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'].attrs['reflectance_offsets']
  chan1=(reflective - offset[0])*scale[0]
 


#channel22 is emissive channel 2 
  index22=2
  chan22=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index22,:,:] 
  scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index22]
  offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index22] 
  chan22=(chan22 - offset)*scale
   

#channel27 is emissive channel 6 
  index27=6
  chan27=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index27,:,:] 
  scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index27]
  offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index27] 
  chan27=(chan27 - offset)*scale

#channel28 is emissive channel 7 
  index28=7
  chan28=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index28,:,:] 
  scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index28]
  offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index28] 
  chan28=(chan28 - offset)*scale

    #channel29 is emissive channel 8 
  index29=8
  chan29=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index29,:,:]
  scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index29]
  offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index29]
  chan29=(chan29 - offset)*scale


   
      #channel31 is emissive channel 10
  index31=10
  chan31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
  scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
  offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
  chan31=(chan31 - offset)*scale

      #channel32 is emissive channel 11
  index32=11
  chan32=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index32,:,:]
  scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index32]
  offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index32]
  chan32=(chan32 - offset)*scale

     #channel35 is emissive channel 14
  index35=14
  chan35=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index35,:,:]
  scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index35]
  offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index35]
  chan35=(chan35 - offset)*scale

chan1_min,chan31_min=np.amin(chan1),np.amin(chan31)
chan1_max,chan31_max=np.amax(chan1),np.amax(chan31)

chan1_edges=np.linspace(0,1,30)
chan22_edges=np.linspace(0,10,40)
chan27_edges=np.linspace(0,10,40)

chan31_edges=np.linspace(0,10,40)
chan28_edges=np.linspace(0,10,40)
chan29_edges=np.linspace(0,10,40)

chan32_edges=np.linspace(0,10,40)
chan35_edges=np.linspace(0,10,40)

hist_array,chan1_centers,chan31_centers=numba_hist2d(chan1,chan31,chan1_edges,chan31_edges)
#hist_arraybit17,chan22_centers,chan33_centers=numba_hist2d(chan22,chan33,chan22_edges,chan33_edges)
hist_arraybit18,chan31_centers,chan32_centers=hist2d(chan31,chan32,chan31_edges,chan32_edges)
hist_arraybit19,chan31_centers,chan22_centers=hist2d(chan31,chan22,chan31_edges,chan22_edges)
hist_arraybit24,chan29_centers,chan31_centers=hist2d(chan29,chan31,chan29_edges,chan31_edges)

# hist_array,chan1_centers,chan31_centers=numba_hist2d(chan1,chan31,chan1_edges,chan31_edges)

# for i in range(3):
#     print('\npython iteration #{}'.format(i))
#     with timeit('call hist2d -- plain python'):
#         hist_array,chan1_centers,chan31_centers=hist2d(chan1,chan31,chan1_edges,chan31_edges)

# for i in range(3):
#     print('\nnumba iteration #{}'.format(i))
#     with timeit('call hist2d -- numba'):
#         hist_array,chan1_centers,chan31_centers=numba_hist2d(chan1,chan31,chan1_edges,chan31_edges)

# hist_array=ma.array(hist_array,mask=np.isnan(hist_array))

cmap=cm.RdBu_r
cmap.set_over('y')
cmap.set_under('w')
cmap.set_bad('0.75') #75% grey
vmin= 0.
vmax= 100000.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)

fig=plt.figure(2)
fig.clf()
ax=fig.add_subplot(111)
im=ax.pcolormesh(chan1_centers,chan31_centers,hist_array,cmap=cmap,norm=the_norm)
cb=fig.colorbar(im,extend='both')
ax.set_title('2d histogram B')
fig.canvas.draw()
figpath='{}/{}'.format(plotdir,'kin.png')
fig.savefig(figpath)

#hist_array,chan1_centers,chan31_centers=hist2d(chan1,chan31,chan1_edges,chan31_edges)
# cmap=cm.RdBu_r
# cmap.set_over('y')
# cmap.set_under('w')
# cmap.set_bad('0.75') #75% grey
# vmin= 0.
# vmax= 100000.
# the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)

# fig=plt.figure(2)
# fig.clf()
# ax=fig.add_subplot(111)
# im=ax.pcolormesh(chan1_centers,chan31_centers,hist_array,cmap=cmap,norm=the_norm)
# cb=fig.colorbar(im,extend='both')
# ax.set_title('2d histogram B')
# fig.canvas.draw()
# figpath='{}/{}'.format(plotdir,'Ch1Ch31.png')
# fig.savefig(figpath)


#hist_arraybit24,chan29_centers,chan31_centers=hist2d(chan29,chan31,chan29_edges,chan31_edges)
cmap=cm.RdBu_r
cmap.set_over('y')
cmap.set_under('w')
cmap.set_bad('0.75') #75% grey
vmin= 0.
vmax= 100000.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)

fig=plt.figure(2)
fig.clf()
ax=fig.add_subplot(111)
im=ax.pcolormesh(chan29_centers,chan31_centers,hist_arraybit24,cmap=cmap,norm=the_norm)
cb=fig.colorbar(im,extend='both')
ax.set_title('bit 24')
fig.canvas.draw()
figpath='{}/{}'.format(plotdir,'Ch29Ch31.png')
fig.savefig(figpath)


# bit 18
cmap=cm.RdBu_r
cmap.set_over('y')
cmap.set_under('w')
cmap.set_bad('0.75') #75% grey
vmin= 0.
vmax= 100000.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)

fig=plt.figure(2)
fig.clf()
ax=fig.add_subplot(111)
im=ax.pcolormesh(chan31_centers,chan32_centers,hist_arraybit18,cmap=cmap,norm=the_norm)
cb=fig.colorbar(im,extend='both')
ax.set_title('bit 18')
fig.canvas.draw()
figpath='{}/{}'.format(plotdir,'bit 18.png')
fig.savefig(figpath)

#bit19
cmap=cm.RdBu_r
cmap.set_over('y')
cmap.set_under('w')
cmap.set_bad('0.75') #75% grey
vmin= 0.
vmax= 100000.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)

fig=plt.figure(2)
fig.clf()
ax=fig.add_subplot(111)
im=ax.pcolormesh(chan31_centers,chan22_centers,hist_arraybit19,cmap=cmap,norm=the_norm)
cb=fig.colorbar(im,extend='both')
ax.set_title('bit 19')
fig.canvas.draw()
figpath='{}/{}'.format(plotdir,'bit 19.png')
fig.savefig(figpath)







#this is the log histogram

# vmin= 0.
# vmax= 6.
# the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
# log_hist_array=np.log10(hist_array)
# fig=plt.figure(3)
# fig.clf()
# ax=fig.add_subplot(111)
# im=ax.pcolormesh(chan1_centers,chan31_centers,log_hist_array,cmap=cmap,norm=the_norm)
# cb=fig.colorbar(im,extend='both')
# ax.set_title('2d histogram C')
# fig.canvas.draw()
# figpath='{}/{}'.format(plotdir,'histogram2.png')
# fig.savefig(figpath)


plt.show()
