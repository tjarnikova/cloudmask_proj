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

l1b_file,=glob.glob('./scandinavia/MYD021*h5')

with h5py.File(l1b_file) as l1b_file:
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

chan29_min,chan31_min=np.amin(chan29),np.amin(chan31)
chan29_max,chan31_max=np.amax(chan29),np.amax(chan31)


chan31_edges=np.linspace(0,10,40)
chan29_edges=np.linspace(0,10,40)

hist_arraybit24,chan29_centers,chan31_centers=hist2d(chan29,chan31,chan29_edges,chan31_edges)

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
