from os import path
from os.path import dirname
import pandas as pd

def getDataDir():
    script_path = __file__
    current_folder = dirname(script_path)
    # Calculating path to the test data
    data_location = path.join(current_folder,'data' )
    data_location = path.normpath(data_location)
    return data_location;

def getCaptureDir():
    data_dir= getDataDir()
    capture_location = path.join(data_dir,'set1','capture')
    capture_location = path.normpath(capture_location)
    return capture_location


print(getCaptureDir())