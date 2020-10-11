##@@@-------------------------------------------------------------------------
##@@@ Basic Libraries
import os, sys
# import re
import time
# import numpy as np

# ##@@@-------------------------------------------------------------------------
# ##@@@ Installed(conda/pip) Libraries
# import pyautogui as pag
# import cv2
# import pytesseract


##@@@-------------------------------------------------------------------------
##@@@ External(.json/.py)
# sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '_config'))
# from settings import _ENV, _IMGS, _MAP
sys.path.append(os.path.join(os.path.dirname(__file__), '../supporters'))
# from databaser.GoogleSpread import GoogleSpread
from functions.imageFns import *
from functions.guiFns import *
from functions.dataFns import file_to_json

uis = file_to_json('../_config/json/uis.json')
config = file_to_json('../_config/json/config.json')
characters = file_to_json('../_config/json/characters.json')

characters_image = config['CHARACTERS']


def set_img_path(name, category='UIS'):
    return config[category] + name + config['IMG_EXT']


def login(nick='millennium 102'):
    series = [
        {'box': uis['btn_Main_Profile'], 'interval': 2},
        {'box': uis['btn_profile_settings'], 'interval': 2},
        {'box': uis['btn_profile_settings_characterMangement'], 'interval': 2},
    ]
    mouse_click_series_box(series=series)

    path = ''
    print("nick: {}".format(nick))
    for character in characters:
        print("character['nick']: {}".format(character['nick']))
        if character['nick'] == nick:
            path = config['CHARACTERS'] + config['login_prefix'] + character['sn'] + config['IMG_EXT']
            print(path)
            break
    box = uis['box_characterMangement']
    print(box)
    mouse_click_match_scroll(template=path, image=uis['box_characterMangement'], scroll=-(box[3]-box[1]))
    time.sleep(1)
    
    mouse_click_box(uis['btn_characterMangement_login_YES'])


def claim_VIP():
    """
    기능: 매일 주어지는 VIP point/chest gift 수령
    """
    series = [
        {'box': uis['btn_Main_VIP'], 'interval': 2},
        {'box': uis['btn_profile_VIP_pointsChest'], 'interval': 4, 'callback':mouse_click, 'kwargs':{'position':None, 'clicks':4, 'interval':0.5}},
        {'box': uis['btn_profile_VIP_pointsClaim'], 'interval': 4, 'callback':mouse_click, 'kwargs':{'position':None, 'clicks':4, 'interval':0.5}},
        {'box': uis['btn_profile_VIP_CLOSE'], 'interval': 1}
    ]
    mouse_click_series_box(series=series)


def claim_gifts():
    """
    기능: 연맹 선물 수령
    """
    series = [
        {'box': uis['btn_menu_alliance'], 'interval': 2},
        {'box': uis['btn_menu_alliance_gifts'], 'interval': 2},
        {'box': uis['tab_menu_alliance_gifts_rare'], 'interval': 3},
    ]
    mouse_click_series_box(series=series)

    ## rare 선물 claim 누르기
    for _ in range(0, 50):
        image_box = expand_box(box=uis['box_menu_alliance_gifts_claim4'], offset=[20, 10])
        claim = match_image_box(template=set_img_path('btn_menu_alliance_gifts_claim'), image=image_box)
        if type(claim) is list:
            mouse_click(claim)
        else:
            break

    series = [
        {'box': uis['tab_menu_alliance_gifts_normal'], 'interval': 3},
        {'box': uis['btn_menu_alliance_gifts_claimAll'], 'interval': 2},
        {'box': uis['tab_menu_alliance_gifts_rare'], 'interval': 3},
    ]
    mouse_click_series_box(series=series)

    for i in range(1, 4):
        box = uis['box_menu_alliance_gifts_claim' + i]
        mouse_click_box(box)
    
    series = [
        {'box': uis['btn__menu_alliance_gifts_CLOSE'], 'interval': 2},
        {'box': uis['btn__menu_alliance_CLOSE'], 'interval':2},
    ]
    mouse_click_series_box(series=series)


def do_allianceHelp():
    """
    기능: 연맹 도움 클릭
    """
    # Note: menu가 열려있는지 확인 후 닫혀있으면 연다
    # unfold_menu()
    series = [
        {'box': uis['btn_menu_alliance'], 'interval': 2},
        {'box': uis['btn_menu_alliance_help'], 'interval':2},
        {'box': uis['btn_menu_alliance_help_help'], 'interval': 2},  ## 도움이 있을 때
        {'box': uis['btn_menu_alliance_help_CLOSE'], 'interval': 2},  ## 도움이 없을 때
        {'box': uis['btn_menu_alliance_CLOSE'], 'interval': 1}
    ]
    mouse_click_series_box(series=series)


