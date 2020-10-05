# -*- coding:utf-8 -*-

##@@@@========================================================================
##@@@@ Libraries

##@@@-------------------------------------------------------------------------
##@@@ Basic Libraries
import sys, os
import math

##@@@-------------------------------------------------------------------------
##@@@ Installed(conda/pip) Libraries
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pyautogui as pag

from pynput.keyboard import Listener, Key

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
    if type(box) == str:
        viewbox = [0, 0, box, box]
    elif len(box) == 2:
        viewbox = [0, 0, box[0], box[1]]
    else:
        viewbox = box

    return viewbox


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
        print('local image')
    elif type(image) is list: ## scren selected box
        time.sleep(3)  ##@@@@@@@@@@ delay
        img = snap_screenshot(image)
        print('screen area image')
    elif type(image) is dict: ## image file path and crop box {'path':path, 'box':[,,,]}
        if color == 'COLOR':
            img = cv2.imread(image['path'], cv2.IMREAD_COLOR)
        elif color == 'GRAY':
            img = cv2.imread(image['path'], cv2.IMREAD_GRAYSCALE)
        box = image['box']
        img = img[box[1]:box[3], box[0]:box[2]]
    else:
        img = snap_screenshot()

    if show:
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return img

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


# class ImageProcessor:

#     def __init__(self, source=None, target=None, box=[0, 0, 1920, 1080]):
#         self.source = source
#         self.target = target
#         self.box = box

#     def snap_screenshot(box=None):
#         """
#         기능: 파일 경로(이름 포함), 스크린 이미지 영역(box)을 opencv 이미지(배열)로 변환
#         입력:
#             - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
#             - box || 스크린샷 지정 영역 | None / list | None | None: full screen[0, 0, 1920, 1080] / list: 이미지 영역[100, 100, 600, 300]
#         출력:
#             - 의미 | 데이터 타입 | 예시
#             - opencv 이미지(배열) | list | ...
#         Note:
#             - 
#         """
#         if box == None:
#             box = self.box
        
#         x1 = box[0]
#         y1 = box[1]
#         width = box[2] - x1
#         height = box[3] - y1

#         img = cv2.cvtColor(np.array(pag.screenshot(region=(x1, y1, width, height))), cv2.COLOR_BGR2RGB)

#         return img


#     def save_screenshot(box=None, path=None):
#         """
#         기능: 스크린샷 저장
#         입력:
#             - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
#             - image || 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
#         Note:
#             - 
#         """
#         """
#         Brief: save screenshot
#         Args:
#             box (list): 스크린샷 지정 영역(default: 전체 화면)
#             path (str): 저장 위치
#         Returns:
#             opencv image array
#         """
#         image = snap_screenshot(box)
#         if path == None:
#             path = _PATH['SCREENSHOT_FOLDER'] + str(box[0]) + '_' + str(box[1]) + '_' + str(box[2]) + '_' + str(box[3]) + '.png'
#         print(path)
#         cv2.imwrite(path, image)
#         return 0


#     def save_file_crop(file, box, path=None):
#         """
#         Brief: save screenshot
#         Args:
#             file
#             box (list): 스크린샷 지정 영역(default: 전체 화면)
#             path (str): 저장 위치
#         Returns:
#             opencv image array
#         """

#         #image = cv2.imread(file.replace(" ", "\ "), cv2.IMREAD_COLOR)[box[1]:box[3], box[0]:box[2]]
#         image = cv2.imread(file, cv2.IMREAD_COLOR)[box[1]:box[3], box[0]:box[2]]
#         #cv2.imshow('image', image)
#         cv2.imwrite(path, image)
#         return 0


#     # def extract_templates(image):
#     #     """
#     #     기능: 이미지에서 독립된 그림 개체(template)들 추출
#     #     입력:
#     #         - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
#     #         - image || 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
#     #     출력:
#     #         - 의미 | 데이터 타입 | 예시
#     #         - 독립된 이미지 박스들 | list | ...
#     #     Note:
#     #         - 
#     #     """
#     #     origin = [0, 0]    ## 기준 좌표
#     #     if type(image) is str:
#     #         image = cv2.imread(image, cv2.IMREAD_COLOR)
#     #     else: ## scren selected box
#     #         origin = image.copy()
#     #         image = snap_screenshot(image)

#     #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     #     blurred = cv2.GaussianBlur(gray, (3, 3), 0)
#     #     canny = cv2.Canny(blurred, 120, 255, 1)
#     #     kernel = np.ones((5,5),np.uint8)
#     #     dilate = cv2.dilate(canny, kernel, iterations=1)

#     #     # Find contours
#     #     cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     #     cnts = cnts[0] if len(cnts) == 2 else cnts[1]

#     #     # template boxes 좌표 배열
#     #     boxes = []

