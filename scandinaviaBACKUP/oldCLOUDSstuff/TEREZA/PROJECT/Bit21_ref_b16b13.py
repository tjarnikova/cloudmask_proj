from __future__ import division
import argparse
import h5py
import glob
from matplotlib import pyplot as plt
import site
site.addsitedir('../utilities')
from TJ_reproject import reproj_L1B

import planck
reload(planck)
from planck import planckInvert
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
import textwrap

#this code plots reflectivities at 

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
    lon_res=np.min(np.abs(np.diff(lons.flat)))
    lat_res=np.min(np.abs(np.diff(lats.flat)))
    out=dict(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
             urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
             lat_1=llcrnrlat,lat_2=urcrnrlat,lat_0=(llcrnrlat+urcrnrlat)/2.,
             lon_0=(llcrnrlon + urcrnrlon)/2.)
    return(out,lon_res,lat_res)


geom_file,=glob.glob('./scandinavia/2015032/MYD03*h5')
l1b_file,=glob.glob('./scandinavia/2015032/MYD021*h5')

with h5py.File(geom_file) as geom_file,h5py.File(l1b_file) as l1b_file:
	index13=5  #channel 13 is  1000 meter reflective channel 5 R0.65
	reflective=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'][5,:,:]
	scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'].attrs['reflectance_scales']
	offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'].attrs['reflectance_offsets']
	chan13=(reflective - offset[5])*scale[5] #do i need indices here?

	index16=8  #channel 16 is  1000 meter reflective channel 8 R0.86
	reflective=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'][8,:,:]
	scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'].attrs['reflectance_scales']
	offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'].attrs['reflectance_offsets']
	chan16=(reflective - offset[8])*scale[8] #do i need indices here?

	the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
	the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]

lim= None
the_slice=slice(0,lim)
small_lons=the_lon[the_slice,:]
small_lats=the_lat[the_slice,:]
chan16_small=chan16[the_slice,:]
chan13_small=chan13[the_slice,:]
 
lcc_values,lon_res,lat_res=find_corners(small_lons,small_lats)
lcc_values['fix_aspect']=True
lcc_values['resolution']='c'
lcc_values['projection']='lcc'

plt.close('all')

missing_val=-999.
latlim=[lcc_values['llcrnrlat'],lcc_values['urcrnrlat']]
lonlim=[lcc_values['llcrnrlon'],lcc_values['urcrnrlon']]
res=0.02
chan13_grid, longrid, latgrid, bin_count = reproj_L1B(chan13_small,missing_val, small_lons, small_lats, lonlim, latlim, res)
chan16_grid, longrid, latgrid, bin_count = reproj_L1B(chan16_small,missing_val, small_lons, small_lats, lonlim, latlim, res)


cmap=cm.YlGn  #see http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
cmap.set_over('r')
cmap.set_under('0.5')
cmap.set_bad('0.75') #75% grey

fig,ax=plt.subplots(1,1,figsize=(12,12))
#
# tell Basemap what axis to plot into
#
vmin= 0.
vmax= 1.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
lcc_values['ax']=ax
proj=make_plot(lcc_values)
x,y=proj(longrid,latgrid)
CS=proj.ax.pcolormesh(x,y,chan16_grid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('Channel 16 reflectance')
proj.ax.set_title('Channel 16 reflectance')
proj.ax.figure.canvas.draw()
fig.savefig('BIT21_c16ref.png')

fig,ax=plt.subplots(1,1,figsize=(12,12))
#
# tell Basemap what axis to plot into
#
vmin= 0.
vmax= 1.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
lcc_values['ax']=ax
proj=make_plot(lcc_values)
CS=proj.ax.pcolormesh(x,y,chan13_grid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('Channel 13 reflectance')
proj.ax.set_title('Channel 13 reflectance')
proj.ax.figure.canvas.draw()
fig.savefig('BIT21_c13ref.png')

ratiogrid = chan16_grid/chan13_grid
rmin = np.nanmin(ratiogrid)
rmax = np.nanmax(ratiogrid)


fig,ax=plt.subplots(1,1,figsize=(12,12))
#
# tell Basemap what axis to plot into
#
vmin= rmin
vmax= rmax
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
lcc_values['ax']=ax
proj=make_plot(lcc_values)
CS=proj.ax.pcolormesh(x,y,ratiogrid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('r16/r13')
proj.ax.set_title('ratio of 0.87 reflectivity and 0.66 reflectivity')
proj.ax.figure.canvas.draw()
fig.savefig('BIT21_b16b13ratio.png')

plt.show()