import os, sys
import json
import platform, ctypes

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
        self.OS = self.set_OS() # Windows, Darwin(OSX), Linux, ...
        self.resolution = self.set_resolution() # [1920, 1080]
        self.emulator = 'LDPLAYER' # LDPLAYER, BLUESTACK, 
        self.account = 'deverlife@gmail.com' # deverlife@gmail.com, mowater@gmail.com, ...
        self.nick = '천년왕국' # 게임 닉네임
        self.id = '33627943'  # 게임 아이디

    def set_state(self):
        pass

    def set_OS(self):
        return platform.system()

    def set_resolution(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return list(screensize)

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
        """
        기능: (quicklaunch bar에 있는) LDPLAYER를 켜고, (플레이어 바탕화면에 있는) ROK를 실행시키고, 풀스크린으로 만든 후, 게임 로딩이 완성되면, 메뉴 버튼(우측 하단)을 누름
        Note:
            - 
        """
        mouse_click_match(template=img_path('btn_OS_Player'), image=uis['box_OS_Quickloanch'])
        mouse_click_match_wait(template=img_path('btn_Player_ROK-mid'), image=expand_box(uis['btn_Player_ROK-mid'], offset=[10]), precision=0.99, pause=10)
        key_press('f11')
        mouse_click_match_wait(template=img_path('btn_Main_Menu'), image=expand_box(uis['btn_Main_Menu'], offset=[20]), precision=0.99, pause=20, duration=30)


    def on_rok(self):
        pass

    def login(self):
        pass

    def goto_account(self):
        pass

    def goto_nick(self):
        pass

    def catch_verification(self):
        btn_alert = match_image_box(template=img_path('btn_Verification_Alert'), image=expand_box(uis['btn_Verification_Alert'], offset=[20, 300]))

        if type(btn_alert) is list:
            mouse_click(btn_alert)
            time.sleep(2)
            self.do_verification(attempts=0)
            return True
        
        lbl_rewards = match_image_box(template=img_path('lbl_Verification_Rewards'), image=expand_box(uis['lbl_Verification_Rewards'], offset=[20, 300]))
        if type(lbl_rewards) is list:
            mouse_click(lbl_rewards)
            time.sleep(2)
            self.do_verification(attempts=0)
            return True
        
        return False


    def find_verification_centers(self):
        templates = extract_templates(image=uis['box_Verification_Templates'])

        centers = []
        for template in templates:
            center = feature_image_box(template=template, image=uis['box_Verification_Image'], precision=0.7, inverse=True)
            if center is False:
                return False
            centers.append(center)

        return centers


    def click_verifications(self, centers, attempts=0):
        for center in centers:
            mouse_click(center)
        mouse_click_match(template=img_path('btn_Verification_OK'), image=expand_box(uis['btn_Verification_OK'], offset=[20, 300]))
        print(centers)
        time.sleep(1)
        btn_OK = match_image_box(template=img_path('btn_Verification_OK'), image=expand_box(uis['btn_Verification_OK'], offset=[20, 300]))
        if not btn_OK:
            return True
        else:
            return False


    def do_verification(self, attempts=0):
        """
        기능: verification 퍼즐 해결
        Note:
            - 
        """
        # box_Verification_Templates
        # box_Verification_Image
        # btn_Verification_OK
        # btn_Verification_Close
        # btn_Verification_Refresh
        centers = self.find_verification_centers()

        if not centers:
            mouse_click_match(template=img_path('btn_Verification_Refresh'), image=expand_box(uis['btn_Verification_Refresh'], offset=[20, 300]))
            time.sleep(3)
            self.do_verification(attempts=attempts)
        else:
            if attempts > 4:
                print("verification is not complete!!!")
                return False
            success = self.click_verifications(centers, attempts=attempts)
            # time.sleep(1)
            if not success:
                self.do_verification(attempts=attempts + 1)
            else:
                return True


    def reconnect(self):
        pass


if __name__ == '__main__':
    conn = Connector()
    # conn.on_player()

    time.sleep(5)

    conn.do_verification()