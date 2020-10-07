##@@@-------------------------------------------------------------------------
##@@@ Basic Libraries
import os, sys
import re
import time
import numpy as np

##@@@-------------------------------------------------------------------------
##@@@ Installed(conda/pip) Libraries
import pyautogui as pag
import cv2
import pytesseract


##@@@-------------------------------------------------------------------------
##@@@ External(.json/.py)
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '_config'))
from settings import _ENV, _IMGS, _MAP
# from emulators import KEY_MAP as ui_key
# from emulators import LOCATION_ROK_FULL as ui_xy
# from emulators import IMAGE_ROK_FULL as ui_img
sys.path.append(os.path.join(os.path.dirname(__file__), '../supporters'))
from databaser.GoogleSpread import GoogleSpread
from imageFns import *
from dataFns import json_to_file

##@@@@========================================================================
##@@@@ Functions

##@@@-------------------------------------------------------------------------
##@@@ Basic Functions

gdrive = GoogleSpread()
dicts = gdrive.read_sheet('ROK_UI', '1920_1080')
# ROOT = 'C:\\Dev\\docMoon\\projects\\MROK\\_setup\\screenshots\\'

def setup_ui_images():
    """
    기능: googledrive spreadsheet에 저장된 ROK ui 내용으로 이미지를 crop 저장, json 파일 생성
    출력:
        - 의미 | 데이터 타입 | 예시
        - ui 정보 json 파일 | json | [{'':''}]
    Note:
        - 
    """
    uis = {}
    for dic in dicts:
        for k, v in dic.items():
            if k == 'x_y_w_h' and v != '':
                box = box_from_wh(list(map(int, dic['x_y_w_h'].replace(' ','').split(','))))
                source = _IMGS['SCREENSHOTS'] + dic['subdir'] + '/' + dic['source']
                # print('source: {}, box: {}, path: {}'.format(source, box, path))

                if dic['prefix'].split('_')[0] == 'box':
                    pass
                else:
                    if dic['prefix'].split('_')[0] == 'txt':
                        destination = _IMGS['_OCR'] + dic['prefix'] + _ENV['IMG_EXT']
                    else:
                        destination = _IMGS['UIS'] + dic['prefix'] + _ENV['IMG_EXT']
                
                    # print('source: {}, box: {}, destination: {}'.format(source, box, destination))
                    save_file_crop(source=source, box=box, destination=destination)

                uis[dic['prefix']] = box
                json_to_file(uis, '../_config/json/uis.json')
    # print(uis)
    return uis


# def setup_ui_boxes(file_='TEST', sheet_='crop'):
#     dicts = _bs.get_dict_from_sheet(_bs.fetch_sheet(file_, sheet_), 0)
#     #jsons = []
#     uis = {}
#     for dic in dicts:
#         for k, v in dic.items():
#             if k == 'use' and v == 'x':
#                 uis[dic['prefix']] = box_from_wh(list(map(int, dic['x_y_w_h'].replace(' ','').split(','))))
#                 _bs.json_to_file(uis, '../_config/ui_boxes.json')
#     print(uis)
#     return uis


##@@@@========================================================================
##@@@@ Execute Test
if __name__ == '__main__':
    pass
    # gdrive = GoogleSpread()
    # read = gdrive.read_sheet('ROK_UI', '1920_1080')
    # # read = gdrive.read_sheet('Coin_Exchanges', 'test')
    
    # print(read)

    # box = box_from_wh([651, 1040, 32, 30])
    # print(box)
    setup_ui_images()
