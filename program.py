#importing plotly.graph_objects to plot the 3D house
#importing time to check how long the code runs
from shapely.geometry import Polygon
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
print(f"Address : {address}")
print(f"The X coordinate: {address_info['x_value']} and the Y coordinate: {address_info['y_value']}.")

polygon = API.get_polygon(address_info)
print(f"The polygon: {Polygon(polygon['coordinates'][0])}")

""" 
:attrib num calls the GeoTiff.check_tiff function to check in which tiff file the address belongs to
Calling the GeoTiff.get_tiff with num parameter to download the necessary tiff files
:attrib masked_files is a dictionary containing the masked tiff files, 
    it calls the GeoTiff.mask_tiff function with num and polygon as the parameter and creates two masked files
    DSM_masked.tif and DTM_masked.tif and saves it in the data/masked-files folder.
:attrib chm calls the GeoTiff.get_chm function and gets the CHM of the masked DSM and DTM
"""

num = GeoTiff.check_tiff(address_info['x_value'], address_info['y_value'])

GeoTiff.get_tiff(num)
masked_files = GeoTiff.mask_tiff(num, polygon)
print(f"Successfully created the masked files! {masked_files}")
chm = GeoTiff.get_chm(masked_files)
print(f"Successfully created the CHM file for {address}")

""" 
:attrib fig will be the figure of the CHM in 3D, it will also show the 3D and write the save the png of the figure 
    inside the data/3D-images forlder.
:attrib end will contain the end time the program runs and then it will compute the total of how long the program runs
"""

fig = go.Figure(data=go.Surface(z=chm))
fig.update_layout(title=f"This is a 3D representation of {address}")
fig.show()
fig.write_image(f"data/3D-images/{address}.png")
end = time.time()
print(f"Runtime of the program is {end - start}")