# -*- coding:utf-8 -*-

##@@@@========================================================================
##@@@@ Libraries

##@@@-------------------------------------------------------------------------
##@@@ Basic Libraries
import sys, os
import math
import time

##@@@-------------------------------------------------------------------------
##@@@ Installed(conda/pip) Libraries
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pyautogui as pag
import pytesseract

from pynput.keyboard import Listener, Key

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'


SCREEN_X = 1919
SCREEN_Y = 1079

def set_viewbox(box=None):
    """
    기능: 파일 경로(이름 포함), 스크린 이미지 영역(box)을 opencv 이미지(배열)로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - box || 박스 좌표 | None / str / list | None | None: full screen[0, 0, SCREEN_X, SCREEN_Y] / str: 500 / list: [500, 300] / [100, 200, 500, 300]
    출력:
        - 의미 | 데이터 타입 | 예시
        - 이미지 영역 | list | [100, 200, 500, 300]
    Note:
        - 
    """
    if box == None:
        viewbox = [0, 0, 1920, 1080]
    elif type(box) == int:
        viewbox = [0, 0, box, box]
    elif type(box) == str:
        viewbox = [0, 0, int(box), int(box)]
    elif len(box) == 2:
        viewbox = [0, 0, box[0], box[1]]
    else:
        viewbox = box

    return viewbox




def wh_from_box(box):
    """
    Brief: get wh coordinate([x1, y1, w, h]) from box coordinate([x1:left, y1:top, x2:right, y2:bottom])
    Args:
        wh (list): wh coordinate([x1, y1, w, h])
    Returns:
        box (list): box coordinate
    """
    return [box[0], box[1], box[2] - box[0], box[3] - box[1]]


