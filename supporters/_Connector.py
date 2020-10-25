import os, sys
import json
import platform, ctypes

sys.path.append(os.path.join(os.path.dirname(__file__), './functions'))
from guiFns import *
from imageFns import *
from functions.dataFns import file_to_json

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '_config'))
from settings import _ENV, _IMGS, _MAP


uis = file_to_json('../_config/json/uis.json')
config = file_to_json('../_config/json/config.json')
characters = file_to_json('../_config/json/characters.json')

_CENTER = [config['MAX_X']//2, config['MAX_Y']//2]


def is_connected():
    if match_image_box(template, image=[]):
        pass


def img_path(prefix, where='UIS'):
    return _IMGS[where] + prefix + _ENV['IMG_EXT']


def charcter_info(nick, what='sn'):
    for character in characters:
        if character['nick'] in nick:
            return character[what]
    return None


def full_screen():
    win = match_image_box(template=img_path('img_ldplayer_settings'), image=expand_box(uis['img_ldplayer_settings'], offset=[10]))
    if type(win) == list:
        key_press('f11')


def clear_network_error():
    button = img_path('btn_disconnect_timeout_confirm')
    area = expand_box(uis['btn_disconnect_timeout_confirm'], offset=[10])
    target = {
        'tpl': img_path('btn_Main_Menu'),
        'img': expand_box(uis['btn_Main_Menu'], offset=[10])
    }
    full_screen()  ## 엘디플레이어를 full screen으로
    mouse_click_match_not(template=button, image=area, target=target)


class Connector:
    def __init__(self):
        # ROK 접속
        self.connect()
        # OS, 해상도, 계정, 캐릭터, ...
        # self.state = 'OFF' # connect state('OFF', 'VERIFICATION', 'DISCONNECTED', 'ADWARE', 'OVERLAPPED', 'GOOD')
        self.OS = self.set_OS() # Windows, Darwin(OSX), Linux, ...
        self.resolution = self.set_resolution() # [1920, 1080]
        self.emulator = 'LDPLAYER' # LDPLAYER, BLUESTACK, 
        self.nick = self.set_nick() # 게임 닉네임
        self.account = self.set_account() # deverlife@gmail.com, mowater@gmail.com, ...
        self.id = self.set_id() #  게임 아이디 '33627943'
        self.sn = self.set_sn() #  캐릭터 일련번호 'M000', 'M001', ...

        # print('OS: {}, resolution: {}, emulator: {}'.format(self.OS, self.resolution, self.emulator))
        # print('nick: {}, account: {}, sn: {}'.format(self.nick, self.account, self.sn))
 
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
        """
        기능: 
            - 캐릭터 닉네임을 확인하고, self.nick값에 입력
            - 자신의 도시를 클릭한 후, addMarker 창에서 복사함
        Note:
            - 임원의 경우 인터페이스가 다름!!!
            - 자신의 도시가 지도의 중앙에 나오도록 조정한 후에 해야 함!!!
        """
        self.go_home_city()
        self.set_view_mode(mode='AllianceView')

        series = [
            {'position':_CENTER, 'interval':2},
            {'position': center_from_box(uis['btn_object_click_cityHall_marker']), 'interval':3},
        ]

        mouse_click_series(series=series)

        staff = match_image_box(template=img_path('tab_addMarker_staff'), image=expand_box(uis['tab_addMarker_staff'], offset=[10]))
        # mouse_click_match(template=img_path('btn_Player_stop_confirm'), image=expand_box(uis['btn_Player_stop_confirm'], offset=[10]), precision=0.99)
        if not staff:
            series = [
                {'position': center_from_box(uis['txt_addMarker_Nick']), 'interval':2}
            ]
        else:
            series = [
                {'position': center_from_box(uis['tab_addMarker_general']), 'interval':3},
                {'position': center_from_box(uis['txt_addMarker_Nick']), 'interval':2}
            ]

        mouse_click_series(series=series)
        time.sleep(3)
        # input = center_from_box(uis['inp_addMarker_Nick'])
        nick = get_clipboard_copy(config['addMarker_start'], config['addMarker_end'], center_from_box(uis['btn_addMarker_copy']), center_from_box(uis['btn_addMarker_selectAll']))  # [760X]ぐ천년왕국ブ 와 같이 연맹 이름이 포함됨
        # print('nick is {}'.format(nick))
        series = [
            {'position':uis['btn_addMarker_OK'], 'interval': 2},
            {'position': uis['btn_addMarker_CLOSE'], 'interval': 2}
        ]
        mouse_click_series(series=series)
        return nick


    def set_sn(self):
        charcter_info(nick=self.nick, what='sn')

    def set_id(self):
        charcter_info(nick=self.nick, what='id')

    def set_account(self):
        charcter_info(nick=self.nick, what='google')

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

    def get_sn(self):
        return self.id

    def connect(self):
        """
        기능: 
            - 연결 상태, 접속 에러 등을 확인하고, ROK 접속
            - (quicklaunch bar에 있는) LDPLAYER를 켜고, (플레이어 바탕화면에 있는) ROK를 실행시키고, 풀스크린으로 만든 후, 게임 로딩이 완성되면, 메뉴 버튼(우측 하단)을 누름
        Note:
            - 로딩 도중 네트워크 에러 처리 필요
            - action의 첫 클릭시 네트워크 에러 처리 필요
        """
        # 퀵런치 바에 LDPlayer 아이콘이 활성화 되어 있지 않았다면, 에뮬레이터(ldplayer) 실행(OFF -> ON)
        conn1 = mouse_click_match(template=img_path('btn_OS_Player_inactive'), image=uis['box_OS_Quickloanch'], precision=0.999)

        # ROK app이 (강제) 중지된 상태가 확인되면, 확인 버튼 누름(STOPPED)
        conn2 = mouse_click_match(template=img_path('btn_Player_stop_confirm'), image=expand_box(uis['btn_Player_stop_confirm'], offset=[10]), precision=0.99)

        # 다른 기기 로그인으로 인한 중지
        conn3 = mouse_click_match(template=img_path('btn_disconnect_otherDevice_confirm'), image=expand_box(uis['btn_disconnect_otherDevice_confirm'], offset=[10]), precision=0.99)

        # 광고 팝업이 있으면 닫음(ADWIN/ADPOP)
        mouse_click_match(template=img_path('btn_ldplayer_adwin_CLOSE'), image=expand_box(uis['btn_ldplayer_adwin_CLOSE'], offset=[10]), precision=0.98)
        mouse_click_match(template=img_path('btn_ldplayer_adpop_CLOSE'), image=expand_box(uis['btn_ldplayer_adpop_CLOSE'], offset=[10]), precision=0.98)

        # ROK app 실행(OUT)
        if conn1 or conn2 or conn3:
            mouse_click_match_wait(template=img_path('btn_Player_ROK-mid'), image=expand_box(uis['btn_Player_ROK-mid'], offset=[10]), precision=0.99, pause=10)
            key_press('f11')
            self.set_menu_wait()
            # mouse_click_match_wait(template=img_path('btn_Main_Menu'), image=expand_box(uis['btn_Main_Menu'], offset=[20]), precision=0.99, pause=20, repeat=30)
            # 표준 veiw_mode, menu_mode 로 변경

        # 네트워크 불량으로 인한 접속 타임아웃
        # conn4 = mouse_click_match(template=img_path('btn_disconnect_timeout_confirm'), image=expand_box(uis['btn_disconnect_timeout_confirm'], offset=[10]), precision=0.99)
        # if conn4:
        #     self.set_menu_wait()

        clear_network_error()

        # ROK 인증이 필요한 경우(VERIFICATION)
        self.catch_verification()


    def go_home_city(self):
        """
        기능: 
            - 맵 중앙 위치를 자신의 city로 변경
        Note:
            - 
        """
        city_view = match_image_box(template=img_path('btn_Main_GoAllianceView'), image=expand_box(uis['btn_Main_GoAllianceView'], offset=[10]), precision=0.99)
        if type(city_view) == list:
            mouse_click(position=uis['btn_Main_GoAllianceView'])
            time.sleep(0.5)
            mouse_click(position=uis['btn_Main_GoAllianceView'])
        else:
            mouse_click(position=uis['btn_Main_GoAllianceView'])


    def set_view_mode(self, mode='AllianceView'):
        """
        기능: 
            - view mode를 맞춤 ('CityView': 도시뷰, 'AllianceView': 연맹뷰, 'WorldView': 월드뷰)
        Note:
            - 
        """
        city_view = match_image_box(template=img_path('btn_Main_GoAllianceView'), image=expand_box(uis['btn_Main_GoAllianceView'], offset=[10]), precision=0.99)
        world_view = match_image_box(template=img_path('btn_Main_WorldView'), image=expand_box(uis['btn_Main_WorldView'], offset=[10]), precision=0.99)
        if mode == 'CityView':
            if not city_view:
                mouse_click(position=uis['btn_Main_GoAllianceView'])
        elif mode == 'AllianceView':
            if type(city_view) == list:
                mouse_click(position=uis['btn_Main_GoAllianceView'])
            elif type(world_view) == list:
                mouse_click(position=uis['btn_Main_GoAllianceView'])
                time.sleep(1)
                mouse_click(position=uis['btn_Main_GoAllianceView'])


    def set_menu_mode(self, mode='unfold'):
        """
        기능: 
            - menu mode를 맞춤 ('unfold': 메뉴 펼치기, 'fold': 메뉴 감추기)
        Note:
            - 
        """
        menu_alliance = match_image_box(template=img_path('btn_menu_alliance'), image=expand_box(uis['btn_menu_alliance'], offset=[10]), precision=0.99)
        if mode == 'unfold':
            if not menu_alliance:
                mouse_click(position=uis['btn_Main_Menu'])
        else:
            if type(menu_alliance) is list:
                mouse_click(position=uis['btn_Main_Menu'])

    def set_menu_wait(self):
        """
        기능: 
            - ROK가 로딩된 후 menu mode를 'unfold'(메뉴 펼치기)로 설정 <- 게임 로딩 확인
        Note:
            - 
        """
        mouse_click_match_wait(template=img_path('btn_Main_Menu'), image=expand_box(uis['btn_Main_Menu'], offset=[20]), precision=0.99, pause=20, repeat=30)


    def set_view_menu(self):
        self.set_view_mode()
        self.set_menu_mode()


    def goto_account(self, account):
        if self.account != account:
            series = [
                {'position':uis['btn_Main_Profile'], 'interval': 2},
                {'position': uis['btn_profile_settings'], 'interval': 2},
                {'position':uis['btn_profile_settings_account'], 'interval': 2},
                {'position': uis['btn_accountSetting_switchAccount'], 'interval': 2},
            ]
            mouse_click_series(series=series)

            mouse_click_match(template=img_path('btn_accountSetting_switchAccount_google', where='CHARACTERS'), image=expand_box(uis['btn_accountSetting_switchAccount_google'], offset=[50, 200]))
            time.sleep(2)
            mouse_click_match(template=img_path('btn_accountSetting_switchAccount_google_' + account, where='CHARACTERS'), image=expand_box(uis['btn_accountSetting_switchAccount_google_' + account], offset=[50, 200]))

        print('goto account: {}'.format(account))
        time.sleep(10)
        self.connect()

    def goto_sn(self, sn):
        ## Note: nick이 다른 account에 있는 경우!!! -> self.goto_account
        # account = charcter_info(nick=nick, what='google')
        # if self.account != account:
        #     self.goto_account(account)
        #     # self.goto_nick()

        if self.sn != sn:
            series = [
                {'position':uis['btn_Main_Profile'], 'interval': 2},
                {'position': uis['btn_profile_settings'], 'interval': 2},
                {'position':uis['btn_profile_settings_characterMangement'], 'interval': 20},
            ]
            mouse_click_series(series=series)
            sn = 'img_avatar_login_' +  sn

            ## Note: 드래그 하면서 확인 필요!!!
            mouse_click_match(template=img_path(sn, where='CHARACTERS'), image=uis['box_characterMangement'])
            time.sleep(2)

            mouse_click(uis['btn_characterMangement_login_YES'])

        time.sleep(10)
        self.connect()


    def goto_nick(self, nick):
        if self.nick != nick:
            self.goto_sn(charcter_info(nick=nick, what='sn'))


    def catch_verification(self):
        btn_alert = match_image_box(template=img_path('btn_verification_alert'), image=expand_box(uis['btn_verification_alert'], offset=[20, 300]))

        if type(btn_alert) is list:
            mouse_click(btn_alert)
            time.sleep(2)

        btn_verify = match_image_box(template=img_path('btn_verification_verify'), image=expand_box(uis['btn_verification_verify'], offset=[100, 200]), precision=0.999)
        print('btn_verify: {}'.format(btn_verify))
        if type(btn_verify) is list:
            print('btn_verify: {}'.format(btn_verify))
            mouse_click(btn_verify)
            time.sleep(2)
            self.do_verification(attempts=0)
            return True
        
        # return False

    def find_verification_centers(self):
        templates = extract_templates(image=uis['box_Verification_Templates'])
        if len(templates) > 4: ## 템플릿 이미지가 4개를 초과하면, 포기
            return False

        centers = []
        for template in templates: ## 템플릿 이미지들과 유사한 이미지를, 이미지 영역에서 찾음
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


if __name__ == '__main__':
    time.sleep(5)
    conn = Connector()

    time.sleep(5)
    # conn.goto_account('life681225')
    # conn.goto_nick('millennium 202')
    # conn.goto_account('deverlife')

    # conn.catch_verification()
    # conn.set_nick()