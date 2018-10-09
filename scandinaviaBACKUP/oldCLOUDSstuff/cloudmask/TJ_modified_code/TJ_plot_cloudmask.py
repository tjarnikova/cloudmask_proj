from __future__ import division
import h5py
import glob
from matplotlib import pyplot as plt
import site
site.addsitedir('../src')
from reproject import reproj_L1B
from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
from mpl_toolkits.basemap import Basemap
import bitmap

def make_plot(lcc_values):
    """
      set up the basic map projection details with coastlines and meridians
      return the projection object for further plotting
    """
    proj = Basemap(**lcc_values)
    parallels = np.arange(-90, 90, 1)
    meridians = np.arange(0, 360, 2)
    proj.drawparallels(parallels, labels=[1, 0, 0, 0],
                       fontsize=10, latmax=90)
    proj.drawmeridians(meridians, labels=[0, 0, 0, 1],
                       fontsize=10, latmax=90)
    # draw coast & fill continents
    # map.fillcontinents(color=[0.25, 0.25, 0.25], lake_color=None) # coral
    proj.drawcoastlines(linewidth=3., linestyle='solid', color='r')
    return proj


def find_corners(lons, lats):
    """
      guess values for the upper right and lower left corners of the
      lat/lon grid and the grid center based on max/min lat lon in the
      data and return a dictionary that can be passed to Basemap to set
      the lcc projection.  Also return the smallest lat and lon differences
      to get a feeling for the image resolution
    """
    min_lat, min_lon = np.min(lats), np.min(lons)
    max_lat, max_lon = np.max(lats), np.max(lons)
    llcrnrlon, llcrnrlat = min_lon, min_lat
    urcrnrlon, urcrnrlat = max_lon, max_lat
    print(min_lat, max_lat, min_lon, max_lon)
    lon_res=np.min(np.abs(np.diff(lons.flat)))
    lat_res=np.min(np.abs(np.diff(lats.flat)))
    out=dict(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
             urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
             lat_1=llcrnrlat,lat_2=urcrnrlat,lat_0=(llcrnrlat+urcrnrlat)/2.,
             lon_0=(llcrnrlon + urcrnrlon)/2.)
    return(out,lon_res,lat_res)


l1b_file,=glob.glob('./data/scandinavia/MYD021*h5')
geom_file,=glob.glob('./data/scandinavia/MYD03*h5')
with h5py.File(geom_file) as geom_file,h5py.File(l1b_file) as l1b_file:

  the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
  the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]


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



    

lim= 500
the_slice=slice(0,lim)
small_lons=the_lon[the_slice,:]
small_lats=the_lat[the_slice,:]
chan31_small=chan31[the_slice,:]
chan1_small=chan1[the_slice,:]
chan28_small=chan28[the_slice,:]
chan29_small=chan29[the_slice,:]
#cloud_mask,=glob.glob('cloud_mask.h5')

#with h5py.File(cloud_mask) as cm_h5:
#     maskout=cm_h5['cloudmask'][the_slice,:]
#     landout=cm_h5['landmask'][the_slice,:]

lcc_values,lon_res,lat_res=find_corners(small_lons,small_lats)
lcc_values['fix_aspect']=True
lcc_values['lat_0']=49.5
lcc_values['lat_1']=49.
lcc_values['lat_2']=50.
lcc_values['llcrnrlat']=40.
lcc_values['urcrnrlat']=55.
lcc_values['llcrnrlon']= -25.
lcc_values['urcrnrlon']= 15.
## lcc_values['width']=500.e3
## lcc_values['height']=200.e3
lcc_values['resolution']='h'
lcc_values['projection']='lcc'

#
#pixels with map projection
#

plt.close('all')

missing_val=-999.
latlim=[43.,52.]
lonlim=[-21.,11.]
res=0.02
chan31_grid, longrid, latgrid, bin_count = reproj_L1B(chan31_small, small_lons, small_lats, lonlim, latlim, res)
chan1_grid, longrid, latgrid, bin_count = reproj_L1B(chan1_small, small_lons, small_lats, lonlim, latlim, res)
chan28_grid, longrid, latgrid, bin_count = reproj_L1B(chan28_small, small_lons, small_lats, lonlim, latlim, res)
chan29_grid, longrid, latgrid, bin_count = reproj_L1B(chan29_small, small_lons, small_lats, lonlim, latlim, res)
#mask_grid, longrid, latgrid, bin_count = reproj_L1B(maskout, small_lons, small_lats, lonlim, latlim, res)
# land_grid, longrid, latgrid, bin_count = reproj_L1B(landout, small_lons, small_lats, lonlim, latlim, res)


