from os import path
from os.path import dirname
import json
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

def getExcelPath():
    data_dir= getDataDir()
    excel_path = path.join(data_dir,'set1','data.xlsx')
    return excel_path

def getImagePath(imgIdx):
    img_path=path.join(getCaptureDir(),str(imgIdx)+'.png')
    return img_path

def getJsonPath(imgIdx):
    img_path=getImagePath(imgIdx)
    json_path=img_path+'.json'
    return json_path

def getData(imgIdx):
    json_path = getJsonPath(imgIdx)
    with open(json_path) as f:
        data = json.load(f)
        return data


print(getCaptureDir())

i = 0

data_dict={
    'imgId':[],
    'imgFile': [],
    'UpArrow':[],
    'DownArrow':[],
    'LeftArrow':[],
    'RightArrow':[],
    'action':[]
}

while(path.isfile(getImagePath(i))):
    data=getData(i)
    data_dict['imgId'].append(i)
    data_dict['imgFile'].append(getImagePath(i))
    data_dict['UpArrow'].append(data['UpArrow'])
    data_dict['DownArrow'].append(data['DownArrow'])
    data_dict['LeftArrow'].append(data['LeftArrow'])
    data_dict['RightArrow'].append(data['RightArrow'])
    action='DoNothing'
    if(data['DownArrow']=='down'):
        action='Break'
    else:
        if (data['UpArrow'] == 'down'):
            action = 'Accelerate'
        if (data['RightArrow'] == 'down'):
            action = 'TurnRight'
        if (data['LeftArrow'] == 'down'):
            action = 'TurnLeft'
    data_dict['action'].append(action)
    i += 1

df = pd.DataFrame(data_dict)

print('Data loaded')

df.to_excel(getExcelPath(),index=False)