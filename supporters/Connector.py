import os, sys
import json
import platform, ctypes

sys.path.append(os.path.join(os.path.dirname(__file__), './functions'))
from guiFns import ( mouse_click, mouse_click_series, mouse_click_match_not, mouse_click_match, key_press )
#expand_box, wait_match_image
from imageFns import *
from functions.dataFns import file_to_json

# sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '_config'))
# from settings import _ENV, _IMGS, _MAP

uis = file_to_json('../_config/json/uis.json')
config = file_to_json('../_config/json/config.json')
characters = file_to_json('../_config/json/characters.json')

_CENTER = [config['MAX_X']//2, config['MAX_Y']//2]


def img_path(prefix, where='UIS'):
    """
    기능: 
        - 이미지 경로(파일 이름 포함) 반환
    입력: 
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - prefix || 이미지 파일 이름 | str | None | 'btn_addMarker_OK'
        - where || 이미지 종류 | str | 'UIS' | ../_config/json/config.json'참조 / 'UIS': ui요소, 'CHARACTERS': 캐릭터, 'OBJECTS': 오브젝트
    출력:
        - 의미 | 데이터 타입 | 예시
        - 이미지 경로(파일 이름 포함) | str | '../_config/images/uis/btn_addMarker_OK.png'
    Note:
        - 이미지 종류 정리 필요
    """
    return config[where] + prefix + config['IMG_EXT']


def charcter_info(nick, what='sn'):
    """
    기능: 
        - 캐릭터 정보(sn, id, google) 반환
    입력: 
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - nick || 캐릭터 닉네임 | str | None | '[]천년왕국'
        - what || 정보 종류 | str | 'sn' | ../_config/json/characters.json'참조 / 'sn': 시리얼넘버, 'id': 아이디번호, 'google': 구글 계정('@gmail.com' 제외)
    출력:
        - 의미 | 데이터 타입 | 예시
        - 캐릭터 해당 정보 | str | 'M000'
    Note:
        - 시리얼넘버 정리 필요
    """
    for character in characters:
        if character['nick'] in nick:
            return character[what]
    return None


def full_screen():
    """
    기능: 
        - 에뮬레이터(ldplayer)를 전체 화면으로
    Note:
        - 기준 ui(ldplayer settings 버튼) 변경 or expand_box 사이즈 최적화 필요
    """
    win = match_image_box(template=img_path('img_ldplayer_settings'), image=expand_box(uis['img_ldplayer_settings'], offset=[200, 100]))
    if type(win) == list:
        key_press('f11')


def clear_network_error():
    """
    기능: 
        - 네트워크 에러 발생시 재로딩
    Note:
        - 네트워크 에러 상황 및 종류 확인
        - 재로딩 완료 확인 및 표준 매뉴.맵 크기 조정 필요!!
    """
    print('clear_network_error')
    button = img_path('btn_disconnect_timeout_confirm')
    area = expand_box(uis['btn_disconnect_timeout_confirm'], offset=[10])
    target = {
        'tpl': img_path('btn_Main_Menu'),
        'img': expand_box(uis['btn_Main_Menu'], offset=[10])
    }
    full_screen()  ## 엘디플레이어를 full screen으로
    mouse_click_match_not(template=button, image=area, target=target)


def get_resolution():
    """
    기능: 
        - 화면 해상도 출력
    출력:
        - 의미 | 데이터 타입 | 예시
        - 화면 해상도 | list | [1920, 1080]
    """
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return list(screensize)


def get_nick():
    """
    기능: 
        - 캐릭터 닉네임을 확인하고, nick값에 입력
        - 자신의 도시를 클릭한 후, addMarker 창에서 복사함
    출력:
        - 의미 | 데이터 타입 | 예시
        - 닉네임(연맹정보 포함) | str | 'Duke Plz 공작부탁드립니다 [760W]ぐ천년왕국ブ'
    Note:
        - 임원의 경우 인터페이스가 다름!!!
        - 자신의 도시가 지도의 중앙에 나오도록 조정한 후에 해야 함!!!
    """
    go_home_city()
    set_view_mode(mode='AllianceView')

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
    print('nick is {}'.format(nick))
    series = [
        {'position':uis['btn_addMarker_OK'], 'interval': 2},
        {'position': uis['btn_addMarker_CLOSE'], 'interval': 2}
    ]
    mouse_click_series(series=series)
    return nick


def get_sn(nick):
    """
    기능: 
        - 캐릭터 시리얼넘버(사용자 임의 지정 값) 반환
    입력: 
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - nick || 캐릭터 닉네임 | str | None | 'Duke Plz 공작부탁드립니다 [760W]ぐ천년왕국ブ' / get_nick() 참조
    출력:
        - 의미 | 데이터 타입 | 예시
        - 캐릭터 시리얼넘버 | str | 'M000'
    """
    charcter_info(nick=nick, what='sn')


def get_id(nick):
    """
    기능: 
        - 캐릭터 아이디(캐릭터 8자리 고유번호) 반환
    입력: 
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - nick || 캐릭터 닉네임 | str | None | 'Duke Plz 공작부탁드립니다 [760W]ぐ천년왕국ブ' / get_nick() 참조
    출력:
        - 의미 | 데이터 타입 | 예시
        - 캐릭터 아이디 | str | '33627943'
    """
    charcter_info(nick=nick, what='id')


def get_account(nick):
    """
    기능: 
        - 캐릭터 구글 계정 반환
    입력: 
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - nick || 캐릭터 닉네임 | str | None | 'Duke Plz 공작부탁드립니다 [760W]ぐ천년왕국ブ' / get_nick() 참조
    출력:
        - 의미 | 데이터 타입 | 예시
        - 캐릭터 구글 계정('@gmail.com' 제외) | str | 'deverlife'
    """
    charcter_info(nick=nick, what='google')


def turn_on_emulator():
    """
    기능: 
        - 퀵런치 바에 LDPlayer 아이콘이 활성화 되어 있지 않았다면, 에뮬레이터(ldplayer) 실행
    """
    return mouse_click_match(template=img_path('btn_OS_Player_inactive'), image=uis['box_OS_Quickloanch'], precision=0.999)


def restart_ROK(error_type='stop'):
    """
    기능: 
        - '중지(stop)', '다른 기기(otherDevice)' 등으로 접속이 끊긴 ROK 재실행
    Note:
        - '중지', '다른 기기' 외의 경우가 없는지 확인 필요!!
    """
    if error_type == 'stop':
        ui = 'btn_Player_stop_confirm'
    elif error_type == 'otherDevice':
        ui = 'btn_disconnect_otherDevice_confirm'
    return mouse_click_match(template=img_path(ui), image=expand_box(uis[ui], offset=[10]), precision=0.99)


def clear_ad_win(ui_covered, btn_close):
    """
    기능: 
        - 에뮬레이터 로딩시 생긴 광고창(중앙/우측) 닫기(가려진 ui가 있으면, '닫기'버튼 누름)
    Note:
        - 광고창 갯수 변화, 광고창 '닫기' 버튼 위치 등 확인 필요
    """
    template = img_path(ui_covered)
    image = expand_box(uis[ui_covered], offset=[10])
    if type(btn_close) == list:
        position = btn_close
    else:
        position = match_image_box(template=img_path(btn_close), image=expand_box(uis[btn_close], offset=[200, 100]))
    if not match_image_box(template=template, image=image):
        mouse_click(position=position)


def connect():
    """
    기능: 
        - 연결 상태, 접속 에러 등을 확인하고, ROK 접속
        - (quicklaunch bar에 있는) LDPLAYER를 켜고, (플레이어 바탕화면에 있는) ROK를 실행시키고, 풀스크린으로 만든 후, 게임 로딩이 완성되면, 메뉴 버튼(우측 하단)을 누름
    Note:
        - 로딩 도중 네트워크 에러 처리 필요
        - action의 첫 클릭시 네트워크 에러 처리 필요
    """
    turn_on_emulator()
    restart_ROK(error_type='stop')
    restart_ROK(error_type='otherDevice')

    # 에뮬레이터 켜짐 확인
    template = img_path('img_emulator_status_network')
    image = expand_box(uis['img_emulator_status_network'], offset=[100, 200])
    wait_match_image(template=template, image=image)

    # 광고창 닫기
    clear_ad_win(ui_covered='btn_Player_ROK-mid', btn_close='btn_emulator_adCenter_CLOSE')

    # ROK 앱 클릭
    mouse_click_match(template=img_path('btn_Player_ROK-mid'), image=expand_box(uis['btn_Player_ROK-mid'], offset=[10]), precision=0.99)

    # fullscreen
    full_screen()

    # ROK 인증이 필요한 경우(VERIFICATION)
    clear_verification()

    # 메뉴 unfold
    set_menu_wait()

    # 네트워크 에러 해결
    # clear_network_error()


def go_home_city():
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


def set_view_mode(mode='AllianceView'):
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


def set_menu_mode(mode='unfold'):
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


def set_menu_wait():
    """
    기능: 
        - ROK가 로딩된 후 menu mode를 'unfold'(메뉴 펼치기)로 설정 <- 게임 로딩 확인
    Note:
        - 
    """
    loaded = wait_match_image(template=img_path('btn_Main_GoAllianceView'), image=expand_box(uis['btn_Main_GoAllianceView'], offset=[20]), precision=0.99, pause=3, repeat=15, interval=1)
    if loaded:
        clear_ad_win(ui_covered='btn_Main_Menu', btn_close=uis['box_emulator_adSide1_CLOSE'])
    
    mouse_click_match(template=img_path('btn_Main_Menu'), image=expand_box(uis['btn_Main_Menu'], offset=[20]), precision=0.99)


def set_view_menu():
    set_view_mode()
    set_menu_mode()


def goto_account(account):
    # if account != account:
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
    connect()


def goto_sn(sn):
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
    connect()


def goto_nick(nick):
    if nick != nick:
        goto_sn(charcter_info(nick=nick, what='sn'))


def clear_verification():
    btn_alert = match_image_box(template=img_path('btn_verification_alert'), image=expand_box(uis['btn_verification_alert'], offset=[20, 300]))

    if type(btn_alert) is list:
        mouse_click(btn_alert)
        time.sleep(2)

    btn_verify = match_image_box(template=img_path('btn_verification_verify'), image=expand_box(uis['btn_verification_verify'], offset=[200, 100]), precision=0.99)
    print('btn_verify: {}'.format(btn_verify))
    if type(btn_verify) is list:
        print('btn_verify: {}'.format(btn_verify))
        mouse_click(btn_verify)
        time.sleep(2)
        do_verification(attempts=0)
        return True


def find_verification_centers():
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


def click_verifications(centers, attempts=0):
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


def do_verification(attempts=0):
    """
    기능: verification 퍼즐 해결
    Note:
        - 
    """
    centers = find_verification_centers()

    if not centers:
        mouse_click_match(template=img_path('btn_Verification_Refresh'), image=expand_box(uis['btn_Verification_Refresh'], offset=[20, 300]))
        time.sleep(3)
        do_verification(attempts=attempts)
    else:
        if attempts > 4:
            print("verification is not complete!!!")
            return False
        success = click_verifications(centers, attempts=attempts)
        # time.sleep(1)
        if not success:
            do_verification(attempts=attempts + 1)
        else:
            return True


if __name__ == '__main__':
    time.sleep(5)
    # connect()
    # get_nick()

    # goto_account('life681225')
    # goto_nick('millennium 202')
    # goto_account('deverlife')

    clear_verification()
    # get_nick()

    # full_screen()
    # set_view_mode(mode='CityView')