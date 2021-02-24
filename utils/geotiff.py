import pandas as pd
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import rasterio as rt
from rasterio.mask import mask


class GeoTiff:
    
    
    def check_tiff(x, y):
        bbox = pd.read_csv('./data/bounding-box.csv')
        for i in range(bbox.shape[0]):
            if bbox['Left (X)'][i] <= x:
                if bbox['Right (X)'][i] >= x:
                    if bbox['Bottom (Y)'][i] <= y:
                        if bbox['Top (Y)'][i] >= y:
                            i = i
                            break                
        if i < 9 :
            num = f'k0{i+1}'
        else:
            num = f'k{i+1}' 
        return num
    
    
    def get_tiff(num):
        files = {'DSM': f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dsm-raster-1m/DHMVIIDSMRAS1m_{num}.zip", 
                 'DTM': f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dtm-raster-1m/DHMVIIDTMRAS1m_{num}.zip"}
        
        for key, value in files.items():
            with urlopen(value) as zipresp:
                print(f"Downloading the {key} zip file......")
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    print(f"Extracting the {key} zip file .......")
                    zfile.extractall(f'./data/raster-files/{key}')
                    print(f"Done extracting the {key} zip file to raster-files/{key} folder!")
        
        return("Successfully extracted the tiff files!")
    
    
    def mask_tiff(num, polygon):
        raster_files = {'DSM' : f"./data/raster-files/DSM/GeoTiff/DHMVIIDSMRAS1m_{num}.tif",
                        'DTM' : f"./data/raster-files/DTM/GeoTiff/DHMVIIDTMRAS1m_{num}.tif"}
        
        for name, file in raster_files.items():
            data = rt.open(file)
            out_img, out_transform = mask(dataset=data, shapes=[polygon], crop=True)
            out_meta = data.meta.copy()
            epsg_code = int(data.crs.data['init'][5:])
            out_meta.update({"driver": "GTiff",
                         "height": out_img.shape[1],
                         "width": out_img.shape[2],
                         "transform": out_transform,
                         "crs": epsg_code
                        })
        masked_files = {}
        with rt.open(f"./data/{name}_masked.tif", "w", **out_meta) as dest:
            dest.write(out_img)
            masked_files[{name}] = f"./data/{name}_masked.tif"
    
        return masked_files
            
    
    def get_chm():
        pass
            
            
            
            