# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:15:22 2019

Jordan Frey
Web mapping, Assignment 5a

Uses Python 3
"""

#import packages
import numpy as np
import gdal
import ogr
import os


#write desired wd as variable
#myPath = r"D:\OneDrive\Documents\School Work\Clark\Web Mapping\Lab5A_RasterReadWritewithGDAL"
myPath = r"E:\OneDrive\Documents\School Work\Clark\Web Mapping\Lab5A_RasterReadWritewithGDAL"

#change wd
os.chdir(myPath)

#register drivers
gdal.AllRegister()

#open landsat image
myImage = 'landsat_tm.img'
raster_ds = gdal.Open(myImage, gdal.GA_ReadOnly)

#ensure that raster file has been opened
if raster_ds is None:
    print('Could not open.')
else:
    print("File opened")

#file structure:
raster_ds.RasterCount #band count
cols = raster_ds.RasterXSize #col count
rows = raster_ds.RasterYSize #row count


#get raster bands - starts at index 1
band1 = raster_ds.GetRasterBand(1)
band3 = raster_ds.GetRasterBand(3)
band4 = raster_ds.GetRasterBand(4)

#read band as array
band3array = band3.ReadAsArray(0, 0, cols, rows).astype(np.float)
band4array = band4.ReadAsArray(0, 0, cols, rows).astype(np.float)

# compute ndvi
top = (band4array - band3array)
bottom =  (band4array + band3array)

ndvi = top / bottom

#shape of ndvi (cols, rows)
ndvi.shape

#specify driver for .img file output
imgDriver = gdal.GetDriverByName("HFA")

#get raster extent
raster_extent = raster_ds.GetGeoTransform()
print(raster_extent)

#shape of band3 -- same as ndvi.shape
bandShape = band3array.shape

#get projection from original landsat image
proj = raster_ds.GetProjection()

#create empty raster that will contain ndvi with specified extent and projection
ndvi_ds = imgDriver.Create("ndvi.img", bandShape[1], bandShape[0], 1, gdal.GDT_Float32)
ndvi_ds.SetGeoTransform(raster_extent)
ndvi_ds.SetProjection(proj) 

#save values of ndvi array to empty image file
ndvi_ds.GetRasterBand(1).WriteArray(ndvi)


#####################################################
#create boolean array where values greater than 0 are assigned a 1, and all others assigned -999
booleanNDVI = np.where(ndvi > 0, 1, -999)
#gets cols, rows of the boolean NDVI array
booleanNDVI.shape

#create empty raster that will contain boolean array with specified extent and projection
boolean_ds = imgDriver.Create("booleanNDVI.img", bandShape[1], bandShape[0], 1, gdal.GDT_Float32)
boolean_ds.SetGeoTransform(raster_extent)
boolean_ds.SetProjection(proj) 

#save vakyes if boolean array to empty image file
boolean_ds.GetRasterBand(1).WriteArray(booleanNDVI)
################################################


#specify name of clip shapefile
clip = 'clip.shp'

#specify shapefile driver
shp_driver = ogr.GetDriverByName('ESRI Shapefile')

#load in clip shapefile
clip_ds = shp_driver.Open(clip, 0)

#open the shapefile layer. Note differences here from a GDAL type (this is OGR)
clip_layer = clip_ds.GetLayer(0) 

#get extent of clip for bounding box and save values sequentially to variables
xMin, xMax, yMin, yMax = clip_layer.GetExtent() #passes on vals to xMin, xMax, yMin, yMax to variables in this order

#pixel sizes (resolution)
pixelSizeX = raster_extent[1]
pixelSizeY = -raster_extent[5] #convert negative value (-30) to positive (30)

#define clip origin
xOffset = (xMax-xMin) / pixelSizeX
yOffset = (yMax-yMin) / pixelSizeY


###########################################################################

#clip natural color composit to desired extent
clippedNatural = gdal.Warp("clippedNatural.img", raster_ds, format = "HFA", outputBounds = [xMin, yMin, xMax, yMax],
                      xRes = pixelSizeX, yRes = pixelSizeY, dstSRS = raster_ds.GetProjection())


#clip ndvi to desired extent
clippedNDVI = gdal.Warp("clippedNDVI.img", ndvi_ds, format = "HFA", outputBounds = [xMin, yMin, xMax, yMax],
                      xRes = pixelSizeX, yRes = pixelSizeY, dstSRS = ndvi_ds.GetProjection())


#clip boolean NDVI to desired extent
clippedBool = gdal.Warp("clippedBool_NDVI.img", boolean_ds, format = "HFA", outputBounds = [xMin, yMin, xMax, yMax],
                      xRes = pixelSizeX, yRes = pixelSizeY, dstSRS = boolean_ds.GetProjection())



#finish writing files to disk and close datasets
ndvi_ds = None
boolean_ds = None
clippedNDVI = None
clippedNatural = None
clippedBool = None

