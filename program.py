from utils.api import API
from utils.geotiff import GeoTiff

address = input("Enter the Belgium address: ") 

x, y = API.get_coordinates(address)

num = GeoTiff.check_tiff(x, y)

polygon = API.get_polygon(address)

mask = GeoTiff.mask_tiff(num, polygon)