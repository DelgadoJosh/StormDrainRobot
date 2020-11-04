# UCF
# Senior Design
# Stormwater Drain Robot
# Team Black

# ShapeFile_BackEnd
# This will take in data, and generate a shapefile from it

import shapefile as shp 
import os 
import sys 

# 
def create_shapefile(fileDir, nameOfFile, xs, ys, dates):
  
  # Location of the shapefile
  savePath = fileDir + "\\" + nameOfFile
  
  # Set up shapefile writer, and create empty fields
  shapeFileWriter = shp.Writer(savePath, shp.POINT)
  shapeFileWriter.autobalance = 1 # Ensures geometry and attributes match
  shapeFileWriter.field("x", "F", 10, 8) # Float with 10.8 precision
  shapeFileWriter.field("y", "F", 10, 8)
  shapeFileWriter.field("Date", "D")

  for index, xCord in enumerate(xs):
    shapeFileWriter.point(xs[index], ys[index]) # Write the geometry
    shapeFileWriter.record(xs[index], ys[index], dates[index])

    
  
  # Save the shapefile
  shapeFileWriter.close()


