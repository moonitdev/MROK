# -*- coding:utf-8 -*-
"""
Function: Set Of Game Bot Emulator Configurations

Structure:
    - _ENV
    - _PATH
    - _TESSERACT
    - _GOOGLE

Usage: from _config.settings import *
"""

_ENV = {
    'MAX_X': 1920,
    'MAX_Y': 1080,
    'ZOOM_MAX': 50,
    'IMG_EXT': '.png',
    'EMULATOR': 'LDPLAYER',
    'MOUSE_DURATION': 0.5,
    'MOUSE_CLICK_PAUSE': (0, 0), # 마우스 클릭 (전, 후) 멈춤 시간
    'CLICK_INTERVAL': 1,
}

_PATH = {
    'ROOT': '../images/',
    'UIS': '../images/uis/',  ## UI images
    '_UIS': '../images/_uis/',  ## UI images
    'OBJECTS': '../images/objects/',  ## UI images
    'MAPS': '../images/maps/',  ## map images
    'SCREENSHOT': '../images/screenshots/'  ## screenshot images
}

_TESSERACT = {
    'WIN': {
        ## Notebook
        'EXE': 'C:/Program Files/Tesseract-OCR/tesseract.exe',
        'DATA': '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"',
    }
}


_GOOGLE = {
    'JSON': '../_config/rok_service_account_googledrive.json',
    'SCOPE': [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ],
    'URLS': {
        'TEST': 'https://docs.google.com/spreadsheets/d/1zwHf6FEcqb_vyHC-3uSlzzE0ln8zoMsW5-YwNzTryLU/edit#gid=0',
        'LOGS': 'https://docs.google.com/spreadsheets/d/1yOj3yXIAZzDyEfzwqr0MMsEq9vwEyo0WXvS9yj_L7uY/edit#gid=443257774'
    }
}

_MAP = {
    'WHOLE': [1200, 1200],
    'ONE_MIN': [8, 6],
    'ONE_MAX': [320, 240],
    'EDGE': [230, 170, 1600, 900],
    ## Transformation Matrix Perspective Coordinate Coordinate To Carsian(Rectangular)
    'Matrix_P2C': [
        [ 1.35162297e+00,  6.28326412e-01, -3.39296263e+02],
        [ 6.93889390e-17,  2.27541342e+00, -4.98846844e+02],
        [ 2.71050543e-19,  6.51153648e-04,  1.00000000e+00]
    ],
    'CLOCKWISE' : [
        [0, 0],
        [-0.725, 0],  # 우 right
        [0, -0.95],  # 하 bottom
        [0.73, 0],  # 좌 left
        [0.73, 0],  # 좌 left
        [0, 1.353],  # 상 top
        [0, 1.353],  # 상 top
        [-0.726, 0],  # 우 right
        [-0.726, 0],  # 우 right
        [0, -0.942],  # 하 bottom
    ],
    'R_UNITS' : [
        [0, 0],
        [-1, 0],  # 우 right
        [0, -1],  # 하 bottom
        [1, 0],  # 좌 left
        [1, 0],  # 좌 left
        [0, 1],  # 상 top
        [0, 1],  # 상 top
        [-1, 0],  # 우 right
        [-1, 0],  # 우 right
    ],
    'SCAN_BOX': [710, 390, 1210, 690]  # 부족 마을, 동굴 탐험용 scan box (minimum size map, 좌표 100 이동 기준)
}


_FILTER : {
    'yellow_lower': [20, 100, 100],
    'yellow_upper': [30, 255, 255],
}