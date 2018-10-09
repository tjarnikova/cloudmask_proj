from __future__ import division
import h5py
import glob
from matplotlib import pyplot as plt
import site
site.addsitedir('../src')
site.addsitedir('/Users/alena/SYNC/CLOUDS/cloudmask/')
site.addsitedir('/Users/alena/SYNC/CLOUDS/utilities/')
#site.addsitedir('./cloudmask/')
from TJ_reproject import reproj_L1B
import planck
reload(planck)
from planck import planckInvert
from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
from mpl_toolkits.basemap import Basemap
import bitmap
print(dir(bitmap))
print((bitmap))
# import sys
# sys.exit()
import time
import os.path

def bit18extract(cloud_mask,l1b_file):
    with h5py.File(l1b_file) as l1b_file, h5py.File(cloud_mask) as cloud_mask_h5:
        #bandnel31 is emissive bandnel 10
        index31=10
            band31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
            scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
            offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
            band31=(band31 - offset)*scale
            #bandnel32 is emissive bandnel 11
            index32=11
            band32=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index32,:,:]
            scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index29]
            offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index29]
            band32=(band32 - offset)*scale
            #getting appropriate bits from cloudmask
            cloud_mask_all=cloud_mask_h5['mod35']['Data Fields']['Cloud_Mask'][...]
            bit18_flag=bitmap.getbit(cloud_mask_all[2,:,:],2)
            ch31_bright=planckInvert(11.03,band31)
            ch32_bright=planckInvert(12.02,band32)

return band31, band32, ch31_bright, ch32_bright, bit18_flag

def bit19extract(cloud_mask,l1b_file):
    with h5py.File(l1b_file) as l1b_file, h5py.File(cloud_mask) as cloud_mask_h5:
        #bandnel31 is emissive bandnel 10
        index31=10
            band31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
            scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
            offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
            band31=(band31 - offset)*scale
            #bandnel22 is emissive bandnel 2
            index22=2
            band22=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index22,:,:]
            scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index29]
            offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index29]
            band22=(band22 - offset)*scale
            #getting appropriate bits from cloudmask
            cloud_mask_all=cloud_mask_h5['mod35']['Data Fields']['Cloud_Mask'][...]
            bit19_flag=bitmap.getbit(cloud_mask_all[2,:,:],3)
            ch31_bright=planckInvert(11.03,band31)
            ch22_bright=planckInvert(3.95,band22)

return band31, band32, ch31_bright, ch32_bright, bit19_flag

def bit21extract(cloud_mask,l1b_file):
    with h5py.File(l1b_file) as l1b_file, h5py.File(cloud_mask) as cloud_mask_h5:
        #band 16 is emissive bandnel 5
        index31=5
            band16=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'][index31,:,:]
            scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'].attrs['radiance_scales'][index31]
            offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_RefSB'].attrs['radiance_offsets'][index31]
            band31=(band31 - offset)*scale
            #bandnel22 is emissive bandnel 2
            index22=2
            band22=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index22,:,:]
            scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index29]
            offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index29]
            band22=(band22 - offset)*scale
            #getting appropriate bits from cloudmask
            cloud_mask_all=cloud_mask_h5['mod35']['Data Fields']['Cloud_Mask'][...]
            bit19_flag=bitmap.getbit(cloud_mask_all[2,:,:],3)
            ch31_bright=planckInvert(11.03,band31)
            ch22_bright=planckInvert(3.95,band22)

return band31, band32, ch31_bright, ch32_bright, bit19_flag

def bit24extract(cloud_mask,geom_file,l1b_file):
    with h5py.File(geom_file) as geom_file,h5py.File(l1b_file) as l1b_file, h5py.File(cloud_mask) as cloud_mask_h5:
        #band 31 is emissive bandnel 10
        index31=10
            band31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
                scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
                offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
                band31=(band31 - offset)*scale
                #band 29 is emissive bandnel 8
                index29=8
                band29=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index29,:,:]
                scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index29]
                offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index29]
                band29=(band29 - offset)*scale
                #getting appropriate bits from cloudmask
                cloud_mask_all=cloud_mask_h5['mod35']['Data Fields']['Cloud_Mask'][...]
                bit24_flag=bitmap.getbit(cloud_mask_all[3,:,:],0)
                ch31_bright=planckInvert(11.03,band31)
                ch29_bright=planckInvert(8.6,band29)
    
    return band29, band31, ch31_bright, ch29_bright, bit24_flag


def lonlatextract(geom_file):
    with h5py.File(geom_file) as geom_file:
        the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
            the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]
    return the_lon, the_lat

# def bit24extract(cloud_mask,geom_file,l1b_file):
# 	with h5py.File(geom_file) as geom_file,h5py.File(l1b_file) as l1b_file, h5py.File(cloud_mask) as cloud_mask_h5:
#     	#bandnel31 is emissive bandnel 10
#     	index31=10
#     	band31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
#         scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
#         offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
#         band31=(band31 - offset)*scale
#                #bandnel29 is emissive bandnel 8
#         index29=8
#         band29=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index29,:,:]
#         scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index29]
#         offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index29]
#         band29=(band29 - offset)*scale
#         the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
#         the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]
#         #getting appropriate bits from cloudmask
#         cloud_mask_all=cloud_mask_h5['mod35']['Data Fields']['Cloud_Mask'][...]
#         bit24_flag=bitmap.getbit(cloud_mask_all[3,:,:],0)

# 	return band29, band31, the_lon, the_lat, bit24_flag 
