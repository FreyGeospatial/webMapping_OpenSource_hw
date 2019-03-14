# Jordan Frey
# Web Mapping
# Lab 4A: Progrmming with OGR


# import packages
import ogr
import sys
import os

# set the current working directory
os.chdir('D:/OneDrive/Documents/School Work/Clark/Web Mapping/lab4_ogr/Lab4A_OGR_vector_rw2/Lab_OGR_vector_rw')

#set shapefile path
shp_path = r'D:/OneDrive/Documents/School Work/Clark/Web Mapping/lab4_ogr/Lab4A_OGR_vector_rw2/Lab_OGR_vector_rw/parks.shp'

# load driver
shp_driver = ogr.GetDriverByName('ESRI Shapefile') #driver pulled from ogr for ESRI shapefiles

#open shapefile
shp = shp_driver.Open(shp_path, 0) 

# open shapefile layer
lyr = shp.GetLayer()

# access features, starting at index 0
feature = lyr.GetFeature(0)

# return all data from column 'Object Id'
for feature in lyr:
    feature.GetField('OBJECTID')

# reset cursor
lyr.ResetReading() #pointing back to first record

# return all data from column 'Park Name'
n_feat = 0
for feature in lyr:
    print(feature.GetField('PARK_NAME'))
    n_feat += 1

lyr.ResetReading()

# filter, or select data that is of type Playground
lyr.SetAttributeFilter("PARK_TYPE2= 'Playground'")

# create new shapefile in the working directory
output_shp = shp_driver.CreateDataSource("lab4PlaygroundsSelection.shp")

# copy layer to new shapefile from previous layer
output_lyr = output_shp.CopyLayer(lyr, 'lab4PlaygroundsSelection')

# delete columns not wanted -- must take integers
output_lyr.DeleteField(9)
output_lyr.DeleteField(8)
output_lyr.DeleteField(7)
output_lyr.DeleteField(0)
output_lyr.DeleteField(0)
output_lyr.DeleteField(0)
output_lyr.DeleteField(0)
output_lyr.DeleteField(0)