vmin= 0.
vmax= 10.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
fig,ax=plt.subplots(1,1,figsize=(12,12))
ax.pcolormesh(small_lons)
ax.pcolormesh(small_lats)

cmap=cm.YlGn  #see http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
cmap.set_over('r')
cmap.set_under('0.5')
cmap.set_bad('0.75') #75% grey



the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
fig,ax=plt.subplots(1,1,figsize=(12,12))

#
# tell Basemap what axis to plot into
#
lcc_values['ax']=ax
proj=make_plot(lcc_values)
x,y=proj(longrid,latgrid)
CS=proj.ax.pcolormesh(x,y,chan31_grid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('Channel 31 radiance (W/m^2/micron/sr')
proj.ax.set_title('Channel 31 radiance')
proj.ax.figure.canvas.draw()
fig.savefig('chan31.png')

# fig,ax=plt.subplots(1,1,figsize=(12,12))

# #
# # tell Basemap what axis to plot into
# #
# lcc_values['ax']=ax
# proj=make_plot(lcc_values)
# x,y=proj(longrid,latgrid)
# CS=proj.ax.pcolormesh(x,y,chan29_grid,cmap=cmap,norm=the_norm)
# CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
# CBar.set_label('Channel 29 radiance (W/m^2/micron/sr')
# proj.ax.set_title('Channel 29 radiance')
# proj.ax.figure.canvas.draw()
# fig.savefig('chan29.png')

# fig,ax=plt.subplots(1,1,figsize=(12,12))


# # tell Basemap what axis to plot into
# #
# lcc_values['ax']=ax
# proj=make_plot(lcc_values)
# x,y=proj(longrid,latgrid)
# CS=proj.ax.pcolormesh(x,y,chan28_grid,cmap=cmap,norm=the_norm)
# CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
# CBar.set_label('Channel 28 radiance (W/m^2/micron/sr')
# proj.ax.set_title('Channel 28 radiance')
# proj.ax.figure.canvas.draw()
# fig.savefig('chan28.png')

# fig,ax=plt.subplots(1,1,figsize=(12,12))

# #
# # tell Basemap what axis to plot into
# #
# vmin= 0.
# vmax= 1.
# the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
# lcc_values['ax']=ax
# proj=make_plot(lcc_values)
# x,y=proj(longrid,latgrid)
# CS=proj.ax.pcolormesh(x,y,chan1_grid,cmap=cmap,norm=the_norm)
# CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
# CBar.set_label('Channel 1 reflectance')
# proj.ax.set_title('Channel 1 reflectance')
# proj.ax.figure.canvas.draw()
# fig.savefig('chan1.png')

# fig,ax=plt.subplots(1,1,figsize=(12,12))
# #
# # tell Basemap what axis to plot into
# #
# vmin= 0.
# vmax= 3.
# the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
# lcc_values['ax']=ax
# proj=make_plot(lcc_values)
# CS=proj.ax.pcolormesh(x,y,mask_grid,cmap=cmap,norm=the_norm)
# CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
# CBar.set_label('cloud mask')
# proj.ax.set_title('cloud mask')
# proj.ax.figure.canvas.draw()
# fig.savefig('cloudmask.png')

# fig,ax=plt.subplots(1,1,figsize=(12,12))
# #
# # tell Basemap what axis to plot into
# #
# vmin= 0.
# vmax= 3.
# the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
# lcc_values['ax']=ax
# proj=make_plot(lcc_values)
# CS=proj.ax.pcolormesh(x,y,land_grid,cmap=cmap,norm=the_norm)
# CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
# CBar.set_label('land mask')
# proj.ax.set_title('land mask')
# proj.ax.figure.canvas.draw()
# fig.savefig('landmask.png')

plt.show()