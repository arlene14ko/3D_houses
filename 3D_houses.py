from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

dsm_ds = gdal.Open("data/DSM/DSM_01.tif")
dsm_gt = dsm_ds.GetGeoTransform()
dsm_proj = dsm_ds.GetProjection()

dsm_band = dsm_ds.GetRasterBand(1)
dsm_array = dsm_band.ReadAsArray()



#plt.figure()
#plt.imshow(dsm_array)

dsm_binmask = np.where((dsm_array >= np.mean(dsm_array)), 1,0)
plt.figure()
plt.imshow(dsm_binmask)