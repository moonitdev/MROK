import os, sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '../supporters'))
from databaser.GoogleSpread import GoogleSpread
from imageFns import *
from dataFns import json_to_file, modify_file, str_to_json, file_to_json

uis = file_to_json('../_config/json/uis.json')
config = file_to_json('../_config/json/config.json')
# characters = file_to_json('../_config/json/characters.json')

gdrive = GoogleSpread()

def setup_config():
    """
    기능: googledrive spreadsheet에 저장된 ROK config 내용으로 config.json 파일 생성
    출력:
        - 의미 | 데이터 타입 | 예시
        - config 정보 json 파일 | json | [{'':''}]
    Note:
        - 
    """
    dicts = gdrive.read_sheet('ROK_SETTINGS', 'config')

    out = {}
    for d in dicts:
        print(d)
        out[d['key']] = d['value']

        if d['type'] == 'int':
            out[d['key']] = int(d['value'])
        elif  d['type'] == 'float':
            out[d['key']] = float(d['value'])
        elif  d['type'] == 'json':
            out[d['key']] = str_to_json(d['value'])

    json_to_file(out, '../_config/json/config.json', mode='w+')


def setup_ui_images():
    """
    기능: googledrive spreadsheet에 저장된 ROK ui 내용으로 이미지를 crop 저장, json 파일 생성
    출력:
        - 의미 | 데이터 타입 | 예시
        - ui 정보 json 파일 | json | [{'':''}]
    Note:
        - 
    """
    dicts = gdrive.read_sheet('ROK_SETTINGS', 'uis')
    uis = {}
    for dic in dicts:
        for k, v in dic.items():
            if k == 'x_y_w_h' and v != '':
                box = box_from_wh(list(map(int, dic['x_y_w_h'].replace(' ','').split(','))))
                source = config['SCREENSHOTS'] + dic['subdir'] + '/' + dic['source']
                print('source: {}, box: {}'.format(source, box))

                if dic['prefix'].split('_')[0] == 'box':
                    pass
                else:
                    if dic['prefix'].split('_')[0] == 'txt':
                        destination = set_img_path(dic['prefix'], category='_OCR')
                    else:
                        destination = set_img_path(dic['prefix'], category='UIS')
                
                    # print('source: {}, box: {}, destination: {}'.format(source, box, destination))
                    save_file_crop(source=source, box=box, destination=destination)

                uis[dic['prefix']] = box
    json_to_file(uis, '../_config/json/uis.json')
    modify_file('../_config/json/uis.json', {'\n}{':','}) # Note: 뒤에 추가하면서 생긴 '}{' 삭제
    # print(uis)
    return uis


def setup_characters():
    """
    기능: googledrive spreadsheet에 저장된 ROK characters 내용으로 characters.json 파일 생성
    출력:
        - 의미 | 데이터 타입 | 예시
        - character 정보 json 파일 | json | [{'':''}]
    Note:
        - 
    """
    dicts = gdrive.read_sheet('ROK_SETTINGS', 'characters')
    json_to_file(dicts, '../_config/json/characters.json', mode='w+')
    return dicts


def setup_buildings():
    """
    기능: googledrive spreadsheet에 저장된 ROK buildings 내용으로 이미지를 crop 저장, json 파일 생성
    출력:
        - 의미 | 데이터 타입 | 예시
        - buildings 정보 json 파일 | json | [{'':''}]
    Note:
        - 
    """
    dicts = gdrive.read_sheet('ROK_SETTINGS', 'buildings')

    buildings = {}
    for dic in dicts:
        if dic['box'] == '':
            continue
        buildings[dic['name']] = {}
        for k, v in dic.items():
            if k == 'image' or k == 'category' or k == 'name':
                continue
            elif v != '':
                box = box_from_wh(list(map(int, dic[k].replace(' ','').split(','))))
                source = config['SCREENSHOTS'] + '/buildings/' + dic['image']
                print('source: {}, box: {}'.format(source, box))
                buildings[dic['name']][k] = box

    json_to_file(buildings, '../_config/json/buildings.json', mode='w+')
    return buildings


##@@@@========================================================================
##@@@@ Execute Test
if __name__ == '__main__':
    setup_ui_images()  ## UI 이미지 만들기, 좌표 저장(uis.json)
    # setup_config()  ## config.json 생성
    # setup_characters()  ## characters.json 생성
    # setup_buildings() ## buildings.json 생성
