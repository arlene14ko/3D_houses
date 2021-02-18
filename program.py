from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt


dsm_ds = gdal.Open("data\DSM_07\DSM_07.tif")
dsm_gt = dsm_ds.GetGeoTransform()
dsm_proj = dsm_ds.GetProjection()

dsm_band = dsm_ds.GetRasterBand(1)
dsm_array = dsm_band.ReadAsArray()

plt.figure()
plt.imshow(dsm_array)
