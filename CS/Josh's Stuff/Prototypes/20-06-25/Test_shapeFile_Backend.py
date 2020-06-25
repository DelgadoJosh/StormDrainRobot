# Unit Test for shapeFile_Backend

import shapeFile_Backend
import datetime

def test_generating_shapefile():
  fileDir = f"D:\Jay\Desktop\Joshs Folder\Code\Desk_VS_Code\Python\ArcGIS\Personal\Generated Files"
  nameOfFile = "TestFileOutput"
  xs = [420.69]
  ys = [1337.12345]
  dates = [datetime.datetime(2020, 4, 20)]

  shapeFile_Backend.create_shapefile(fileDir, nameOfFile, xs, ys, dates)

test_generating_shapefile()