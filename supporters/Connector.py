import os, sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), './functions'))
from guiFns import *
from imageFns import *

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '_config'))
from settings import _ENV, _IMGS, _MAP


with open('../_config/json/uis.json', encoding='UTF-8') as f:
    uis = json.load(f)
# with open('../_config/ui_boxes.json', encoding='UTF-8') as f:
#     vals = json.load(f)

def is_connected():
    if match_image_box(template, image=[]):
        pass


def img_path(prefix, where='UIS'):
    return _IMGS[where] + prefix + _ENV['IMG_EXT']

# CITY_VIEW
# KINGDOM_VIEW
# WORLD_VIEW

class Connector:
    def __init__(self):
        # OS, 해상도, 계정, 캐릭터, ...
        self.state = 'OFF' # connect state('OFF', 'VERIFICATION', 'DISCONNECTED', 'ADWARE', 'OVERLAPPED', 'GOOD')
        self.OS = 'win' # win, osx, linux, ...
        self.resolution = [1920, 1080] # [1920, 1080]
        self.emulator = 'LDPLAYER' # LDPLAYER, BLUESTACK, 
        self.account = 'deverlife@gmail.com' # deverlife@gmail.com, mowater@gmail.com, ...
        self.nick = '천년왕국' # 게임 닉네임
        self.id = '33627943'  # 게임 아이디

    def set_state(self):
        pass

    def set_OS(self):
        pass

    def set_resolution(self):
        pass

    def set_emulator(self):
        pass

    def set_account(self):
        pass

    def set_nick(self):
        pass

    def set_id(self):
        pass


    def get_state(self):
        return self.state

    def get_OS(self):
        return self.OS

    def get_resolution(self):
        return self.resolution

    def get_emulator(self):
        return self.emulator

    def get_account(self):
        return self.account

    def get_nick(self):
        return self.nick

    def get_id(self):
        return self.id


    def on_player(self):
        icon_player = match_image_box(template=img_path('btn_OS_Player'), image=uis['box_OS_Quickloanch'])
        mouse_click(icon_player)
        icon_rok = wait_match_image(template=img_path('btn_Player_ROK-mid'), image=uis['box_Player_Apps-mid'], pause=20)
        if not icon_rok:
            print('template image not founded: {}'.format(img_path('btn_Player_ROK-mid')))
            return False
        # if type(icon_rok) == list:
        time.sleep(1)
        mouse_click(icon_rok)
        key_press('f11')
        icon_map = wait_match_image(template=img_path('btn_Main_CityView'), image=expand_box(uis['btn_Main_CityView'], offset=[20]), pause=20, duration=30)
        if icon_rok:
            mouse_click(icon_map)
        # icon_player = match_image_box(template=uis['btn_OS_Player'], image=uis['box_OS_Quickloanch'])
        # mouse_click(icon_player)
        # icon_rok = wait_match_image(template=uis['btn_Player_ROK-mid'], image=uis['box_Player_Apps-mid'], pause=10)
        # if icon_rok:
        #     return False
        # # if type(icon_rok) == list:
        # time.sleep(1)
        # mouse_click(icon_rok)
        # key_press('f11')
        # icon_map = wait_match_image(template=uis['btn_Main_CityView'], image=expand_box(uis['btn_Main_CityView'], offset=[20]), pause=20)


    def on_rok(self):
        pass

    def login(self):
        pass

    def goto_account(self):
        pass

    def goto_nick(self):
        pass

    def verificate(self):
        pass

    def reconnect(self):
        pass





# def turnOnEmulator(emulator=_ENV['_EMULATOR']):
#     # 버튼
#     #_UI = emulators[emulator]['BUTTONS']

#     # For BLUESTACK
#     if emulator == 'BLUESTACK':
#         clickMouse(_UI['location']['icon_wallpaper'])
#         time.sleep(10)
#         clickMouse([1000, 500])

#     # For LDPLAYER
#     elif emulator == 'LDPLAYER':
#         # 바탕화면 더블 클릭
#         clickMouse2(_OS['ROK_WALLPAPER']['xy'])

#         ## popup 닫기 !!!!
#         ## 상단 메뉴바 아래 부분에서 '닫기' 버튼 있으면, 클릭!!!!
#         for btn in _UI['OUTER']['POPUP_CLOSES']:
#             time.sleep(1)
#             clickMouse(btn)

#         # ROK 아이콘 클릭
#         for _ in range(0, 15):
#             print('rok icon path: ' + _ENV['_IMAGES_FOLDER'] + _UI['OUTER']['WALLPAPER_ROK_MID']['fn'])
#             loaded = matchImageBox(_ENV['_IMAGES_FOLDER'] + _UI['OUTER']['WALLPAPER_ROK_MID']['fn'])
#             if loaded == False:
#                 time.sleep(10)
#             else:
#                 clickMouse(loaded)
#                 break

#         ## popup(avast) 닫기
#         clickMouse(_UI['OUTER']['POPUP_AVAST'])

#         # 최대화 버튼 클릭
#         time.sleep(2)
#         clickMouse(_UI['OUTER']['MENUBAR_MAX_MID']['xy'])

#         # 게임 화면 진입 여부 확인
#         for _ in range(0, 30):
#             loaded = matchImageBox(_ENV['_IMAGES_FOLDER'] + _UI['MAIN']['VIEWALLIANCE_MAX']['fn'])
#             if loaded == False:
#                 time.sleep(10)
#             else:
#                 print(loaded)
#                 break
        
#         ## 게임 화면 진입이 안된 경우 처리!!!
#         if loaded == False:
#             pass

#         time.sleep(2)
        
#         # 하단 메뉴 펼침
#         unfoldMenuBtn()
    
#     return 0


if __name__ == '__main__':
    conn = Connector()

    conn.on_player()