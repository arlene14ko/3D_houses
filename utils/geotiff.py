#importing the necessary libraries
import pandas as pd
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import rasterio as rt
from rasterio.mask import mask
import shutil

class GeoTiff:
    """
    Class GeoTiff  is where we get all the details about the GeoTiff files
    It has four functions namely:
    :check_tiff function to check from which tiff file the address is
    :get_tiff function to download the necessary tiff files
    :mask_tiff function to create the masked tiff files from the DTM and DSM files
    :get_chm function to get the CHM of the tiff files
    """
    
    
    def check_tiff(x: str, y: str) -> str:
        """
        check_tiff function is where we check from which tiff file the address belongs to.
        It needs the x and y coordinates as a parameter
        :attrib bbox will read the bounding-box.csv which contains the list of all the tiff files
        It will then go inside a for loop and check if the x and y is inside the bounding box of the tiff file
        Once it is done, the for loop will break and it will return the attrib i
        :attrib i will contain from which index the tiff file belongs to
        :attrib num will contain the number of the tiff file
        """
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
    
    
    def get_tiff(num: str):
        """
        get_tiff function is where it will download the necessary tiff files connected to the address
        It requires the num from the check_tiff as the parameter and then it will return a print statement
        :attrib files is a dictionary containing the DSM and DTm with the links on where to download it
        It will then go inside a for loop and use the urlopen, ZipFile, BytesIO to be able to extract the file without
        downloading the zip file. It will save the file in the data/temp-raster folder
        """

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
    
    
    def mask_tiff(num: str, polygon: Dict[str,str]) -> Dict[str, str]:
        """
        mask_tiff function will create the masked files for the DSM and DTM
        it requires the num and polygon as the parameter
        :attrib raster_files is a dictionary containing the path to the tif files
        :attrib masked_files is a dictionary that will contain the path of the masked files
        It will go inside a for loop and create the masked files using the rasterio mask module
        After masking the file, it will save the masked tiff file in the data/masked-files folder
        Then it will delete the data/temp-raster folder using the shutil module
        The function will return the masked files in a dictionary format
        """
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
                         "developer-name": "Arlene Postrado"
                        })

            with rt.open(f"./data/masked-files/{name}_masked.tif", "w", **out_meta) as dest:
                dest.write(out_img)
                print("writing to a new masked tiff")
                masked_files[f'{name}'] = f"./data/masked-files/{name}_masked.tif"
                print("created the masked files")
                shutil.rmtree(f"./data/temp-raster/{name}", ignore_errors=True)
                print(f"deleted the files inside the temp-raster folder for {name}")


        return masked_files
            
    
    def get_chm(masked_files: Dict[str,str]):
        """
        get_chm function will get the CHM from the dsm and dtm
        It requires the masked_files as the parameter and returns the CHM
        :attrib dsm_tiff will contain the DSM masked file
        :attrib dsm_array will read the 1st band of the the dsm_tiff
        :attrib dtm_tiff will contain the DTM masked file
        :attrib dtm_array will read the 1st band of the dtm_tiff
        :attrib chm contains the CHM array
        """
        dsm_tiff = rt.open(masked_files['DSM'])
        dsm_array = dsm_tiff.read(1)

        dtm_tiff = rt.open(masked_files['DTM'])
        dtm_array = dtm_tiff.read(1)

        chm = dsm_array - dtm_array

        return chm
            
            
            
            