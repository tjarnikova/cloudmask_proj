import h5py
import glob
import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt
import site
site.addsitedir('../../src')
from TJ_reproject import reproj_L1B
from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
from mpl_toolkits.basemap import Basemap

l1b_file,=glob.glob('MYD021KM.A2014125.2135.006.2014125183330.h5')
l1b_file=h5py.File(l1b_file)
geom_file,=glob.glob('MYD03*h5')
geom_file=h5py.File(geom_file)
#channel31 is emissive channel 10
index31=10
chan31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
chan31=(chan31 - offset)*scale
index1=0  #channel 1 is first 250 meter reflective channel
reflective=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'][0,:,:]
scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'].attrs['reflectance_scales']
offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'].attrs['reflectance_offsets']
chan1=(reflective - offset[0])*scale[0]
the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]

lim= 500
the_slice=slice(0,lim)
small_lons=the_lon[the_slice]
small_lats=the_lat[the_slice]
chan31_small=chan31[the_slice] #goes from 0-10
chan1_small=chan1[the_slice] #goes from 0-1



r = (small_lats.shape[0])
c = (small_lats.shape[1])

chan31_filt = np.empty((r,c))
chan1_filt = np.empty((r,c))
chan31_filt[:] = np.NAN
chan1_filt[:] = np.NaN
filtcount = 0 

for i in range(0, r):
    for j in range(0, c):
        thislat = small_lats[i,j]
        thislon = small_lons[i,j]
        thischan31 = chan31_small[i,j]
        thischan1 = chan1_small[i,j]
        if thislat < 50.01  and thislat > 48.99 and thislon < -120.99 and thislon > -124.01:
 
            chan31_filt[i,j] = thischan31
            chan1_filt[i,j] = thischan1
            filtcount = filtcount + 1



print filtcount

chan31_rescale = chan31_filt/10


xlim = [0,1]
ylim = [0,1]

# x_array, y_array, bin_count = reproj_L1B(raw_x, raw_y, xlim, ylim, res)
#ch31reproj, ch1reproj, bin_count
ch31reproj, ch1reproj, bin_count = reproj_L1B(chan31_rescale, chan1_filt, xlim, ylim, .1)


rows = (ch1reproj.shape[0])
cols= (ch1reproj.shape[1])
w =bin_count[5,5]
print w
points = rows*cols
stormat = np.empty((points,4))
stormat[:] = np.NAN

w = np.amax(bin_count)
print('*')
print w
plt.subplot(1, 1, 1)
# plt.pcolor(xlim, ylim, bin_count, cmap='RdBu', vmin=z_min, vmax=z_max)
# plt.title('pcolor')
# # set the limits of the plot to the limits of the data
# plt.axis([x.min(), x.max(), y.min(), y.max()])
# plt.colorbar()




# print(stormat[5000,1])
rows = (ch1reproj.shape[0])
cols= (ch1reproj.shape[1])
count = 0
#stormat 0th col is ch31, 1st col is ch 1, 2nd is bins

for i in range(0,rows):
  for j in range(0,cols):
      stormat[count,0] = ch31reproj[i,j]
      stormat[count,1] = ch1reproj[i,j]
      stormat[count,2] = bin_count[i,j]
      if ch1reproj[i,j] > 0:
        stormat[count,3] = ch31reproj[i,j]/(ch1reproj[i,j])
      
      count = count+1

fig = plt.figure()


ax1 = fig.add_subplot(2,1,1, axisbg='w')
ax1.plot(stormat[:,0],stormat[:,1], 'bo')
ax1.tick_params(axis='xlim', colors='k')
ax1.tick_params(axis='ylim', colors='k')
ax1.spines['bottom'].set_color('k')
ax1.spines['top'].set_color('k')
ax1.spines['left'].set_color('k')
ax1.spines['right'].set_color('k')
ax1.yaxis.label.set_color('k')
ax1.xaxis.label.set_color('k')
ax1.set_title('Ch31 vs Ch1', color = 'k')
ax1.set_xlabel('ch 31 / 10 ')
ax1.set_ylabel('ch 1')

ax2 = fig.add_subplot(2,1,2, axisbg='w')
ax2.plot(stormat[:,3],stormat[:,2], 'ro')
# ax2.tick_params(axis='x', colors='k')
# ax2.tick_params(axis='y', colors='k')
ax2.spines['bottom'].set_color('k')
ax2.spines['top'].set_color('k')
ax2.spines['left'].set_color('k')
ax2.spines['right'].set_color('k')
ax2.yaxis.label.set_color('k')
ax2.xaxis.label.set_color('k')
ax2.set_title('Ch31/Ch1 ratio vs bin number', color = 'k')
ax2.set_xlabel('Ch31/Ch1')
ax2.set_ylabel('no of observations in bin')

plt.show()  





# point=np.searchsorted(ch31flat, 5.85)
# point2=np.searchsorted(ch1flat, 0.29)
# point3=np.searchsorted(ch1flat, 0.495)




#print(ch31flat)
#plt.plot(ch31flat[0], ch1flat[0], 'bo')
#plt.show()

#plt.plot(bin_count[:,0],bin_count[:,1], 'bo')


# plt.plot(stormat[:,2],stormat[:,3], 'bo')
# plt.show()


# #print(small_lons)
# print(small_lats.shape[0])
# print(chan31_small.shape)

# x = small_lats.shape[0]
# y = small_lats.shape[1]

# #loop to find points between 49 and 50 latitude, -121 and -124 longitude, store 
# #their chan31 and chan1

# count = 0
# stormat = np.zeros((15571, 4))

# # for i in range(0, x):
# #     for j in range(0, y):
# #         thislat = small_lats[i,j]
# #         thislon = small_lons[i,j]
# #         thischan31 = chan31_small[i,j]
# #         thischan1 = chan1_small[i,j]
# #         if thislat < 50.01  and thislat > 48.99 and thislon < -120.99 and thislon > -124.01:
# #             stormat[count,0] = thislat
# #             stormat[count,1] = thislon
# #             stormat[count,2] = thischan31
# #             stormat[count,3] = thischan1

# #             count = count +1
# # #for j = size(small_lats.shape[1])
# # #15571 points 

# # print(count)


# # print(stormat[1,:])

# #flat_chan31 = np.ravel(chan31_small)
# #flat_chan1 = np.ravel(chan1_small)
# plt.plot(stormat[:,2],stormat[:,3], 'bo')
# plt.show()