#     #     # Iterate thorugh contours and filter for ROI
#     #     for c in cnts:
#     #         x, y, w, h = cv2.boundingRect(c)
#     #         box = [x + origin[0], y + origin[1], x + w + origin[0], y + h + origin[1]]
#     #         boxes.append(box)

#     #     if boxes == []:
#     #         return False
#     #     else:
#     #         boxes = sorted(boxes, key=lambda box: box[0])

#     #     print('boxes at image_recognition.py: {}',format(boxes))
#     #     return boxes


#     # def match_image_box(template, image=None, mask=None, precision=0.98, method=cv2.TM_CCORR_NORMED, show=False, multi=0, color=None):
#     #     """
#     #     Brief:
#     #         - 매칭 되는 이미지(>precision) 중앙 좌표 반환, 없으면 False
#     #         -    match_image_box -> set_cv_image(template/image) + find_match_image_box
#     #     Args:
#     #         template (str: image file path / list: screen image area):
#     #         offset (list) : 중앙 좌표 (이동)보정
#     #         image (str: image file path / list: screen image area):
#     #         mask: 마스크 이미지
#     #         precision: 이미지 유사도
#     #         method: 이미지 매칭 방법
#     #         show:
#     #         multi:
#     #     Returns:
#     #         center (list) : center of box[x1, y1]
#     #     """
#     #     offset = [0, 0]
#     #     if type(image) is list:
#     #         offset = [image[0], image[1]]

#     #     img = set_cv_image(image)
#     #     tpl = set_cv_image(template)

#     #     if mask != None:
#     #         mask = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)

#     #     if color != None:
#     #         ## color filter 적용
#     #         img = cv2.bitwise_and(img, img, mask=cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), np.array(color[0]), np.array(color[1])))
#     #         tpl = cv2.bitwise_and(tpl, tpl, mask=cv2.inRange(cv2.cvtColor(tpl, cv2.COLOR_BGR2HSV), np.array(color[0]), np.array(color[1])))

#     #         # cv2.imshow('img', img)
#     #         # cv2.waitKey(0)
#     #         # cv2.destroyAllWindows()

#     #     return find_match_image_box(template=tpl, image=img, mask=mask, precision=precision, method=method, offset=offset, show=show, multi=multi)


#     # #def find_match_image_box(template, image=None, mask=None, precision=0.3, method=cv2.TM_CCOEFF_NORMED, show=False, multi=0):
#     # def find_match_image_box(template, image=None, mask=None, precision=0.98, method=cv2.TM_CCORR_NORMED, offset=[0,0], show=False, multi=0):
#     #     """
#     #     Brief: 매칭 되는 이미지(>precision) 중앙 좌표 반환, 없으면 False
#     #     Args:
#     #         template (cv2 image array):
#     #         image (cv2 image array):
#     #     """
#     #     img_original = image.copy()
#     #     image = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
#     #     template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

#     #     if mask is None:
#     #         print('mask not exist!!!')
#     #         res = cv2.matchTemplate(image, template, method)
#     #     else:
#     #         print('mask exist!!!')
#     #         res = cv2.matchTemplate(image, template, method, mask=mask)

#     #     print('template.shape: {}, multi: {}'.format(template.shape, multi))
#     #     h, w = template.shape[:]

#     #     if multi == 0:
#     #         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

#     #         if max_val > precision:
#     #             center = [max_loc[0] + w//2 + offset[0], max_loc[1] + h//2 + offset[1]]
#     #             print('matched!!!: {}, center: {}'.format(max_val, center))
#     #             if show == True:
#     #                 #cv2.rectangle(img_original, (max_loc[0], max_loc[1]), (max_loc[0]+w, max_loc[1]+h), (0, 0, 255), 2)
#     #                 cv2.rectangle(img_original, (max_loc[0], max_loc[1]), (max_loc[0]+w + offset[0], max_loc[1]+h + offset[1]), (0, 0, 255), 2)
#     #                 cv2.imshow('find image', img_original)
#     #                 cv2.waitKey(0)
#     #                 cv2.destroyAllWindows()
#     #             return center
#     #         else:
#     #             #print('not matched: {}'.format(max_val))
#     #             return False

#     #     else: #### search multiple matching
#     #         loc = np.where(res >= precision)
#     #         num = len(loc)
#     #         print('num: {}, res: {}'.format(num, res))
#     #         #centers = [[0, 0] for _ in range(0, num)]
#     #         centers = []


#     #         ### 중복(중첩) 영역 제거용
#     #         found = np.zeros(image.shape[:2], np.uint8)
#     #         #i = 0
#     #         last = -10
#     #         for pt in zip(*loc[::-1]):
#     #             #if abs(pt[0] - last) > 1:
#     #             if found[pt[1] + h//2, pt[0] + w//2] != 255: ##@@ 새로운 영역이라면
#     #                 found[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255  ##@@ 영역 등록
#     #                 #centers[i] = [pt[0] + w//2, pt[1] + h//2]
#     #                 centers.append([pt[0] + w//2 + offset[0], pt[1] + h//2 + offset[1]])
#     #                 #last = pt[0]
#     #                 #i += 1
#     #                 print('pt: {}, '.format(pt))
#     #                 cv2.rectangle(img_original, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 2)

