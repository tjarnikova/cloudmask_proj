from __future__ import division
import h5py
import glob
from matplotlib import pyplot as plt
import site
site.addsitedir('../src')
#site.addsitedir('/Users/alena/SYNC/CLOUDS/cloudmask/')
site.addsitedir('./cloudmask/')
from TJ_reproject import reproj_L1B
from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
from mpl_toolkits.basemap import Basemap
import bitmap
print(dir(bitmap))
# import sys
# sys.exit()

#here: set h5 files you want to import
cloud_mask,=glob.glob('./scandinavia/2015064/MYD35*h5')
geom_file,=glob.glob('./scandinavia/2015064/MYD03*h5')
l1b_file,=glob.glob('./scandinavia/2015064/MYD021*h5')

#here: extract interesting data from geom files, L1 files, and cloudmask
with h5py.File(geom_file) as geom_file,h5py.File(l1b_file) as l1b_file, h5py.File(cloud_mask) as cloud_mask_h5:
        #channel31 is emissive channel 10
        index31=10
        chan31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
        scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
        offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
        chan31=(chan31 - offset)*scale
               #channel29 is emissive channel 8
        index29=8
        chan29=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index29,:,:]
        scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index29]
        offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index29]
        chan29=(chan29 - offset)*scale
        the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
        the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]
        #3rd byte, 0th bit
        cloud_mask_bit24=cloud_mask_h5['mod35']['Data Fields']['Cloud_Mask'][3,:,:]
        bit24_flag=bitmap.getbit(cloud_mask_bit24[3,:,:],0)


#get brightness temperatures      
ch31_bright=planckInvert(11.03,chan31)
ch29_bright=planckInvert(8.6,chan29)

#limits of plotting files
lim= None
the_slice=slice(0,lim)
small_lons=the_lon[the_slice,:]
small_lats=the_lat[the_slice,:]
chan31_small=chan31[the_slice,:]
chan29_small=chan29[the_slice,:]
 
lcc_values,lon_res,lat_res=find_corners(small_lons,small_lats)
lcc_values['fix_aspect']=True
lcc_values['resolution']='c'
lcc_values['projection']='lcc'

missing_val=-999.
latlim=[lcc_values['llcrnrlat'],lcc_values['urcrnrlat']]
lonlim=[lcc_values['llcrnrlon'],lcc_values['urcrnrlon']]
res=0.02

#reproject all our files so that we can plot them. 
ch31bright_grid, longrid, latgrid, bin_count = reproj_L1B(ch31_bright, missing_val, small_lons, small_lats, lonlim, latlim, res)
ch29bright_grid, longrid, latgrid, bin_count = reproj_L1B(ch29_bright, missing_val, small_lons, small_lats, lonlim, latlim, res)
bit24_grid, longrid, latgrid, bin_count = reproj_L1B(bit24_flag,missing_val, small_lons, small_lats, lonlim, latlim, res)
#high_grid=ma.array(high_grid,mask=np.isnan(high_grid))
        
cmap=cm.YlGn  #see http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
cmap.set_over('r')
cmap.set_under('0.5')
cmap.set_bad('0.75') #75% grey
vmin= 0.
vmax= 10.

fig,ax=plt.subplots(1,1,figsize=(12,12))
    #
    # tell Basemap what axis to plot into
    #
vmin= 200.
vmax= 300.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
lcc_values['ax']=ax
proj=make_plot(lcc_values)
x,y=proj(longrid,latgrid)
CS=proj.ax.pcolormesh(x,y,bit24_grid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('11 micron brightness temp (K)')
proj.ax.set_title('11 micron brightness temp')
proj.ax.figure.canvas.draw()
fig.savefig('0423_Bit24mask.png')



