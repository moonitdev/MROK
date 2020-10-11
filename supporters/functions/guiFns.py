##@@@@========================================================================
##@@@@ Libraries

##@@@-------------------------------------------------------------------------
##@@@ Basic Libraries
import sys
import os
import time
import random
import math
import re

##@@@-------------------------------------------------------------------------
##@@@ Installed(conda/pip) Libraries
import pyautogui as pag
import pyperclip
import numpy as np
#import cv2

##@@@-------------------------------------------------------------------------
##@@@ User Libraries
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from imageFns import *


##@@@@========================================================================
##@@@@ Constants


##@@@-------------------------------------------------------------------------
##@@@ External(.json/.py)
sys.path.append(os.path.join(os.path.dirname(__file__), '../../_config'))
from settings import _ENV, _IMGS, _MAP
# from emulators import KEY_MAP as ui_key
# from emulators import OBJECTS as ui_obj
# from emulators import LOCATION_ROK_FULL as ui_xy
# from emulators import IMAGE_ROK_FULL as ui_img


_CENTER = [_ENV['MAX_X']//2,_ENV['MAX_Y']//2]


##@@@-------------------------------------------------------------------------
##@@@ 마우스 관련 함수
def mouse_move(position=[0, 0], duration=_ENV['DURATION_CLICK']):
    """
    기능: 해당 위치로 마우스를 이동함
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - position || 스크린 좌표 | list | [0, 0] | [247, 102]
        - duration || 마우스 이동 시간(초) | float | _ENV['MOUSE_DURATION']: 0.5
    Note:
        - 
    """
    pag.moveTo(position[0], position[1], duration)


def mouse_click(position=None, duration=_ENV['DURATION_CLICK'], clicks=1, interval=0.25):
    """
    기능: 해당 위치에서 마우스를 클릭함
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - position || 스크린 좌표 | list | None | [247, 102]
        - duration || 마우스 클릭 시간(초) | float | _ENV['MOUSE_DURATION']: 0.5
        - clicks || 마우스 클릭 횟수 | int | 1 | 2: 2번 클릭
        - interval || 마우스 클릭 간격(초) | float | 0.25 | 0.25 -> 0.25초 간격으로 마우스를 클릭
    출력:
        - 의미 | 데이터 타입 | 예시
        - 클릭한 마우스 위치 | list | [247, 102]
    """
    if position == None:
        pag.click(duration=duration, clicks=clicks, interval=interval)
    else:
        pag.moveTo(position[0], position[1], duration)
        time.sleep(random.uniform(0.0101, 0.0299))
        pag.mouseDown()
        time.sleep(random.uniform(0.0101, 0.0299))
        pag.mouseUp()


def mouse_press(position=None, duration=_ENV['DURATION_PRESS']):
    """
    기능: 해당 위치에서 마우스를 지속 시간만큼 눌렀다가(down) 뗌(up)
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - position || 스크린 좌표 | list | None | [247, 102]
        - duration || 마우스 다운 지속 시간(초) | float | _ENV['DURATION_DOWN']: 5
    """
    if type(position) is list:
        pag.moveTo(position[0], position[1])
    time.sleep(0.1)
    pag.mouseDown()
    time.sleep(duration)
    pag.mouseUp()


def mouse_click_box(box=[0, 0, 100, 100], duration=_ENV['DURATION_CLICK']):
    """
    기능: 해당 박스의 중앙 좌표에서 마우스를 클릭함
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - box || 스크린 영역 상자 | list | [0, 0, 100, 100] | [0, 0, 100, 100]
        - duration || 마우스 클릭 시간(초) | float | _ENV['MOUSE_DURATION']: 0.5
    출력:
        - 의미 | 데이터 타입 | 예시
        - 클릭한 마우스 위치 | list | [247, 102]
    """
    mouse_click(position=center_from_box(box), duration=duration)
    

def mouse_click_series(series=[{}]):
    """
    기능: series에 해당하는 마우스 연속 클릭
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - series || 마우스 클릭 배열 | list(of dict) | [{}] | {'pos':[0, 0], 'interval':1, 'callback':time.sleep, 'kwargs': {'a':'b'}},
            * pos : 마우스 클릭 위치(list)
            * interval : 클릭 후 멈춤 시간(float)
            * callback : 클릭 후 실행 함수(function)
            * kwargs : callback 함수의 매개 변수(dict)
    Note:
        - 
    """
    for one in series:
        mouse_click(one['pos'])
        if 'callback' in one:
            one['callback'](**one['kwargs'])
        time.sleep(one['interval'])


def mouse_click_series_box(series=[{}]):
    """
    기능: series에 해당하는 마우스 연속 클릭
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - series || 마우스 클릭 배열 | list(of dict) | [{}] | {'pos':[0, 0], 'interval':1, 'callback':time.sleep, 'kwargs': {'a':'b'}},
            * box : 마우스 클릭 위치(list)
            * interval : 클릭 후 멈춤 시간(float)
            * callback : 클릭 후 실행 함수(function)
            * kwargs : callback 함수의 매개 변수(dict)
    Note:
        - 
    """
    for one in series:
        mouse_click_box(one['box'])
        if 'callback' in one:
            # print(**one['kwargs'])
            one['callback'](**one['kwargs'])
        time.sleep(one['interval'])


def mouse_drag(start=[], end=[], duration=_ENV['DURATION_DRAG']):
    """
    기능: start에서 end까지 마우스 드래그
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - start || 드래그 시작 좌표 | list | [] | [300, 500]
        - end || 드래그 끝 좌표 | list | [] | [100, 900]
        - duration || 마우스 드래그 소요 시간(초) | float | _ENV['DURATION_DRAG']: 1.5
    Note:
        - 
    """
    pag.moveTo(start[0], start[1])
    pag.dragTo(end[0], end[1], duration=duration)


def mouse_scroll(start=[], scroll=-100):
    """
    기능: start에서 end까지 마우스 드래그
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - start || 드래그 시작 좌표 | list | [] | [300, 500]
        - scroll || 스크롤 거리? | int | 1 | -100 (100만큼 아래로 스크롤) / 200 (200만큼 위로 스크롤)
    Note:
        - scroll 최대 길이(스크롤 창 높이)
    """
    pag.moveTo(start[0], start[1])
    time.sleep(1)
    pag.scroll(scroll)


def mouse_click_match(template, image=None):
    """
    기능: image(스크린 영역)에 template과 일치하는 이미지가 있으면 그 중앙 좌표를 클릭
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - template || 템플릿 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]}
        - image || 원본 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
    Note:
        - 
    """
    center = match_image_box(template=template, image=image)
    if not center:
        print("not founded!!!")
        return False
    else:
        mouse_click(center)


def mouse_click_match_wait(template, image=None, precision=0.9, pause=10, duration=15, interval=2):
    """
    기능: image(스크린 영역)에 template과 일치하는 이미지가 있으면 그 중앙 좌표를 클릭(pause, duration, interval에 맞게 반복 찾기)
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - template || 템플릿 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]}
        - image || 원본 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
        - precision || 이미지 유사도 | float | 0.9 | 0 < precision <= 1
        - pause || 처음 멈춤 시간(초) | float | 3 | 3
        - duration || 반복 횟수 | int | 15 | 15
        - interval || 반복시 멈춤 시간(초) | float | 1 | 1
    Note:
        - 
    """
    center = wait_match_image(template=template, image=image, precision=precision, pause=pause, duration=duration, interval=interval)
    if not center:
        print("not founded!!!")
        return False
    else:
        mouse_click(center)


def mouse_click_match_scroll(template, image=None, start=[], scroll=-200, n=5):
    """
    기능: image(스크린 영역)에 template과 일치하는 이미지가 있을 때까지 스크롤 혹은 드래그 반복
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - template || 템플릿 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]}
        - image || 원본 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
        - start || 스크롤/드래그 시작 좌표 | list | [] | [300, 500]
        - scroll || 스크롤 거리 / 드래그 끝 좌표 | int / list | -200 | -100 (100만큼 아래로 스크롤), 200 (200만큼 위로 스크롤) // [300, 600] 드래그 끝 좌표
        - n : 스크롤 횟수 | int | 5 | 5 (5번 스크롤 시도)
    Note:
        - 
    """
    
    for _ in range(0, n):
        center = match_image_box(template=template, image=image)
        if not center:
            print('not found: {}'.format(_))
            if type(scroll) == int:
                mouse_scroll(start, scroll)
            else:
                mouse_drag(start, scroll)
                time.sleep(1)
                mouse_move(start)
            time.sleep(3)
            continue
        else:
            print('center: {}'.format(center))
            mouse_click(center)
            break


def mouse_click_match_drag(template, image=None, start=[], end=[], n=5):
    """
    기능: image(스크린 영역)에 template과 일치하는 이미지가 있을 때까지 드래그 반복
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - template || 템플릿 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]}
        - image || 원본 이미지 파일 경로(이름 포함), 스크린 이미지 영역(box) | None / str / list / dict | None | None: full screen / str: 파일 경로 / list: 이미지 영역 / dict : 파일 경로의 이미지의 지정 이미지 영역 {'path':path, 'box':[,,,]} 
        - start || 드래그 시작 좌표 | list | [] | [300, 500]
        - end || 드래그 끝 좌표 | list | [] | [300, 500]
        - n : 스크롤 횟수 | int | 5 | 5 (5번 드래그 시도)
    Note:
        - 
    """
    
    for _ in range(0, n):
        center = match_image_box(template=template, image=image)
        if not center:
            print('not found: {}'.format(_))
            mouse_drag(start, end)
            time.sleep(3)
            continue
        else:
            print('center: {}'.format(center))
            mouse_click(center)
            break


##@@@-------------------------------------------------------------------------
##@@@ 키보드 관련 함수

def key_press(key=None):
    """
    기능: 키를 누름
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - keys || 입력 문자 | str | None | 'enter'
    Note:
        - 
    """
    pag.press(key)


def key_hotkey(hotkey=()):
    """
    기능: 핫키(hotkey)을 입력
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - hotkey || 핫키 | tuple | () | ('ctrl', 'shift', 'esc')
    Note:
        - 
    """
    pag.hotkey(hotkey)


def key_input(position=[], keys=None):
    """
    기능: 해당 위치(position)에 커서(마우스)를 이동.클릭하고, 문자열(keys)을 입력
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - position || 문자열 입력 좌표 | list | [] | [300, 500]
        - keys || 입력 문자열 | str | None | 'abc'
    Note:
        - 
    """
    mouse_click(position=position)
    pag.typewrite(keys)


def zoom(mode='OUT', n=1, interval=0.1):
    """
    기능: 해당 위치(position)에 커서(마우스)를 이동.클릭하고, 문자열(keys)을 입력
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - position || 문자열 입력 좌표 | list | [] | [300, 500]
        - keys || 입력 문자열 | str | None | 'abc'
    Note:
        - 
    """
    if mode == 'OUT':
        for _ in range(0, n):
            key_press('f5')
            time.sleep(interval)
    else:
        for _ in range(0, n):
            key_press('f4')
            time.sleep(interval)

# def press_hotkey():
#     """
#     Brief: pressHotKey
#     Args:
#     """
#     pass

### callback 테스트용
def test(dt):
    print('keys: {}, vals:{}'.format(dt.keys(), dt.values()))


if __name__ == '__main__':
    # series = [
    #     {'pos':[100, 100], 'interval':5, 'callback':test, 'kwargs': {'a':'b'}},
    #     {'pos':[1000, 500], 'interval':1},
    #     {'pos':[300, 400], 'interval':1, 'callback':test, 'kwargs': {'c':'d', 'e':'f'}},
    # ]
    # mouse_click_series(series)
    time.sleep(5)
    # mouse_drag(start=[500, 200], end=[960, 540])
    # mouse_scroll(start=[960, 540], scroll=1)

    # zoom(mode='IN', n=20, interval=1)
    # template = 'C:\\Dev\\docMoon\\projects\\MROK\\_config\\images\\screenshots\\test\\scroll_quest1.png'
    # wh = [258, 380, 1428, 606]
    # scroll = -wh[3]
    # image = box_from_wh(wh)
    # start = center_from_box(image)

    # print('image: {}, start: {}, scroll: {}'.format(image, start, scroll))
    # mouse_click_match_scroll(template=template, image=image, start=start, scroll=scroll, n=5)

    # mouse_scroll(start=[960, 540], scroll=-500)

    # mouse_drag([960, 1028], [960, 330], duration=10)
    # mouse_drag([960, 1010], [960, 360], duration=2)

    mouse_drag([960, 984], [960, 380], duration=2)

# def scrollMouse():
#     """
#     Brief: scrollMouse(마우스 스크롤)
#     Args:
#     """
#     pass


# def press_keys():
#     """
#     Brief: pressKeys
#     Args:
#     """
#     pass


# def press_hotkey():
#     """
#     Brief: pressHotKey
#     Args:
#     """
#     pass

# def down_mouse(callback, position=[0, 0], duration=1):
#     """
#     Brief: down Mouse(마우스 다운 - 액션 - 업)
#     Args:
#         callback (func): callback function
#         button (str): mouse button of click
#         duration (int):
#     """
#     pag.moveTo(position[0], position[1])
#     pag.mouseDown()
#     time.sleep(duration)
#     callback()
#     pag.mouseUp()


# def delay(interval=_ENV['CLICK_INTERVAL'], rand=False):
#     """
#     Brief: delay intervals(sec)
#     Args:
#         interval (int): delay interval[sec].
#         rand (boolean): generate random time
#     Returns:
#     Note:
#         import time
#     """
#     if rand == True:
#         time.sleep(random.uniform(interval + 0.0101, interval+ 0.0299))
#     else:
#         time.sleep(interval)
#     return 0


# ## get, set
# def get_clipboard(position=[1002, 346]):
#     mouse_click(position)
#     print(pyperclip.paste())





# def get_screen_max():
#     pass


# def get_screen_center():
#     pass


# def get_window_max():
#     pass


# def get_window_center():
#     pass


# def set_perspective_matrix():
#     pass


# def compute_pixel_coord_ratio():
#     pass


# def compute_coord_unit_size():
#     pass


# def track_mouse():
#     """
#     Brief: Mouse Tracker for Unit Test@@@@
#     Args:
#     """
#     pass


# def drag_by_coord():
#     """
#     Brief: possible to move out of screen
#     Args:
#     """
#     pass


# def drag_by_object():
#     pass


# def move_by_object():
#     pass


# # def transform_perspective(points, trans='inverse'):
# #     if trans == 'inverse':
# #         M = np.matrix(_MAP['M_R2P'])
# #     else:
# #         M = np.matrix(_MAP['M_P2R'])

# #     if type(points) is list:  ## 1 point
# #         X = M.dot(np.array([points[0], points[1], 1]))
# #         X = np.asarray(X).reshape(-1)
# #         R = [round(X[0]/X[2]), round(X[1]/X[2])]
# #         print('R From One Point: {}'.format(R))
# #     elif type(points) is tuple:  ## multi points ((75, 148), (112, 100), (150, 75))
# #         R = cv2.perspectiveTransform(np.array([points], dtype=np.float32), M)
# #         print('R From Multi Points: {}'.format(R))
# #     return R


# def move_direction(zeroPoint=[_ENV['MAX_X']//2,_ENV['MAX_Y']//2], callback=None, direction=[1,0]):
#     #relPoint = [direction[0], direction[1]]
#     pag.moveTo(zeroPoint[0], zeroPoint[1], duration=0.0)
#     pag.mouseDown()
#     time.sleep(0.1)
#     pag.moveTo(zeroPoint[0] + direction[0], zeroPoint[1] + direction[1], duration=0.5)
#     time.sleep(0.1)
#     pag.mouseUp()
#     #pag.dragRel(relPoint[0], relPoint[1], duration=0.02, button='left')
#     time.sleep(1)
#     return direction
#     # # x_ratio = 6
#     # # y_ratio = 4.5
#     # x_ratio = 4.985
#     # y_ratio = 2.992
#     # print('x_ratio: {}, y_ratio: {}'.format(x_ratio, y_ratio))
#     # relPoint = [direction[0]*x_ratio, direction[1]*y_ratio]
#     # pag.moveTo(zeroPoint[0], zeroPoint[1], duration=0.0)
#     # pag.mouseDown()
#     # time.sleep(0.1)
#     # pag.moveTo(zeroPoint[0] + relPoint[0], zeroPoint[1] + relPoint[1], duration=0.5)
#     # time.sleep(0.1)
#     # pag.mouseUp()
#     # #pag.dragRel(relPoint[0], relPoint[1], duration=0.02, button='left')
#     # time.sleep(1)
#     # return relPoint


# def get_coords_for_rotation(step=100, count=9, zeroPoint=[_ENV['MAX_X']//2,_ENV['MAX_Y']//2]):
#     """
#     Brief: 시계방향 회전, 우측 이동 -> 
#     Args:
#         step (int): 이동 좌표 크기(minimum size map 기준)
#         count: 단위 이동 횟수(9 -> 360도)
#     Return:
#         coords : [coord1, coord2, ....]
#             coord: {'direction': 이동벡터(screen 기준), 'box': 작업 영역 사각형}
#     """

#     x_ratio = 5/0.73
#     y_ratio = 3/0.95

#     clockwise = [
#         [0, 0],
#         [-0.725, 0],
#         [0, -0.95],
#         [0.73, 0],
#         [0.73, 0],
#         [0, 1.353],
#         [0, 1.353],
#         [-0.726, 0],
#         [-0.726, 0],
#         #[0, -0.942],
#     ]

#     coords = []  # [{'direction':[,], 'box':[,,,]}, {'direction':[,], 'box':[,,,]}]
#     for i, unit in enumerate(clockwise):
#         direction = [int(unit[0]*step*x_ratio), int(unit[1]*step*y_ratio)]

#         w = int(0.73*step*x_ratio)
#         h = int(0.95*step*y_ratio)
#         box = get_box_from_center(zeroPoint, [w, h])
#         coord = {'direction':direction, 'box':box}
#         coords.append(coord)
    
#     return coords


# def test_rotation(start=[200, 200], step=100, count=9, zeroPoint=[_ENV['MAX_X']//2,_ENV['MAX_Y']//2]):
#     zoom_out()
#     coords = get_coords_for_rotation(step, count, zeroPoint)
#     go_by_coordinate(start)
#     i = 0

#     _ir.save_screenshot(path='../images/test/04/whole.png')

#     locations = []
#     for coord in coords:
#         center = get_coordinate()
#         if i > 0:
#             move_direction(zeroPoint, direction=coord['direction'])
        
#         ## find villages @@@@
#         #search_villages(location=[165, 131], box)
#         #if i < 9:

#         ## callback @@@@@@@@@@@@@@
#         # path='../images/test/04/' + str(i) + '.png'
#         # _ir.save_screenshot(box=coord['box'], path='../images/test/04/' + str(i) + '.png')
        
        
#         locations.append({'center':[center[1], center[2]], 'box':coord['box']})
#         i += 1

#         #locations.append({'center':center, 'box':coord['box']})
    
#     return locations



# def move_rotation(zeroPoint=[_ENV['MAX_X']//2,_ENV['MAX_Y']//2], step=1, count=1, callback=None, rotation='clockwise', angle=1):
#     """
#     Brief: 
#     Args:
#         step (int): size of coordinate when troops rotates
#         count (int): 
#         angle (int): 1 -> rotate 90 degree, 2 -> rotate 180 degree, 4 -> rotate 360 degree
#     """

#     x_ratio = 5/0.73
#     y_ratio = 3/0.95

#     clockwise = [
#         [0,0],
#         [-0.725, 0],
#         [0, -0.95],
#         [0.73, 0],
#         [0.73, 0],
#         [0, 1.353],
#         [0, 1.353],
#         [-0.726, 0],
#         [-0.726, 0],
#         [0, -0.942],
#     ]
#     box = get_box_from_center(zeroPoint, [step*3*x_ratio, step*3*y_ratio])
#     _ir.save_screenshot(box=box, path='../images/test/04/whole.png')


#     for i, unit in enumerate(clockwise):
#         direction = [unit[0]*step*x_ratio, unit[1]*step*y_ratio]

#         w = 0.73*step*x_ratio
#         h = 0.95*step*y_ratio
#         # if i > 5 and i < 9:
#         #     h = 1.353*step*y_ratio
#         box = get_box_from_center(zeroPoint, [w, h])

#         if i > 0:
#             move_direction(zeroPoint=zeroPoint, direction=direction)
#         time.sleep(2)
#         print(get_coordinate())
#         #_ir.save_screenshot(path='../images/test/04/' + str(i) + '.png')
#         if i < 9:
#             ### callback@@@@@@@@
#             ## callback
#             path='../images/test/04/' + str(i) + '.png'
#             callback(box, path)
#             #_ir.save_screenshot(box=box, path='../images/test/04/' + str(i) + '.png')


# def get_box_from_wh(wh):
#     """
#     Brief: get box from wh
#         - box coordinate([x1:left, y1:top, x2:right, y2:bottom])
#         - wh coordinate([x1, y1, w, h])
#     Args:
#         box (list): box coordinate
#     Returns:
#         wh (list): wh coordinate([x1, y1, w, h])
#     """
#     return [wh[0], wh[1], wh[0] + wh[2], wh[1] + wh[3]]


# def get_wh_from_box(box):
#     """
#     Brief: get wh coordinate([x1, y1, w, h]) from box coordinate([x1:left, y1:top, x2:right, y2:bottom])
#     Args:
#         wh (list): wh coordinate([x1, y1, w, h])
#     Returns:
#         box (list): box coordinate
#     """
#     return [box[0], box[1], box[2] - box[0], box[3] - box[1]]



# def get_center_from_box(box):
#     """
#     Brief: get box from wh
#         - box coordinate([x1:left, y1:top, x2:right, y2:bottom])
#         - wh coordinate([x1, y1, w, h])
#     Args:
#         box (list): box coordinate
#     Returns:
#         wh (list): wh coordinate([x1, y1, w, h])
#     """
#     return [(box[0] + box[2])//2, (box[1] + box[3])//2]


# def get_box_from_center(center, wh):
#     """
#     Brief: get box from wh
#         - box coordinate([x1:left, y1:top, x2:right, y2:bottom])
#         - wh coordinate([x1, y1, w, h])
#     Args:
#         box (list): box coordinate
#     Returns:
#         wh (list): wh coordinate([x1, y1, w, h])
#     """
#     return [center[0] - wh[0]//2, center[1] - wh[1]//2, center[0] + wh[0]//2, center[1] + wh[1]//2]

# ##@@@-------------------------------------------------------------------------
# ##@@@ simple GUI Functions(pyautogui:: mouse/keyboard) 



# ##@@@-------------------------------------------------------------------------
# ##@@@ complex GUI Functions(pyautogui:: mouse/keyboard)

# def get_image_path(name, category='UIS'):
#     return _PATH[category] + ui_img[name] + _ENV['IMG_EXT']


# def get_viewmode():
#     #cityview = _ir.get_center_match_image(get_image_path('btn_GoWorldView'), precision=0.9)
#     cityview = _ir.match_image_box(template=get_image_path('btn_GoWorldView'), image=[10, 902, 174, 1070], precision=0.95)
#     print('cityview: {}'.format(cityview))
#     if type(cityview) is list:
#         return 'CITY_VIEW'
#     else:
#         return 'WORLD_VIEW'


# def set_viewmode(mode='CITY_VIEW'):
#     if get_viewmode() != mode:
#         mouse_click(ui_xy['btn_GoWorldView'])


# def set_mode_explore():
#     chk_explore = _ir.match_image_box('../images/uis/chk_Explore.png', [10, 238, 60, 288], precision=0.99)
#     if type(chk_explore) is list:
#         print('already explore mode')
#     elif not chk_explore: 
#         mouse_click([36, 260])
#         print('click explore mode')


# def shot_zoom_out():
#     keys = ui_key[_ENV['OS']]['ZOOM_OUT']
#     pag.moveTo(_ENV['MAX_X']//2, _ENV['MAX_Y']//2)
#     for i in range(0, 34):
#         pag.keyDown(keys[0])
#         time.sleep(0.1)
#         pag.keyUp(keys[0])
#         time.sleep(1)
#         _ir.save_screenshot(path='../images/test/02/zoom_' + str(i) + '.png')
#         time.sleep(0.2)


# def zoom_out(nth=_ENV['ZOOM_MAX']):
#     pag.moveTo(_ENV['MAX_X']//2, _ENV['MAX_Y']//2)
#     keys = ui_key[_ENV['OS']]['ZOOM_OUT']
#     for _ in range(0, nth):
#         for key in keys:
#             pag.keyDown(key)
#             time.sleep(0.02)
#         for key in keys:
#             pag.keyUp(key)
#             time.sleep(0.01)
#     time.sleep(2)


# def drag_in_map(relPoint=[0, 0], zeroPoint=[_ENV['MAX_X']//2, _ENV['MAX_Y']//2], viewMode='CASTLE', duration=_ENV['MOUSE_DURATION']):
#     """
#     Brief: dragInMap(게임 내에서 마우스 드래그)
#     Args:
#         relPoint (list): target point(relative)
#         zeroPoint (list): starting point(relative)
#         viewMode (str): _CASTLE / _ALLIANCE / _KINGDOM
#         duration (int):
#     """
#     pag.moveTo(zeroPoint[0], zeroPoint[1], duration=0.0)
#     pag.dragRel(relPoint[0], relPoint[1], duration=0.2, button='left')



# def get_coordinate():
#     """
#     Brief: 지도에서 x, y 좌표를 입력하여 이동
#     Args:
#         location (list): 좌표
#         viewmode (str): CITY_VIEW / WORLD_VIEW(min -> GLOBE)
#     """
#     # @@@@@@@@@@@@@@@@@
#     if get_viewmode() is 'CITY_VIEW':
#         set_viewmode('WORLD_VIEW')

#     #_ir.filter_color(image, color='WHITE')
#     t = _ir.do_ocr([400, 16, 642, 46], 'eng', reverse=True)  # 전체
    
#     #t = '#10 2 175   X:2 97Y:104'
#     print(t)
#     ##@@@@@@@@@
#     s = ['i', 'I', 'l', 'o', 'O', ',', '/']
#     d = ['1', '1', '1', '0', '0', '', '7']
#     for i, v in enumerate(s):
#         #print('s: {}, d: {}'.format(s[i], d[i]))
#         t = t.replace(s[i], d[i])
#     t = re.sub(r'(\d) +(\d)', r'\1\2', t)
#     t = re.sub(r'(\d) +(\d)', r'\1\2', t)

#     t = re.sub(r'[a-zA-Z]', ' ', t)
#     t = re.sub(r'[^0-9,\. ]+', '', t)
#     t = re.sub(r' {2,}', ' ', t)

#     t = " ".join(t.strip().split())

#     arr = t.split(' ')

#     for i, a in enumerate(arr):
#         if len(a) > 4:
#             print(a)
#             arr[i] = a[len(a)-4:]

#     if len(arr) == 3:
#         return (int(arr[0]), int(arr[1]), int(arr[2]))
#     else:
#         return False
#     # s = _ir.do_ocr([418, 16, 484, 46], 'digits', reverse=True)  # server
#     # x = _ir.do_ocr([510, 16, 562, 46], 'digits', reverse=True)  # x
#     # y = _ir.do_ocr([588, 16, 640, 46], 'digits', reverse=True)  # y
#     #print('t: {}, s: {}, x: {}, y: {}'.format(t, s, x, y))



# def find_verification_verify():
#     # return _ir.match_image_box(get_image_path('btn_VerificationVerify', 'UIS'), precision=0.9)
#     return _ir.match_image_box(get_image_path('btn_VerificationVerify', 'UIS'), [830, 470, 1738, 648], precision=0.9)


# def do_verification_reward(precision=0.4):
#     template = [946, 220, 1180, 272]
#     image = [730, 280, 1190, 740]
#     img_btn_OK = [1024, 754, 1190, 812]

#     center_btn_OK = [1100, 786]
#     center_btn_close = [756, 782]

#     boxes = _ir.extract_templates(template)
#     print('boxes at gui.py: {}'.format(boxes))

#     if len(boxes) > 4 or boxes is False:
#         print('too many templates')
#         mouse_click(center_btn_close)
#         return False

#     centers = []
#     for box in boxes:
#         center = _ir.feature_image_box(box, image, precision, inverse=True)
#         if center is False:
#             print('no match image')
#             mouse_click(center_btn_close)
#             return False
#         centers.append(center)
    
#     print(centers)
#     for center in centers:
#         mouse_click(center)
#         delay(1)

#     mouse_click(center_btn_OK)

#     return centers


# def do_verification_rewards(precision=0.4, attempts=6):
#     btn_verify = find_verification_verify()
#     if btn_verify is False:
#         return 0
#     else:
#         mouse_click(btn_verify)
#         delay(5)

#     center_btn_OK = [1104, 784]
#     centers = do_verification_reward(precision)

#     tries = 0

#     if centers is False:
#         tries += 1
#         # print('no match image!')
#         # if tries > attempts:
#         #     do_verification_rewards()  ## 재시도@@@@@@@@@@

#         # mouse_click([800, 120])  ## 인증 팝업 바깥쪽을 누름@@@@@
#         delay(5)
#         do_verification_rewards(precision, attempts)

#     elif len(centers) > 4:
#         tries += 1
#         # print('too many templates!')
#         # if tries > attempts:
#         #     do_verification_rewards()  ## 재시도@@@@@@@@@@
#         # mouse_click([800, 120])  ## 인증 팝업 바깥쪽을 누름@@@@@
#         delay(5)
#         do_verification_rewards(precision)

#     delay(5)

#     if find_verification_verify() is False:
#         print(centers)
#         return centers
#     else:
#         do_verification_rewards(precision, attempts)


# def go_by_coordinate(location=[0,0]):
#     """
#     Brief: 지도에서 x, y 좌표를 입력하여 이동
#     Args:
#         location (list): 좌표
#         viewmode (str): CITY_VIEW / WORLD_VIEW(min -> GLOBE)
#     """
#     #set_viewmode(viewmode)

#     mouse_click(ui_xy['btn_LocationSearch'])  ## 좌표로 찾기 버튼
#     mouse_click(ui_xy['btn_Pop_LocationSearch_X'])  ## X 좌표 필드
#     mouse_click(ui_xy['npt_Pop_LocationSearch_Field'])  ## 텍스트 입력 필드
#     pag.typewrite(str(location[0]))

#     delay(1)

#     mouse_click(ui_xy['btn_Pop_LocationSearch_Y'])  ## Y 좌표 필드
#     mouse_click(ui_xy['btn_Pop_LocationSearch_Y'])  ## Y 좌표 필드
#     mouse_click(ui_xy['npt_Pop_LocationSearch_Field'])  ## 텍스트 입력 필드
#     pag.typewrite(str(location[1]))
#     delay(1)

#     mouse_click2(ui_xy['btn_Pop_LocationSearch_Go'])

#     delay(3)  ## 지도 데어터 읽을 시간을 주장!!!



# # def save_whole_maps(searchMode='Explore', zoom=320, max_size=_MAP['ONE_MAX']):
# #     """
# #     Brief: 지도 스크린샷 저장
# #     Args:
# #         searchMode (str): Alliance, Explore, Resources, Markers, Barbarian Stronghold
# #     """
# #     #set_fullscreen()
# #     #get_server_num()
# #     #set_searchmode()
# #     # _MAP : {
# #     #     'WHOLE': [1200, 1200],
# #     #     'ONE_MIN': [8, 6],
# #     #     'ONE_MAX': [320, 240],
# #     #     'EDGE': [210, 210, 1160, 940]
# #     # }
# #     server = '1621'

# #     ## edge 고려 안함
# #     # w = shotsize[0]
# #     # h = shotsize[1]
# #     # start = [w//2, h//2]
# #     box = _MAP['EDGE']
# #     ratio_x = _ENV['MAX_X'] / _MAP['ONE_MAX'][0]
# #     ratio_y = _ENV['MAX_Y'] / _MAP['ONE_MAX'][1]
# #     x1_ = math.floor(_MAP['EDGE'][0]/ratio_x)
# #     y1_ = math.floor(_MAP['EDGE'][1]/ratio_y)
# #     x2_ = math.floor((_ENV['MAX_X'] - _MAP['EDGE'][2])/ratio_x)
# #     y2_ = math.floor((_ENV['MAX_Y'] - _MAP['EDGE'][3])/ratio_y)
# #     w = _MAP['ONE_MAX'][0] - x2_ + x1_
# #     h = _MAP['ONE_MAX'][1] - y1_ + y2_
# #     # w = _MAP['ONE_MAX'][0] - x1_ - x2_
# #     # h = _MAP['ONE_MAX'][1] - y1_ - y2_
# #     start = [_MAP['ONE_MAX'][0]//2 - x1_, _MAP['ONE_MAX'][1]//2 - y2_]

# #     # w = (_MAP['EDGE'][2] - _MAP['EDGE'][0]) / ratio_x
# #     # h = (_MAP['EDGE'][3] - _MAP['EDGE'][1]) / ratio_y

# #     x_no = _MAP['WHOLE'][0]//w - 1
# #     y_no = _MAP['WHOLE'][1]//h - 3

# #     print('ratio_x: {}, ratio_y: {}'.format(ratio_x, ratio_y))
# #     print('w: {}, h: {}, x1_: {}, _x2: {}, _y1: {}, y2_: {}, start: {}'.format(w, h, x1_, x2_, y1_, y2_, start))
# #     print('x_no: {}, y_no: {}'.format(x_no, y_no))

# #     for j in range(0, y_no):
# #         for i in range(0, x_no):
# #             location = [start[0] + i*w, start[1] + j*h]
# #             #print(location)
# #             save_screenshot_map(location, searchMode, box, server)
# #             delay(1)

# #     return 0


# def save_whole_maps(searchMode='Explore', zoom=320, max_size=_MAP['ONE_MAX']):
#     """
#     Brief: 지도 스크린샷 저장
#     Args:
#         searchMode (str): Alliance, Explore, Resources, Markers, Barbarian Stronghold
#     """
#     server = '1621'

#     ## edge 고려 안함
#     # w = shotsize[0]
#     # h = shotsize[1]
#     # start = [w//2, h//2]
#     box = _MAP['EDGE']
#     ratio_x = _ENV['MAX_X'] / _MAP['ONE_MAX'][0]
#     ratio_y = _ENV['MAX_Y'] / _MAP['ONE_MAX'][1]
#     w = math.floor((_MAP['EDGE'][2] - _MAP['EDGE'][0])/ratio_x) + 37
#     h = math.floor((_MAP['EDGE'][3] - _MAP['EDGE'][1])/ratio_y)
#     start = [165, 131]

#     print('ratio_x: {}, ratio_y: {}'.format(ratio_x, ratio_y))
#     print('w: {}, h: {}, start: {}'.format(w, h, start))

#     for j in range(0, 2):
#         for i in range(0, 3):
#             location = [start[0] + i*w, start[1] + j*h]
#             #print(location)
#             save_screenshot_map(location, searchMode, box, server)
#             delay(1)

#     return 0


# def save_move_direction(zeroPoint=[_ENV['MAX_X']//2, _ENV['MAX_Y']//2], direction=[-10, 0]):
#     x_ = direction[0]
#     y_ = direction[1]
#     for i in range(1, 6):
#         path = _PATH['MAPS'] + 'move_' + str(direction[0]) + '_' + str(direction[1]) + _ENV['IMG_EXT']
#         delay(3)
#         _ir.save_screenshot(path=path)
#         direction[0] += x_
#         direction[1] += y_
#         move_direction(zeroPoint=zeroPoint, direction=[x_, y_])
#         time.sleep(1)


# def save_screenshot_map(location=[0, 0], searchMode='Explore', box=[], server=''):
#     go_by_coordinate(location)
#     #set_searchMode()
#     #set_zoomMode(zoom)
#     path = _PATH['MAPS'] + server + '_' + searchMode + '_' + str(location[0]) + '_' + str(location[1]) + _ENV['IMG_EXT']
#     delay(3)
#     _ir.save_screenshot(box, path)



# def receive_village_gifts(location=[_MAP['ONE_MAX'][0]//2, _MAP['ONE_MAX'][1]//2], max_i=2):
#     zoom_out()
#     #go_by_coordinate(location)
#     template = '../images/uis/img_ExploreVillage.png'  ##@@@@@@@@@@@@
#     #coord = get_coordinate()
#     set_mode_explore()

#     for _ in range(0, max_i):
#         start = time.time()  # 시작 시간 저장
#         center = _ir.wait_match_image(template, _MAP['EDGE'], precision=0.978, duration=15)
#         print("time :", time.time() - start)  ## 실행 속도 측정

#         if not center:
#             #coord = get_coordinate()
#             drag_in_map([-100, 0])
#             #receive_village_gifts()
#             continue

#         mouse_click(center)
#         print(center)
#         delay(0.1)
#         mouse_click2([_ENV['MAX_X']//2, _ENV['MAX_Y']//2])
#         delay(0.1)
#         mouse_click([_ENV['MAX_X']//2 - 200, _ENV['MAX_Y']//2])
#         delay(0.1)
#         zoom_out()
#         delay(0.01)


# def visit_village(coord={'loc': [1166, 682], 'center': [250, 250]}):
#     go_by_coordinate(coord['center'])
#     mouse_click(coord['loc'])
#     delay(0.1)
#     mouse_click2([_ENV['MAX_X']//2, _ENV['MAX_Y']//2])
#     delay(0.1)

#     great = _ir.match_image_box()

#     if type(great) is list:
#         mouse_click(great)
#         _coord = get_coordinate()
#         mouse_click([_ENV['MAX_X']//2 - 200, _ENV['MAX_Y']//2])
#         delay(0.1)
#         zoom_out()
#         delay(0.01)
#         return _coord

#     return False



# def find_village_location(coord={'loc': [1166, 682], 'center': [250, 250]}):
#     go_by_coordinate(coord['center'])
#     mouse_click(coord['loc'])
#     delay(0.1)
#     mouse_click2([_ENV['MAX_X']//2, _ENV['MAX_Y']//2])
#     delay(0.1)
#     _coord = get_coordinate()
#     return [_coord[1], _coord[2]]


# def search_objects_in_map(obj='village_unvisited', location=[500, 300], box=_MAP['SCAN_BOX'], precision=0.62, ms='min'):
#     #go_by_coordinate(location)
#     #time.sleep(3)

#     #yellow filter: cvScalar(23,41,133), cvScalar(40,150,255)
#     # yellow_lower = [20, 100, 100]
#     # yellow_upper = [30, 255, 255]
#     yellow_lower = [15, 70, 70]
#     yellow_upper = [28, 255, 255]
#     #template = '../images/uis/img_ExploreVillage.png'  ##@@@@@@@@@@@@
#     template = _PATH['OBJECTS'] + ui_obj[obj]['img_' + ms] + _ENV['IMG_EXT']
#     mask = None
#     if 'msk_' + ms in ui_obj[obj]:
#         mask = _PATH['OBJECTS'] + ui_obj[obj]['msk_' + ms] + _ENV['IMG_EXT']

#     return _ir.match_image_box(template=template, image=box, mask=mask, precision=precision, show=True, multi=1, color=(yellow_lower, yellow_upper))


# def search_villages(location, box):
#     go_by_coordinate(location)
#     template = '../images/uis/img_ExploreVillage.png'  ##@@@@@@@@@@@@

#     #return _ir.match_image_box(template=template, image=box, precision=0.97, show=True, multi=1)
#     return _ir.match_image_box(template=template, image=box, precision=0.97, multi=1)


# def explore_caves():
#     pass


# ##@@@@========================================================================
# ##@@@@ Execute Test
# if __name__ == "__main__":
#     delay(5)
#     #go_by_coordinate([500, 500])
#     #get_clipboard()
#     #drag_in_map([-_ENV['MAX_X']//2, _ENV['MAX_Y']//2])
#     #drag_in_map([_ENV['MAX_X']//2, 0])
#     # print(_ENV['MAX_X']//2)
#     # pag.moveTo(_ENV['MAX_X']//2, _ENV['MAX_Y']//2, duration=0.0)
#     # pag.dragRel(500, 400, duration=0.2, button='left')
#     # pass
#     #get_image_path('btn_GoWorldView')
#     #print(get_viewmode())
#     #zoom_out()
#     #save_screenshot_map()
#     #save_whole_maps()
#     #print(_ENV['MAX_X'] / _MAP['ONE_MAX'][0])
#     #print(_ENV['MAX_Y'] / _MAP['ONE_MAX'][1])
#     #'EDGE': [210, 150, 1610, 940]
#     #go_by_coordinate([125,89])
#     # delay(3)
#     # pag.moveTo(_MAP['EDGE'][2], _ENV['MAX_Y']//2)
#     # delay(0.1)
#     # pag.mouseDown()
#     # delay(0.3)
#     # pag.moveTo(_MAP['EDGE'][0], _ENV['MAX_Y']//2, duration=4.5)
#     # delay(0.3)
#     # pag.mouseUp()
#     #drag_in_map([_ENV['MAX_X']//2, 0])
    
    
#     #template = '../images/uis/img_ExploreVillage.png'
#     #image = '../images/maps/1621_Explore_125_89_.png'
#     #mask = '../images/uis/mask_ExploreVillage.png'
#     #template = '../images/uis/img_ExploreCave.png'
#     # image = '../images/maps/1621_Explore_125_89.png'
#     # mask = '../images/uis/mask_ExploreCave.png'
#     # template = '../images/target.png'
#     # image = '../images/image.png'
#     # mask = '../images/mask.png'
#     #centers = _ir.match_image_box(template, image, mask, precision=0.9983, show=True, multi=1)
#     #centers = _ir.match_image_box(template, image, precision=0.99, show=True, multi=1)
#     #centers = _ir.match_image_box(template, image, mask, precision=0.9983, show=True, multi=1)
#     #centers = _ir.match_image_box(template, image, precision=0.998, show=True, multi=1)

#     # for _ in range(0, 5):
#     #     center = _ir.match_image_box(template, precision=0.997)
#     #     delay(1)
#     #     mouse_click(center)
#     #     print(center)
#     #     delay(5)
#     #     mouse_click([-_ENV['MAX_X']//2, _ENV['MAX_Y']//2])
#     #     delay(1)
#     #     mouse_click([-_ENV['MAX_X']//2 - 200, _ENV['MAX_Y']//2])
#     #     for _ in range(0, 40):
#     #         pag.hotkey('ctrl', 'down')
#     #         delay(0.1)
#     #     delay(3)

#     #centers = _ir.match_image_box(template, _MAP['EDGE'], precision=0.97, show=True, multi=1)
#     # for _ in range(0, 100):
#     #     center = _ir.match_image_box(template, _MAP['EDGE'], precision=0.97)
#     #     if not center:
#     #         continue 
#     #     mouse_click(center)
#     #     print(center)
#     #     delay(3)
#     #     mouse_click2([_ENV['MAX_X']//2, _ENV['MAX_Y']//2])
#     #     delay(1)
#     #     mouse_click([_ENV['MAX_X']//2 - 200, _ENV['MAX_Y']//2])
#     #     delay(0.1)
#     #     zoom_out()
#     #     delay(0.01)

#     # mouse_click(find_verification_verify())
#     # delay(7)
#     #do_verification_reward(0.7)
#     #do_verification_rewards(0.7)
#     #receive_village_gifts([924, 212])
#     #get_coordinate()
#     #set_mode_explore()

#     #shot_zoom_out()

#     #save_whole_maps()
#     #search_villages()
#     #move_direction(direction=[100,0])
#     #save_move_direction([_ENV['MAX_X']-100, _ENV['MAX_Y']//2], [-300,0])
#     #save_move_direction(zeroPoint=[_ENV['MAX_X']//2, _ENV['MAX_Y']-100], direction=[0, -300])
#     #save_move_direction(zeroPoint=[_ENV['MAX_X']//2, _ENV['MAX_Y']//2], direction=[0, -100])

#     # move_rotation(step=100, callback=_ir.save_screenshot)

#     #move_direction(zeroPoint=[960, 540], direction=[-365.0, 0])
#     #transform_perspective([_ENV['MAX_X']//2, _ENV['MAX_Y']//2], trans='inverse')
#     #print(get_coordinate())
#     #coords = get_coords_for_rotation()
#     #print(coords)

#     #locations = test_rotation(start=[150, 150], step=100, count=9)
#     # for location in locations:
#     #     villages = search_villages(location=location['center'], box=location['box'])
#     #     if villages is list:
#     #         location['villages'] = villages
    
#     #search_villages(location=[250, 150], box=[710, 390, 1210, 690])
#     #print(locations)

#     # rotation_units = _MAP['R_UNITS']
#     # location = [150, 150]
#     # step = 100
#     # coords = []
#     # for unit in rotation_units:
#     #     location = [location[0] - step*unit[0], location[1] - step*unit[1]]
#     #     vs = search_villages(location=location, box=_MAP['SCAN_BOX'])
#     #     coord = {}
#     #     if type(vs) is list:
#     #         if len(vs) > 0:
#     #             print('founded  villages: {}'.format(vs))
#     #             coord['loc'] = vs
#     #             coord['center'] = location
#     #             coords.append(coord)
    
#     # print('founded all villages: {}'.format(coords))



#     # v_coords = [{'villages': [[1166, 682]], 'center': [250, 250]}, {'villages': [[785, 409]], 'center': [50, 250]}]

#     # for v in v_coords:
#     #     go_by_coordinate(v['center'])
#     #     for village in v['villages']:
#     #         mouse_click(village)
#     #         time.sleep(5)


#     # vs = search_objects_in_map(obj='village_unvisited', location=[250, 250], box=_MAP['SCAN_BOX'], precision=0.97, ms='min')

#     # print(vs)

#     #coord = find_village_location(coord={'loc': [1166, 682], 'center': [250, 250]})
#     #print(coord)

#     search_objects_in_map()