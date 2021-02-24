import pandas as pd
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import rasterio as rt
from rasterio.mask import mask
import shutil

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
        if i < 9:
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
                    zfile.extractall(f'./data/temp-raster/{key}')
                    print(f"Done extracting the {key} zip file to temp-raster/{key} folder!")
        
        return("Successfully extracted the tiff files!")
    
    
    def mask_tiff(num, polygon):
        print("Mask tiff function")
        raster_files = {'DSM' : f"./data/temp-raster/DSM/GeoTiff/DHMVIIDSMRAS1m_{num}.tif",
                        'DTM' : f"./data/temp-raster/DTM/GeoTiff/DHMVIIDTMRAS1m_{num}.tif"}
        masked_files = {}
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

            with rt.open(f"./data/masked-files/{name}_masked.tif", "w", **out_meta) as dest:
                dest.write(out_img)
                print("writing to a new masked tiff")
                masked_files[f'{name}'] = f"./data/masked-files/{name}_masked.tif"
                print("created the masked files")
                shutil.rmtree(f"./data/temp-raster/{name}", ignore_errors=True)
                print(f"deleted the files inside the temp-raster folder for {name}")


        return masked_files
            
    
    def get_chm(masked_files):
        dsm_tiff = rt.open(masked_files['DSM'])
        dsm_array = dsm_tiff.read(1)

        dtm_tiff = rt.open(masked_files['DTM'])
        dtm_array = dtm_tiff.read(1)

        chm = dsm_array - dtm_array

        return chm
            
            
            
            