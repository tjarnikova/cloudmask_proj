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
    #channel31 is emissive channel 10
        index31=10
        chan31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
        scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
        offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
        chan31=(chan31 - offset)*scale
        #channel22 is emissive channel 2
        index22=11
        chan22=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index22,:,:]
        scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index22]
        offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index22]
        chan22=(chan22 - offset)*scale
        the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
        the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]

ch31_bright=planckInvert(11.03,chan31)
ch22_bright=planckInvert(3.96,chan22)

max22bright = np.nanmax(ch22_bright)
min22bright = np.nanmax(ch22_bright)

lim= None
the_slice=slice(0,lim)
small_lons=the_lon[the_slice,:]
small_lats=the_lat[the_slice,:]
chan31_small=chan31[the_slice,:]
chan22_small=chan22[the_slice,:]

lcc_values,lon_res,lat_res=find_corners(small_lons,small_lats)
lcc_values['fix_aspect']=True
lcc_values['resolution']='c'
lcc_values['projection']='lcc'

plt.close('all')

missing_val=-999.
latlim=[lcc_values['llcrnrlat'],lcc_values['urcrnrlat']]
lonlim=[lcc_values['llcrnrlon'],lcc_values['urcrnrlon']]
res=0.02

ch31bright_grid, longrid, latgrid, bin_count = reproj_L1B(ch31_bright, missing_val, small_lons, small_lats, lonlim, latlim, res)
ch22bright_grid, longrid, latgrid, bin_count = reproj_L1B(ch22_bright, missing_val, small_lons, small_lats, lonlim, latlim, res)

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
CS=proj.ax.pcolormesh(x,y,ch31bright_grid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('11 micron brightness temp (K)')
proj.ax.set_title('11 micron brightness temp')
proj.ax.figure.canvas.draw()
fig.savefig('BIT19_c31_bright.png')

fig,ax=plt.subplots(1,1,figsize=(12,12))
#
# tell Basemap what axis to plot into
#
vmin= min22bright
vmax= max22bright
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
lcc_values['ax']=ax
proj=make_plot(lcc_values)
x,y=proj(longrid,latgrid)
CS=proj.ax.pcolormesh(x,y,ch22bright_grid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('3.9 micron brightness temp (K)')
proj.ax.set_title('3.9 micron brightness temp')
proj.ax.figure.canvas.draw()
fig.savefig('BIT19_c22_bright.png')

diffgrid = ch22bright_grid - ch31bright_grid

fig,ax=plt.subplots(1,1,figsize=(12,12))
#
# tell Basemap what axis to plot into
#
vmin= 0.
vmax= 200.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
lcc_values['ax']=ax
proj=make_plot(lcc_values)
x,y=proj(longrid,latgrid)
CS=proj.ax.pcolormesh(x,y,diffgrid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('diff btwn 11 and 3.9 brightness temp (K)')
proj.ax.set_title('11 and 3.9 micron brightness temp difference')
proj.ax.figure.canvas.draw()
fig.savefig('BIT19_diffbright.png')

plt.show()