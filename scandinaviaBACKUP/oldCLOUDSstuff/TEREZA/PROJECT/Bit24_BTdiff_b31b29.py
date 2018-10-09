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
mod06_file=glob.glob('./scandinavia/2015032/MYD06*h5')



with h5py.File(geom_file) as geom_file,h5py.File(l1b_file) as l1b_file:
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
      
ch31_bright=planckInvert(11.03,chan31)
ch29_bright=planckInvert(8.6,chan29)

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

with h5py.File(mod06_file) as m06_h5:
      phase=m06_h5['mod06']['Data Fields']['Cloud_Phase_Infrared_1km'][:,:]
      phase=phase.astype(np.int32)

plt.close('all')

missing_val=-999.
latlim=[lcc_values['llcrnrlat'],lcc_values['urcrnrlat']]
lonlim=[lcc_values['llcrnrlon'],lcc_values['urcrnrlon']]
res=0.02

ch31bright_grid, longrid, latgrid, bin_count = reproj_L1B(ch31_bright, missing_val, small_lons, small_lats, lonlim, latlim, res)
ch29bright_grid, longrid, latgrid, bin_count = reproj_L1B(ch29_bright, missing_val, small_lons, small_lats, lonlim, latlim, res)
phase_grid,longrid, latgrid, bin_count = reproj_L1B(phase,missing_val, small_lons, small_lats, lonlim, latlim, res)

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
fig.savefig('0421_BIT24_b31_bright.png')

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
CS=proj.ax.pcolormesh(x,y,ch29bright_grid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('8.6 micron brightness temp (K)')
proj.ax.set_title('8.6 micron brightness temp')
proj.ax.figure.canvas.draw()
fig.savefig('0421_BIT24_b29_bright.png')

diffgrid = ch31bright_grid - ch29bright_grid

fig,ax=plt.subplots(1,1,figsize=(12,12))
    #
    # tell Basemap what axis to plot into
    #
vmin= -4.
vmax= 4.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
lcc_values['ax']=ax
proj=make_plot(lcc_values)
x,y=proj(longrid,latgrid)
CS=proj.ax.pcolormesh(x,y,diffgrid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('diff btwn 11 and 8.6 micron brightness temp (K)')
proj.ax.set_title('11 and 8.6 brightness temp difference')
proj.ax.figure.canvas.draw()
fig.savefig('0421_BIT24_diffbright.png')

fig,ax=plt.subplots(1,1,figsize=(12,12))
vmin= 0.
vmax= 6.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
cmap=cm.YlGn
cmap.set_over('r')
cmap.set_under('0.5')
cmap.set_bad('0.75') #75% grey
lcc_values['ax']=ax
proj=make_plot(lcc_values)
phase_grid=ma.array(phase_grid,mask=np.isnan(phase_grid))
CS=proj.ax.pcolormesh(x,y,phase_grid,cmap=cmap,norm=the_norm)
CBar=proj.colorbar(CS, 'right', size='5%', pad='5%',extend='both')
CBar.set_label('phase 0-6')
proj.ax.set_title('0 -- cloud free,1 -- water cloud,2 -- ice cloud,3 -- mixed phase cloud,6 -- undetermined phase')
proj.ax.figure.canvas.draw()
fig.savefig('{}/phase.png'.format(plot_dir))

plt.show()