def buy_expedition_store(items=['aethelflaed', 'legend', 'goldStar', 'goldStar4', 'training']):
    """
    기능: expedition 스토어 아이템 구매
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - items || 구매 리스트 | list | [] | '애설', '쿠스', '식량', '목재', '석재', '금화', '전설', '황별', '황별2', '황별4', '은별', '은별2', '은별4', '책'('aethelflaed', 'constance', 'legend', 'goldStar', 'goldStar2', 'goldStar4', 'silverStar', 'silverStar2', 'silverStar4', 'book', 'food', 'wood', 'stone', 'gold')
        - black || 구매 배제 리스트 | list | [] | '애설', '쿠스', 
    Note:
        - 
    """
    for item in items:
        name = 'btn_menu_campaign_expedition_store_' + item
        if item == 'aethelflaed' or item == 'constance' or item == 'legend':
            center = mouse_click_box(box=uis[name])
        else:
            template = config['UIS'] + name + config['IMG_EXT']
            center = match_image_box(template=template, image=uis['box_menu_campaign_expedition_store_items'], precision=0.999)
            if center:
                offset = config['expedition_store_offset']
                mouse_click(position=[center[0] + offset[0], center[1] + offset[1]])
            else:
                print('not found: {}'.format(item))


def open_buy_expedition():
    """
    기능: expedition 상자 오픈, 스토어 아이템 구매
    """
    # Note: menu가 열려있는지 확인 후 닫혀있으면 연다
    # unfold_menu()
    series = [
        {'box': uis['btn_menu_campaign'], 'interval': 2},
        {'box': uis['btn_menu_campaign_expedition'], 'interval':2},
        {'box': uis['btn_menu_campaign_expedition_chest'], 'interval': 2, 'callback':mouse_click, 'kwargs':{'position':center_from_box(uis['btn_menu_campaign_expedition_rewards']), 'clicks':4, 'interval':0.5}},  ## expedition 상자 오픈
        {'box': uis['btn_menu_campaign_expedition_store'], 'interval': 2},  ## expedition 스토어
    ]
    mouse_click_series_box(series=series)

    buy_expedition_store(items=['aethelflaed', 'legend', 'goldStar', 'goldStar4', 'training'])

    ## refresh 가격이 무료인 경우, 다시 한번 더
    name = 'txt_menu_campaign_expedition_store_free'
    template = config['_OCR'] + name + config['IMG_EXT']
    free = match_image_box(template=template, image=expand_box(box=uis[name], offset=[10, 10]))
    if type(free) is list:
        mouse_click_box(box=uis['btn_menu_campaign_expedition_store_refresh'])
        time.sleep(1)
        buy_expedition_store(items=['legend', 'goldStar', 'goldStar4', 'training'])

    series = [
        {'box': uis['btn_menu_campaign_expedition_store_CLOSE'], 'interval': 2},
        {'box': uis['btn_menu_campaign_expedition_BACK'], 'interval':2},
        {'box': uis['btn_menu_campaign_BACK'], 'interval': 2}
    ]
    mouse_click_series_box(series=series)


def donate_allianceSkills():
    """
    기능: 연맹 기술 기부
    """
    series = [
        {'box': uis['btn_menu_alliance'], 'interval': 2},
        {'box': uis['btn_menu_alliance_technology'], 'interval': 2}
    ]
    mouse_click_series_box(series=series)

    prefix = 'tab_menu_alliance_technology_'
    skills = ['development', 'territory', 'war', 'allianceSkill']

    found = False
    for skill in skills:
        tab = uis[prefix + skill]

        ## 기부할 수 있는 기술 찾음, 없으면 다른 탭을 누름 누름
        notFull = 'img_menu_alliance_technology_notFull'
        template = set_img_path(notFull)
        image = uis['box_menu_alliance_technology_skills']
        # match_image_box(template=template, image=image, precision=0.997, multi=True, show=True)
        center = match_image_box(template=template, image=image, precision=0.997)

        if not center:  ## Note: 수평 스크롤을 이용해서 기부할 수 있는 기술 더 찾아야 함!!!
            mouse_click(tab)
            time.sleep(1)
            continue
        else:
            found = True
            mouse_click(center)
            time.sleep(1)
            break

    ## 기부 / CLOSE
    if found:
        mouse_press(position=center_from_box(uis['btn_menu_alliance_technology_donate']), duration=20)
        series = [
            {'box': uis['btn_menu_alliance_technology_donate_CLOSE'], 'interval': 2},
            {'box': uis['btn_menu_alliance_technology_CLOSE'], 'interval': 2},
            {'box': uis['btn_menu_alliance_CLOSE'], 'interval': 2}
        ]
        mouse_click_series_box(series=series)
    else:
        series = [
            {'box': uis['btn_menu_alliance_technology_CLOSE'], 'interval': 2},
            {'box': uis['btn_menu_alliance_CLOSE'], 'interval': 2}
        ]
        mouse_click_series_box(series=series)


if __name__ == '__main__':
    time.sleep(5)
    # login('millennium 102') ## 입력값(nick)에 해당하는 캐릭터로 login
    # claim_VIP() ## 매일 주어지는 VIP point/chest gift 수령
    # do_allianceHelp() ## 연맹 도움
    # open_buy_expedition()  ## expedition 상자 오픈, 스토어 아이템 구매
    # donate_allianceSkills()  ## 연맹 기술 기부
    claim_gifts()  ## 연맹 선물 수령
