#importing plotly.graph_objects to plot the 3D house
#importing time to check how long the code runs
import plotly.graph_objects as go
import time
#importing API class from utils.api
#importing GeoTiff class from utils.geotiff
from utils.api import API
from utils.geotiff import GeoTiff

""" 
You only need to run this program.py for the program to start.
:attrib address will contain the input address
:attrib start will get the time the program started running
:attrib address_info calls the API.get_details function, it is a dictionary
    that contains the details of the address (polygon, coordinates[x,y], etc)
:attrib polygon calls the API.get_polygon function to get the polygon of the address 
"""

address = input("Enter the Belgium address: ")
start = time.time()

address_info = API.get_details(address)
print(address_info)

polygon = API.get_polygon(address_info)
print(f"polygon: {polygon}")

num = GeoTiff.check_tiff(address_info['x_value'], address_info['y_value'])
print(f"num: {num}")

GeoTiff.get_tiff(num)
masked_files = GeoTiff.mask_tiff(num, polygon)
print(masked_files)
chm = GeoTiff.get_chm(masked_files)
print(chm)

fig = go.Figure(data=go.Surface(z=chm))
fig.update_layout(title=f"This is a 3D representation of {address}")
fig.show()
fig.write_image(f"data/3D-images/{address}.png")
end = time.time()
print(end)
print(f"Runtime of the program is {end - start}")