#USE A DIFFERENT SHAPEFILE

import ogr
import sys
import os

shp_driver = ogr.GetDriverByName('ESRI Shapefile')
# shp_path = 'D:/OneDrive/Documents/School Work/Clark/Web Mapping/Lab_OGR_vector_rw'
# shp = shp_driver.Open(shp_path, 0)

os.getcwd()

#remoteDesktop
os.chdir('D:/OneDrive/Documents/School Work/Clark/Web Mapping/lab4_ogr/Lab4A_OGR_vector_rw2/Lab_OGR_vector_rw')
#workstation
os.chdir('E:/OneDrive/Documents/School Work/Clark/Web Mapping/lab4_ogr/Lab4A_OGR_vector_rw2/Lab_OGR_vector_rw')

data_source = shp_driver.Open('parks.shp', 0)

layer = data_source.GetLayer(0) # .GetLayer converts shapefile to layer, which is a format that OGR can read
featureCount = layer.GetFeatureCount()
print("There are " + str(featureCount) + " features in the shapefile")

#extent = layer.GetExtent()
#extent[0] #MinX
#extent[1] #MaxX
#extent[2] #MinY
#extent[3] #MaxY

#layer.GetGeomType() #0=Geometry, 1=Point, 2=Line, 3=Polygon, 100=NoGeometry
#
#layer.GetLayerDefn().GetFieldCount() #gets number of cols

for i in range(layer.GetLayerDefn().GetFieldCount()):   #you want a list [0,1,2....n] where n is the number of fields
    layer.GetLayerDefn().GetFieldDefn(i).GetName()

layer.GetSpatialRef()

#A feature definition is essentially a description of the feature object

#ACCESSING FEATURES:
feature = layer.GetFeature(0)

for feature in layer:
    feature.GetField('OBJECTID')

feature = layer.GetNextFeature()
layer.ResetReading() #pointing back to first record

feature.GetFieldDefnRef('OBJECTID')
feature['OBJECTID']
layer.ResetReading() #pointing back to first record

n_feat = 0
for feat in layer:
    print(feat.GetField('PARK_NAME'))
    n_feat += 1
#    if n_feat == 10:
#        break

layer.ResetReading() 
n_feat = 0
for feat in layer:
    print(feat.GetField('PARK_TYPE2'))
    n_feat += 1


layer.ResetReading() 
n_feat = 0
for feat in layer:
    if feat.GetField('PARK_TYPE2') == 'Playground':
        print(feat.GetField('PARK_NAME'))
        n_feat += 1



layer.ResetReading() #pointing back to first record

#for point layer, wont work on polygons
#geometry = feature.GetGeometryRef()
#geometry.GetX()
#geometry.GetY()


layer.SetAttributeFilter("PARK_TYPE2='Playground'")
homeworkDataSource = shp_driver.CreateDataSource("Playgrounds.shp")
# deep copy
homeworkLayer = data_source.CopyLayer(layer, 'Playgrounds')




outDataSource = shp_driver.CreateDataSource("homeworkShape.shp")
outLayer = outDataSource.CreateLayer("states_extent", geom_type=ogr.wkbPolygon)

#layer.ResetReading() 
#
##CREATE NEW SHAPEFILE TO WRITE DESIRED ATTRIBUTES
#homeworkShape = shp_driver.CreateDataSource('homeworkShape.shp') # create name of shpfile using driver
#homeworkLayer = homeworkShape.CreateLayer('homeworkShape', geom_type = ogr.wkbPolygon) # create new layer
#
## create new field definitions
#fldDef1 = ogr.FieldDefn('MBL', ogr.OFTInteger) # id, type integer
#fldDef1.GetWidth()
#fldDef1.SetWidth(12) #set length of field
#homeworkLayer.CreateField(fldDef1) # create field
#
#fldDef2 = ogr.FieldDefn('name', ogr.OFTString)
#fldDef2.GetWidth()
#fldDef2.SetWidth(50)
#homeworkLayer.CreateField(fldDef2)
#
### CREATE ALL FIELDS BEFORE PROCEEDING!
#homeworkFeatureDefn = homeworkLayer.GetLayerDefn()
#homeworkFeature = ogr.Feature(homeworkFeatureDefn)
#
## CREATE GEOMETRIES
#homeworkPolygon = ogr.Geometry(ogr.wkbLinearRing)
#
#
## SET FEATURE GEOMETRY
#homeworkFeature.SetGeometry(geom)


#for feat in layer:
#    if feat.GetField('PARK_TYPE2') == 'Playground':
#        
#
#

# Prints the feature geometry centroids
#for feature in layer:
#    geom = feature.GetGeometryRef()
#    print(geom.Centroid().ExportToWkt())
#
##layer.SetAttributeFilter("PARK_TYPE2")
#
#