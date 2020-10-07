import os, sys
import rokgui
import imagePrcessor

def is_connected():

    if match_image_box(template, image=[]):

    pass



CITY_VIEW
KINGDOM_VIEW
WORLD_VIEW

class Connector:
    def __init__():
        # OS, 해상도, 계정, 캐릭터, ...
        self.state  # connect state('OFF', 'VERIFICATION', 'DISCONNECTED', 'ADWARE', 'OVERLAPPED', 'GOOD')
        self.OS  # win, osx, linux, ...
        self.resolution # [1920, 1080]
        self.emulator # LDPLAYER, BLUESTACK, 
        self.account # deverlife@gmail.com, mowater@gmail.com, ...
        self.nick # 
        self.id

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
        pass

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