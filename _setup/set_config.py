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
from settings import _ENV, _PATH, _MAP
# from emulators import KEY_MAP as ui_key
# from emulators import LOCATION_ROK_FULL as ui_xy
# from emulators import IMAGE_ROK_FULL as ui_img
sys.path.append(os.path.join(os.path.dirname(__file__), '../supporters'))
from databaser.GoogleSpread import GoogleSpread
##@@@@========================================================================
##@@@@ Functions

##@@@-------------------------------------------------------------------------
##@@@ Basic Functions

# def setup_ui_images(file_='TEST', sheet_='crop'):
#     """
#     Brief: 
#     Args:
#     Returns:
#     """
#     dicts = _bs.get_dict_from_sheet(_bs.fetch_sheet(file_, sheet_), 0)
#     #jsons = []
#     uis = {}
#     for dic in dicts:
#         for k, v in dic.items():
#             if k == 'x_y_w_h' and v != '':
#                 # dicts.remove(dic)

#                 shots = '/Volumes/data/dev/SynologyDrive/projects/_ROK/bot/_screenShots/'
#                 file = shots + re.sub(r'\D', '', dic['original']) + _ENV['IMG_EXT']
#                 box = _bs.compute_box_from_wh(list(map(int, dic['x_y_w_h'].replace(' ','').split(','))))
#                 #box = _bs.compute_box_from_wh(list(map(int, dic['x_y_w_h'].replace(' ','').split(','))))
#                 path = '../images/_uis/' + dic['prefix'] + _ENV['IMG_EXT']
#                 print('file: {}, box: {}, path: {}'.format(file, box, path))

#                 ### save ui images
#                 if dic['use'] == 'i' or dic['use'] == 'b':
#                     _bs.save_file_crop(file, box, path)
#                 if dic['use'] == 'x' or dic['use'] == 'b':
#                     uis[dic['prefix']] = _bs.compute_center_from_box(box)
#                 _bs.json_to_file(uis, '../_config/uis.json')
#     print(uis)
#     return uis


# def setup_ui_boxes(file_='TEST', sheet_='crop'):
#     dicts = _bs.get_dict_from_sheet(_bs.fetch_sheet(file_, sheet_), 0)
#     #jsons = []
#     uis = {}
#     for dic in dicts:
#         for k, v in dic.items():
#             if k == 'use' and v == 'x':
#                 uis[dic['prefix']] = _bs.compute_box_from_wh(list(map(int, dic['x_y_w_h'].replace(' ','').split(','))))
#                 _bs.json_to_file(uis, '../_config/ui_boxes.json')
#     print(uis)
#     return uis


##@@@@========================================================================
##@@@@ Execute Test
if __name__ == '__main__':
    pass
    gdrive = GoogleSpread()
    # read = gdrive.read_sheet('ROK_UI', '1920_1080')
    read = gdrive.read_sheet('Coin_Exchanges', 'test')
    
    print(read)