def center_from_box(box):
    """
    Brief: get box from wh
        - box coordinate([x1:left, y1:top, x2:right, y2:bottom])
        - wh coordinate([x1, y1, w, h])
    Args:
        box (list): box coordinate
    Returns:
        wh (list): wh coordinate([x1, y1, w, h])
    """
    return [(box[0] + box[2])//2, (box[1] + box[3])//2]


def box_from_center(center, wh):
    """
    Brief: get box from wh
        - box coordinate([x1:left, y1:top, x2:right, y2:bottom])
        - wh coordinate([x1, y1, w, h])
    Args:
        box (list): box coordinate
    Returns:
        wh (list): wh coordinate([x1, y1, w, h])
    """
    return [center[0] - wh[0]//2, center[1] - wh[1]//2, center[0] + wh[0]//2, center[1] + wh[1]//2]


def expand_box(box, offset=[0, 0, 0, 0]):
    """
        left, top, right, bottom
    """
    if len(box) == 2:
        box.append(box[0])
        box.append(box[1])

    if len(offset) == 1:
        for i in range(1, 4):
            offset.append(offset[0])
    if len(offset) == 2:
        offset.append(offset[0])
        offset.append(offset[1])

    for i, b in enumerate(box):
        if i < 2:
            box[i] = b - offset[i]
        else:
            box[i] = b + offset[i]

    box = fit_box_to_screen(box)
    print('box: {}'.format(box))
    return box


def fit_box_to_screen(box):
    if box[0] < 1:
        box[0] = 1
    if box[1] < 1:
        box[1] = 1
    if box[2] > _ENV['MAX_X']:
        box[2] = _ENV['MAX_X']
    if box[3] > _ENV['MAX_Y']:
        box[3] = _ENV['MAX_Y']
    return box


def snap_screenshot(box=None):
    """
    기능: 스크린 이미지 영역(box)을 opencv 이미지(배열)로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - box || 스크린샷 지정 영역 | None / list | None | None: full screen[0, 0, 1920, 1080] / list: 이미지 영역[100, 100, 600, 300]
    출력:
        - 의미 | 데이터 타입 | 예시
        - opencv 이미지(배열) | list | ...
    Note:
        - 
    """
    box = set_viewbox(box)
    
    x1 = box[0]
    y1 = box[1]
    width = box[2] - x1
    height = box[3] - y1

    img = cv2.cvtColor(np.array(pag.screenshot(region=(x1, y1, width, height))), cv2.COLOR_BGR2RGB)

    return img


def save_screenshot(box=None, path=None):
    """
    기능: 스크린 이미지 영역(box)을 해당 경로(path)에 저장
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - box || 스크린샷 지정 영역 | None / list | None | None: full screen[0, 0, 1920, 1080] / list: 이미지 영역[100, 100, 600, 300]
        - path || 저장 경로 | None / str | None | None:  / str: 저장 경로
    출력:
        - 의미 | 데이터 타입 | 예시
        - opencv 이미지(배열) | list | ...
    Note:
        - _PATH['SCREENSHOT_FOLDER']
    """
    image = snap_screenshot(box)
    if path == None:
        path = _PATH['SCREENSHOT_FOLDER'] + str(box[0]) + '_' + str(box[1]) + '_' + str(box[2]) + '_' + str(box[3]) + '.png'
    print(path)
    cv2.imwrite(path, image)
    return image


def save_file_crop(source, box=None, destination=None):
    """
    기능: source의 이미지의 해당 영역(box)을 해당 경로(path)에 저장
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - source || 원본 이미지 파일 경로 | str | None | 
        - box || 스크린샷 지정 영역 | None / list | None | None: full screen[0, 0, 1920, 1080] / list: 이미지 영역[100, 100, 600, 300]
        - destination || 저장 경로 | str | None | '../images/dest/dest01.png'
    출력:
        - 의미 | 데이터 타입 | 예시
        - opencv 이미지(배열) | list | ...
    Note:
        - _PATH['SCREENSHOT_FOLDER']
    """
    box = set_viewbox(box)
    image = cv2.imread(source, cv2.IMREAD_COLOR)[box[1]:box[3], box[0]:box[2]]
    #cv2.imshow('image', image)
    cv2.imwrite(destination, image)
    return image


def set_cv_image(image=None, color='COLOR', show=False):
    """
    기능: 파일 경로(이름 포함), 스크린 이미지 영역(box)을 opencv 이미지(배열)로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - image || 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
        - color || 이미지 컬러 | str | 'COLOR' | 'COLOR'
        - show || (확인)이미지 출력 여부 | False | True -> 화면에 출력
    출력:
        - 의미 | 데이터 타입 | 예시
        - opencv 이미지(배열) | list | ...
    Note:
        - 
    """
    if type(image) is str:    ## image file path
        if color == 'COLOR':
            img = cv2.imread(image, cv2.IMREAD_COLOR)
        elif color == 'GRAY':
            img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    elif type(image) is list: ## scren selected box
        time.sleep(3)  ##@@@@@@@@@@ delay
        img = snap_screenshot(image)

    elif type(image) is dict: ## image file path and crop box {'path':path, 'box':[,,,]}
        if color == 'COLOR':
            img = cv2.imread(image['path'], cv2.IMREAD_COLOR)
        elif color == 'GRAY':
            img = cv2.imread(image['path'], cv2.IMREAD_GRAYSCALE)
        box = image['box']
        img = img[box[1]:box[3], box[0]:box[2]]

    elif type(image) is np.ndarray: ## opencv numpy.ndarray
        img = image

    else:
        img = snap_screenshot()

    if show:
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return img


def find_match_image_box(template, image=None, mask=None, precision=0.98, method=cv2.TM_CCORR_NORMED, offset=[0,0], show=False, multi=False):
    """
    기능: 원본 이미지(image)에 템플릿 이미지(template)(>precision)가 있으면 중앙 좌표(원본 이미지) 반환, 없으면 False
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - template || 템플릿 이미지(opencv 배열) | list | 필수 | opencv 배열
        - image || 원본 이미지(opencv 배열) | list | None | opencv 배열
        - mask || 마스크 이미지(opencv 배열) | list | None | opencv 배열
        - precision || 이미지 유사도 | float | 0.98 | 0 < precision <= 1
        - method || 이미지 매칭 방법 | enum | cv2.TM_CCORR_NORMED | cv2.TM_CCORR_NORMED, ...
        - offset || 이미지가 viewbox로 지정된 경우, 중앙 좌표를 offset 만큼 이동 반환 | [100, -50]
        - show || 매칭 결과 표시 여부 | bool | False | True: 매칭 결과 창을 보여줌
        - multi || 매칭 결과를 여러개 찾을 것인지 여부 | bool | False
    출력:
        - 의미 | 데이터 타입 | 예시
        - 매칭되는 이미지 영역의 중앙 좌표(들) / Flase | list / list(of list) / False | ...
    Note:
        - 원본/템플릿 이미지가 opencv배열인 경우는 
    """
    img_original = image.copy()
    image = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    if mask is None:
        # print('mask not exist!!!')
        res = cv2.matchTemplate(image, template, method)
    else:
        # print('mask exist!!!')
        res = cv2.matchTemplate(image, template, method, mask=mask)

    # print('template.shape: {}, multi: {}'.format(template.shape, multi))
    h, w = template.shape[:]

    if not multi:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val > precision:
            center = [max_loc[0] + w//2 + offset[0], max_loc[1] + h//2 + offset[1]]
            # print('matched!!!: {}, center: {}'.format(max_val, center))
            if show == True:
                #cv2.rectangle(img_original, (max_loc[0], max_loc[1]), (max_loc[0]+w, max_loc[1]+h), (0, 0, 255), 2)
                cv2.rectangle(img_original, (max_loc[0], max_loc[1]), (max_loc[0]+w + offset[0], max_loc[1]+h + offset[1]), (0, 0, 255), 2)
                cv2.imshow('find image', img_original)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return center
        else:
            #print('not matched: {}'.format(max_val))
            return False

    else: #### search multiple matching
        loc = np.where(res >= precision)
        num = len(loc)
        print('num: {}, res: {}'.format(num, res))
        #centers = [[0, 0] for _ in range(0, num)]
        centers = []

        ### 중복(중첩) 영역 제거용
        found = np.zeros(image.shape[:2], np.uint8)
        #i = 0
        last = -10
        for pt in zip(*loc[::-1]):
            #if abs(pt[0] - last) > 1:
            if found[pt[1] + h//2, pt[0] + w//2] != 255: ##@@ 새로운 영역이라면
                found[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255  ##@@ 영역 등록
                centers.append([pt[0] + w//2 + offset[0], pt[1] + h//2 + offset[1]])
                print('pt: {}, '.format(pt))
                cv2.rectangle(img_original, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 2)

        if show == True:
            imgplot = plt.imshow(img_original)
            plt.show()

        return centers


def match_image_box(template, image=None, mask=None, precision=0.98, method=cv2.TM_CCORR_NORMED, show=False, multi=False, color=None):
    """
    기능: 원본 이미지(image)에 템플릿 이미지(template)(>precision)가 있으면 중앙 좌표(원본 이미지) 반환, 없으면 False(이미지 등 매개변수들을 find_match_image_box 함수에 전달)
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - template || 템플릿 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]}
        - image || 원본 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
        - mask || 마스크 이미지 파일 경로(이름 포함) | str | None | str: 파일 경로
        - precision || 이미지 유사도 | float | 0.98 | 0 < precision <= 1
        - method || 이미지 매칭 방법 | enum | cv2.TM_CCORR_NORMED | cv2.TM_CCORR_NORMED, ...
        - show || 매칭 결과 표시 여부 | bool | False | True: 매칭 결과 창을 보여줌
        - multi || 매칭 결과를 여러개 찾을 것인지 여부 | bool | False
    출력:
        - 의미 | 데이터 타입 | 예시
        - 매칭되는 이미지 영역의 중앙 좌표(들) / Flase | list / list(of list) / False | ...
    Note:
        - 원본/템플릿 이미지가 opencv배열인 경우는 find_match_image_box()
    """

    # image 입력값이 viewbox list인 경우, 현재 스크린 화면을 / 입력값이 dict {'path':'', 'box':[]} 인 경우, 이미지 파일을,  기준으로 box 영역으로 원본 이미지를 만들고 box 좌상의 좌표를 offset으로 지정
    offset = [0, 0]
    if type(image) is list:
        offset = [image[0], image[1]]
    elif type(image) is dict:
        offset = [image['box'][0], image['box'][1]]

    img = set_cv_image(image)
    tpl = set_cv_image(template)

    if mask != None:
        mask = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)

    if color != None:
        ## color filter 적용
        img = cv2.bitwise_and(img, img, mask=cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), np.array(color[0]), np.array(color[1])))
        tpl = cv2.bitwise_and(tpl, tpl, mask=cv2.inRange(cv2.cvtColor(tpl, cv2.COLOR_BGR2HSV), np.array(color[0]), np.array(color[1])))

        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    return find_match_image_box(template=tpl, image=img, mask=mask, precision=precision, method=method, offset=offset, show=show, multi=multi)


def extract_templates(image, show=False):
    """
    기능: 이미지에서 독립된 그림 개체(template)들 추출
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - image || 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
        - show || 추출된 템플릿 결과 표시 여부 | bool | False | True: 결과 창을 보여줌
    출력:
        - 의미 | 데이터 타입 | 예시
        - 독립된 이미지 박스들 | list | ...
    Note:
        - 
    """
    origin = [0, 0]    ## 기준 좌표

    image = set_cv_image(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 120, 255, 1)
    kernel = np.ones((5,5),np.uint8)
    dilate = cv2.dilate(canny, kernel, iterations=1)

    # Find contours
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # template boxes 좌표 배열
    boxes = []

    # Iterate thorugh contours and filter for ROI
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        box = [x + origin[0], y + origin[1], x + w + origin[0], y + h + origin[1]]
        boxes.append(box)

    if boxes == []:
        return False
    else:
        boxes = sorted(boxes, key=lambda box: box[0])
        # opencv 배열로 반환
        templates = []
        for box in boxes:
            templates.append(image[box[1]:box[3], box[0]:box[2]])
        if show == True:
            for box in boxes:
                cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
            imgplot = plt.imshow(image)
            plt.show() 

    return templates
    # return boxes


def feature_image_box(template, image, precision=0.7, inverse=True, show=False):
    """
    기능: 원본 이미지(image)에 템플릿 이미지(template)(>precision)와 유사한 부분(방향, 크기 무시)이 있으면 중앙 좌표를, 없으면 False(이미지 등 매개변수들을 find_feature_image_box 함수에 전달)
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - template || 템플릿 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]}
        - image || 원본 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]}
        - precision || 이미지 유사도 | float | 0.7 | 0 < precision <= 1
        - show || 매칭 결과 표시 여부 | bool | False | True: 매칭 결과 창을 보여줌
    출력:
        - 의미 | 데이터 타입 | 예시
        - 매칭되는 이미지 영역의 중앙 좌표(들) / Flase | list / list(of list) / False | ...
    Note:
        - 원본/템플릿 이미지가 opencv배열인 경우는 find_feature_image_box()
    """
    origin = [0, 0]    ## 기준 좌표

    img = set_cv_image(image)
    tpl = set_cv_image(template, 'GRAY')

    if type(image) is list: ## scren selected box
        origin = [image[0], image[1]]    ## 기준 좌표

    if type(template) is list: ## scren selected box
        tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)

    return find_feature_image_box(tpl, img, origin, precision, inverse)


def find_feature_image_box(template, image=None, origin=[0, 0], precision=0.7, inverse=True):
    """
    기능: 원본 이미지(image)에 템플릿 이미지(template)(>precision)와 유사한 부분(방향, 크기 무시)이 있으면 중앙 좌표를, 없으면 False
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - template || 템플릿 이미지(opencv 배열) | list | 필수 | opencv 배열
        - image || 원본 이미지(opencv 배열) | list | None | opencv 배열
        - precision || 이미지 유사도 | float | 0.7 | 0 < precision <= 1
        - show || 매칭 결과 표시 여부 | bool | False | True: 매칭 결과 창을 보여줌
    출력:
        - 의미 | 데이터 타입 | 예시
        - 매칭되는 이미지 영역의 중앙 좌표(들) / Flase | list / list(of list) / False | ...
    Note:
        - !!! opencv 3.4.2.16 이하에서만 지원됨
        - !!! opencv 3.4.2.16 설치를 위해 가상 환경을 만듬(conda create --name mrok python=3.6)
    """
    if inverse == True:
        template = ~template            # queryImage 색깔 반전!!!

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(image, None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)     # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    points_x = []
    points_y = []
    print('matches size: {}'.format(len(matches)))

    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):

        if m.distance < precision*n.distance:

            points_x.append(kp2[m.trainIdx].pt[0] + origin[0])
            points_y.append(kp2[m.trainIdx].pt[1] + origin[1])
            print('orign_x: {}, orign_y: {}'.format(origin[0], origin[1]))
            print('matching points: {}'.format(kp2[m.trainIdx].pt))    ###### matching points

    # Not Found Feature
    if points_x == []:
        return False

    center = [(min(points_x) + max(points_x))//2, (min(points_y) + max(points_y))//2]
    #print('center: {}'.format(center))
    #print('-------------------------------')
    return center


def show_image_mark(image=None, coords=[]):
    """
    기능: 이미지에 mark를 찍어줌
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - image || 원본 이미지(opencv 배열) | list | None | opencv 배열
    Note:
        - 
    """
    image = set_cv_image(image)
    for coord in coords:
        if type(coord) is list:
            cv2.circle(image, (int(coord[0]), int(coord[1])), 5, (255, 0, 0), 5)
        # cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
    imgplot = plt.imshow(image)
    plt.show()


def filter_color(image, color='WHITE'):
    if color == 'WHITE':
        lower = np.array([0,0,168])
        upper = np.array([172,111,255])

    img = set_cv_image(image)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower, upper)
    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)
    # 결과 이미지 생성
    #imgplot = plt.imshow(img_result)
    #plt.show()
    return img_result

def wait_match_image(template, image=None, precision=0.978, pause=3, duration=15):
    time.sleep(pause)
    center = match_image_box(template, image=image, precision=precision)
    _ITV_MATCH_IMAGE = 0.5
    if duration == 0:
        return center
    else:
        #n = duration // _ITV_MATCH_IMAGE
        for _ in range(0, duration):
            center = match_image_box(template, image=image, precision=precision)
            if center == False:
                time.sleep(_ITV_MATCH_IMAGE)
            else:
                return center
    return False


def set_ocr_image(image, reverse=False, path=None):
    """
    기능: 이미지 전처리(OCR용 이미지 생성)
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - image || 원본 이미지(opencv 배열) | list | None | opencv 배열
        - reverse || 이미지 색상 반전 여부 | bool | False | True -> 흑백 반전
        - path || 저장할 파일 경로 | None / str | None | 'dir1/filename.png'
    Note:
        - 
    """
    img = set_cv_image(image, 'GRAY')
    # retval, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    retval, img = cv2.threshold(img, 100, 255, cv2.THRESH_OTSU)
    img = cv2.resize(img,(0,0),fx=3,fy=3)
    img = cv2.GaussianBlur(img, (11,11), 0)
    img = cv2.medianBlur(img, 9)
    if reverse:
        img = ~img
    if img is []:
        return False
    if path != None:
        cv2.imwrite(path, img)
    # cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    imgplot = plt.imshow(img)
    plt.show()
    return img


## @@brief:: 이미지(screen box 좌표 or file path 값) 문자인식
## @@note::
def do_ocr(image, lang='eng', reverse=False, direct=True):
    """
    기능: 이미지의 해당 언어(eng) 문자인식 결과를 반환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - image || 원본 이미지(opencv 배열) | list | None | opencv 배열
        - lang || OCR 기준 언어 | str | eng | eng / num / ...
        - reverse || 이미지 색상 반전 여부 | bool | False | True -> 흑백 반전
    Note:
        - 
    """
    if not direct:
        img = set_ocr_image(image=image, reverse=reverse)
    else:
        img = image
    # imgplot = plt.imshow(img)
    # plt.show()
    # print(pytesseract.image_to_string(img, lang, config = tessdata_dir_config))
    return pytesseract.image_to_string(img, lang, config = tessdata_dir_config)


# def do_ocr_filtered(image, color='WHITE', lang='eng', reverse=False):
#     img = filter_color(image, color)
#     #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     retval, img = cv2.threshold(img,200,255, cv2.THRESH_BINARY)
#     img = cv2.resize(img,(0,0),fx=3,fy=3)
#     img = cv2.GaussianBlur(img,(11,11),0)
#     img = cv2.medianBlur(img,9)
#     if reverse:
#         img = ~img
#     if img is []:
#         return False
#     imgplot = plt.imshow(img)
#     plt.show()
#     return pytesseract.image_to_string(img, lang, config = tessdata_dir_config)


## @@brief:: 이미지(screen box 좌표 or file path 값) 문자인식
## @@note::
def rectify_ocr(text, lang='digit'):
    if lang is 'digit':
        s = ['i', 'I', 'l', 'o', 'O', ',']
        d = ['1', '1', '1', '0', '0', '']
        for i, v in enumerate(s):
            #print('s: {}, d: {}'.format(s[i], d[i]))
            text = text.replace(s[i], d[i])
    return text

if __name__ == '__main__':

    # image = {'path': '../_setup/screenshots/test/source_test01.png', 'box': [0, 0, 600, 100]}
    # template = '../_setup/screenshots/test/template_test01.png'

    # center = match_image_box(template=template, image=image, mask=None, precision=0.98, method=cv2.TM_CCORR_NORMED, show=True, multi=False, color=None)

    # print(center)

    # template = '../_setup/screenshots/test/verification_templates01.png'
    # image = '../_setup/screenshots/test/verification_image01.png'

    # path = '../_setup/screenshots/verification/full06.png'
    # tpl = {'path': path, 'box': [948, 210, 1200, 280]}
    # image = {'path': path, 'box': [732, 282, 1190, 742]}

    # # boxes = extract_templates(template, False)
    # templates = extract_templates(tpl, False)

    # centers = []
    # for template in templates:
    #     center = feature_image_box(template, image, precision=0.75, inverse=True)
    #     if center is False:
    #         print('no match image')
    #     centers.append(center)
    
    # print(centers)

    # show_image_mark(image=image, coords=centers)

    image = '../_setup/screenshots/ocr/rankings_top_power01.png'
    path = '../_setup/screenshots/ocr/main_top_location01.png'
    # path = '../_setup/screenshots/ocr/internet01.png'

    # set_ocr_image(image, reverse=True, path=path)

    # ocr = do_ocr(path, lang='digits_comma', reverse=True, direct=False)
    ocr = do_ocr(path, lang='eng', reverse=True, direct=False)
    print('ocr result: {}'.format(ocr))

# def find_verification_verify():
#     # return _bs.match_image_box(get_image_path('btn_VerificationVerify', 'UIS'), precision=0.9)
#     return _bs.match_image_box(get_image_path('btn_VerificationVerify', 'UIS'), [830, 470, 1738, 648], precision=0.9)


# def do_verification_reward(precision=0.4):
#     template = [946, 220, 1180, 272]
#     image = [730, 280, 1190, 740]
#     img_btn_OK = [1024, 754, 1190, 812]

#     center_btn_OK = [1100, 786]
#     center_btn_close = [756, 782]

#     boxes = _bs.extract_templates(template)
#     print('boxes at gui.py: {}'.format(boxes))

#     if len(boxes) > 4 or boxes is False:
#         print('too many templates')
#         click_mouse(center_btn_close)
#         return False

#     centers = []
#     for box in boxes:
#         center = _bs.feature_image_box(box, image, precision, inverse=True)
#         if center is False:
#             print('no match image')
#             click_mouse(center_btn_close)
#             return False
#         centers.append(center)
    
#     print(centers)
#     for center in centers:
#         click_mouse(center)
#         delay_secs(1)

#     click_mouse(center_btn_OK)

#     return centers


# def do_verification_rewards(precision=0.4, attempts=6):
#     btn_verify = find_verification_verify()
#     if btn_verify is False:
#         return 0
#     else:
#         click_mouse(btn_verify)
#         delay_secs(5)

#     center_btn_OK = [1104, 784]
#     centers = do_verification_reward(precision)

#     tries = 0

#     if centers is False:
#         tries += 1
#         # print('no match image!')
#         # if tries > attempts:
#         #     do_verification_rewards()  ## 재시도@@@@@@@@@@

#         # click_mouse([800, 120])  ## 인증 팝업 바깥쪽을 누름@@@@@
#         delay_secs(5)
#         do_verification_rewards(precision, attempts)

#     elif len(centers) > 4:
#         tries += 1
#         # print('too many templates!')
#         # if tries > attempts:
#         #     do_verification_rewards()  ## 재시도@@@@@@@@@@
#         # click_mouse([800, 120])  ## 인증 팝업 바깥쪽을 누름@@@@@
#         delay_secs(5)
#         do_verification_rewards(precision)

#     delay_secs(5)

#     if find_verification_verify() is False:
#         print(centers)
#         return centers
#     else:
#         do_verification_rewards(precision, attempts)