#     #         if show == True:
#     #             #cv2.imshow('find images', img_original)
#     #             #cv2.waitKey(0)
#     #             #cv2.destroyAllWindows()
#     #             imgplot = plt.imshow(img_original)
#     #             plt.show()

#     #         return centers


#     # ##@@-------------------------------------------------------------------------
#     # ##@@ Feature Image Functions(이미지 비교: 방향, 크기 무시)

#     # def feature_image_box(template, image, precision=0.7, inverse=True):
#     #     """
#     #     Brief:
#     #         - 매칭 되는 이미지(>precision) 중앙 좌표 반환, 없으면 False
#     #         - feature_image_box -> find_feature_image_box + set_cv_image
#     #     Args:
#     #         template (str: image file path / list: screen image area):
#     #         offset (list) : 중앙 좌표 (이동)보정
#     #         image (str: image file path / list: screen image area):
#     #         mask: 마스크 이미지
#     #         precision: 이미지 유사도(default: 0.7)
#     #         method: 이미지 매칭 방법
#     #     Returns:
#     #         center (list) : center of box[x1, y1]
#     #     """
#     #     origin = [0, 0]    ## 기준 좌표

#     #     img = set_cv_image(image)
#     #     tpl = set_cv_image(template, 'GRAY')

#     #     if type(image) is list: ## scren selected box
#     #         origin = [image[0], image[1]]    ## 기준 좌표

#     #     if type(template) is list: ## scren selected box
#     #         tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)

#     #     return find_feature_image_box(tpl, img, origin, precision, inverse)


#     # def find_feature_image_box(template, image=None, origin=[0, 0], precision=0.7, inverse=True):
#     #     """
#     #     Brief:
#     #         - 매칭 되는 이미지(>precision) 중앙 좌표 반환, 없으면 False
#     #     Args:
#     #         template (str: image file path / list: screen image area):
#     #         offset (list) : 중앙 좌표 (이동)보정
#     #         image (str: image file path / list: screen image area):
#     #         mask: 마스크 이미지
#     #         precision: 이미지 유사도(default: 0.7)
#     #         method: 이미지 매칭 방법
#     #     Returns:
#     #         center (list) : center of box[x1, y1]
#     #     """

#     #     if inverse == True:
#     #         template = ~template            # queryImage 색깔 반전!!!

#     #     # Initiate SIFT detector
#     #     #sift = cv2.SIFT_create()
#     #     sift = cv2.xfeatures2d.SIFT_create()
#     #     # find the keypoints and descriptors with SIFT
#     #     kp1, des1 = sift.detectAndCompute(template, None)
#     #     kp2, des2 = sift.detectAndCompute(image, None)
#     #     # FLANN parameters
#     #     FLANN_INDEX_KDTREE = 1
#     #     index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#     #     search_params = dict(checks=50)     # or pass empty dictionary
#     #     flann = cv2.FlannBasedMatcher(index_params,search_params)
#     #     matches = flann.knnMatch(des1, des2, k=2)

#     #     points_x = []
#     #     points_y = []
#     #     print('matches size: {}'.format(len(matches)))

#     #     # ratio test as per Lowe's paper
#     #     for i, (m, n) in enumerate(matches):

#     #         if m.distance < precision*n.distance:

#     #             points_x.append(kp2[m.trainIdx].pt[0] + origin[0])
#     #             points_y.append(kp2[m.trainIdx].pt[1] + origin[1])
#     #             print('orign_x: {}, orign_y: {}'.format(origin[0], origin[1]))
#     #             print('matching points: {}'.format(kp2[m.trainIdx].pt))    ###### matching points

#     #     # Not Found Feature
#     #     if points_x == []:
#     #         return False

#     #     center = [(min(points_x) + max(points_x))//2, (min(points_y) + max(points_y))//2]
#     #     #print('center: {}'.format(center))
#     #     #print('-------------------------------')
#     #     return center


#     # def wait_match_image(template, image=None, precision=0.978, pause=3, duration=15):
#     #     time.sleep(pause)
#     #     center = match_image_box(template, image=image, precision=precision)
#     #     _ITV_MATCH_IMAGE = 0.5
#     #     if duration == 0:
#     #         return center
#     #     else:
#     #         #n = duration // _ITV_MATCH_IMAGE
#     #         for _ in range(0, duration):
#     #             center = match_image_box(template, image=image, precision=precision)
#     #             if center == False:
#     #                 time.sleep(_ITV_MATCH_IMAGE)
#     #             else:
#     #                 return center
#     #     return False


if __name__ == '__main__':
    box = set_viewbox(box=None)
    print(box)