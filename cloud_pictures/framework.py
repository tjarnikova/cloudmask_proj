
# coding: utf-8

# #Are there clouds in the sky?
# 
# ##Reproducing the MODIS cloudmask using MODIS level 1 Radiance Data

# Clouds are generally cooler and more reflective than the earth's surface. The MODIS cloud mask uses this principle to test for cloud presence based on reflectances and brightness temperatures measured at different wavelengths of light by the Moderate Resolution Imaging Spectroradiometer, which orbits Earth on the Terra and Aqua Satellites (both built by NASA).  
# 
# This project aims to compare several bits of the MODIS 48-bit cloudmask with cloud determining tests performed on raw MODIS level 1 data. These tests were written using the Modis Algorithm Theoretical Basis Document as a guide (Ackerman et al, 2010), with the aim to examine how closely they reproduce the output of the final mask product. 
# 
# I wrote tests for  five bits of the mask: Bit 13, Bit 18, Bit 19, Bit 21, and Bit 24 and tested them on the skies over Great Britain using raw data from four different days.  

# #The study area

#  I ran the tests on similar satellite passes on four separate days:
# 
# January 4, 2014 at 13:25
# 
# February 10, 2014 at 13:15 
# 
# June 6, 2014, at 13:20
# 
# March 5, 2015, at 13:20
# 
# Though the passes differ slightly in spatial extent (according to time of satellite passing), all four cover Great Britain. The image below represents the spatial extent of the passes. For the cloudmask tests, I focused on analyzing the area around Great Britain, so I set the extent of the maps between 49 - 59 ° latitude and -11 - 3° longitude. 

# <img src=/files/notefoto/Britain.png>

# #Data products used

# In this analysis, I used 3 different types of NASA data products. All 3 can be downloaded at https://ladsweb.nascom.nasa.gov/data/search.html, under the Aqua MODIS Satellite heading. The products are as follows:
# 
# -Level 1B calibrated radiances (MYD021KM, Aqua Level 1 Product) - contains radiance data at different bands of the MODIS for a given pass (denoted by date and time recorded in filename). A reference table of band number correspondences to wavelength can be found here: (https://en.wikipedia.org/wiki/Moderate-Resolution_Imaging_Spectroradiometer)
# 
# -Geolocation (MYD03, Aqua Level 1 Product) - Contains georeferencing information for a given pass (denoted by date and time recorded in filename, which can be matched with other products for the same pass). 
# 
# -MYD35_L2 (MODIS Level 2 Cloud Mask and Spectral Test Results, Aqua Atmosphere Level 2 Product) - Contains the results of the MODIS cloudmask. 
# 
# My aim in this analysis was to compare the MYD35_L2 cloudmask with the results of tests run on MYD021KM data. The visual comparison of both products (the MODIS cloudmask and my recreation of it) is enabled by plotting both using the same geolocation file. 

# ##The principle of brightness temperature: bits 13, 18, 21

# discuss brightness temperature here

# ##The principle of reflectance: bits 19 and 24

# reflectance

# ##Bit 13: Brightness temperature

# Bit 13 in the MODIS mask is a Group 1 test that uses brightness temperature at 11 microns (MODIS band 31, emissive channel 10) to determine the presence of thick high clouds (the colder the brightness temperature, the higher the chance of cloud presence). The test is difficult to use over land because surface emissivity varies considerably with soil and vegetation type. (According to Ackerman 1997, the test is most effective over ocean at night.) Ackerman uses the following thresholds: 267 K, 270 K and 273 K, with 270 K being the threshold value below which the pixel fails the clear-sky condition. 
# 
# I recreated this test using a script that extracts radiance (W/m^2/micron/sr) at a wavelength of 11 microns for all pixels in a given MODIS level 1 file (filename designation MYD021), then finds brightness temperature from this radiance by solving the Planck function for brightness temperature given radiance and wavelength. (The Planck inversion functon was written by Phil Austin). 
# This script returns an array of brightness temperatures, which can be plotted using the MYD03 geolocation file. It is then possible to write a script that takes an array of brightness temperatures as an input and returns a probability of cloudiness based on the Ackerman thresholds as follows (BT = Brightness Temperature). There are 4 categories of probabilities, with 0 representing cloudy sky and 3 representing a 99% probability clear sky, as listed below:
# 
# 	BT < 267..................... 0 - cloud
# 	267 <= BT < 270 ..............1 - 66% probability clear
# 	270 <= BT < 273 ..............2 - 95% probability clear
# 	BT > 267......................3 - 99% probability clear 

# <img src=files/plot_output/Bit13/bit13.png>

# ##Quantifying differences between my tests and the MODIS mask: histograms

# <img src=files/plot_output/Bit13/thresholds.png>

# In[ ]:



