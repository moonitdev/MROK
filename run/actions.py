import os, sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../supporters'))
# from databaser.GoogleSpread import GoogleSpread
from connector import *
from functions.imageFns import *
from functions.guiFns import *
from functions.dataFns import file_to_json

uis = file_to_json('../_config/json/uis.json')
config = file_to_json('../_config/json/config.json')
characters = file_to_json('../_config/json/characters.json')
buildings = file_to_json('../_config/json/buildings.json')

characters_image = config['CHARACTERS']
screenshots_image = config['SCREENSHOTS']



def claim_city_resources():
    """
    기능: 도시 자원 수령(클릭)
    Note:
      - 자원 수령 주기(time interval) 정할 수 있도록
    """
    series = [
        {'position': buildings['farm']['box'], 'interval': 0.2},
        {'position': buildings['lumberMill']['box'], 'interval': 0.2},
        {'position': buildings['quarry']['box'], 'interval': 0.2},
        {'position': buildings['goldMine']['box'], 'interval': 1}
    ]
    mouse_click_series(series=series)


def search_resources(resource='food', level=5, kingdom='normal'):
    """
    기능: 도시 자원 검색
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | '../images/source/dest01.png'
        - resource || 자원 종류 | str | 'food' | {'food': 'cropland', 'wood': 'loggingCamp', 'stone': 'stoneDeposit', 'gold': 'goldDeposit'}
        - level || 자원 레벨 | int | 5 | 1, 2, ...., 10
        - kingdom || 킹덤 종류 | str | 'normal' | 'normal': 일반 / 'lost': '잃어버린 왕국(kvk)'
    Note:
      - '+' 버튼을 몇 번 누를 것인지?(default level값 확인은?)
      - 해당 level 자원이 없는 경우 '-'를 눌러 level - 1 자원 찾기
      - 다른 유저 채취 행군/도착 여부 확인 필요!!!
    """
    mapper = {'food': 'cropland', 'wood': 'loggingCamp', 'stone': 'stoneDeposit', 'gold': 'goldDeposit'}

    ## viewMode -> allianceView
    set_view_mode(mode='AllianceView')

    ## click search(main) button
    ## click search resource button
    btn_search1 =  uis['btn_search_' + mapper[resource]]
    btn_search2 =  uis['btn_search_' + mapper[resource] + '_search']
    btn_plus =  uis['btn_search_' + mapper[resource] + '_plus']

    series = [
        {'position': uis['btn_Main_Search'], 'interval': 0.5},
        {'position': btn_search1, 'interval': 0.2},
    ]

    mouse_click_series(series=series)

    ## click level plus
    for _ in range(0, level):
        mouse_click(btn_plus)

    ## click search(modal) button
    mouse_click(btn_search2)

    ## 다시 search 버튼이 나타나는지 확인
    



def claim_VIP():
    """
    기능: 매일 주어지는 VIP point/chest gift 수령
    """
    series = [
        {'position': uis['btn_Main_VIP'], 'interval': 2},
        {'position': uis['btn_profile_VIP_pointsChest'], 'interval': 4, 'callback':mouse_click, 'kwargs':{'position':None, 'clicks':4, 'interval':0.5}},
        {'position': uis['btn_profile_VIP_pointsClaim'], 'interval': 4, 'callback':mouse_click, 'kwargs':{'position':None, 'clicks':4, 'interval':0.5}},
        {'position': uis['btn_profile_VIP_CLOSE'], 'interval': 1}
    ]
    mouse_click_series(series=series)


def claim_gifts_rare():
    template = img_path(prefix='bdg_menu_alliance_gifts_rare_new', where='UIS')
    # image = img_path(prefix='uis/menu_alliance_gifts11', where='SCREENSHOTS')
    image = expand_box(uis['bdg_menu_alliance_gifts_rare_new'], offset=[10, 10])
    mask = img_path(prefix='msk_menu_alliance_gifts_normal_new', where='UIS')

    if match_image_box(template=template, image=image, mask=mask, precision=0.999):
        mouse_click(position=uis['tab_menu_alliance_gifts_rare'])
        time.sleep(1)
        ## rare 선물 claim 누르기
        for _ in range(0, 50):
            image_box = expand_box(box=uis['box_menu_alliance_gifts_claim4'], offset=[20, 10])
            claim = match_image_box(template=set_img_path('btn_menu_alliance_gifts_claim'), image=image_box)
            if type(claim) is list:
                mouse_click(claim)
            else:
                break
    
        scroll_box = uis['box_menu_alliance_claim']
        mouse_scroll_box(box=scroll_box, direction=[0, -1], offset=5)
        # mouse_scroll_box(box=scroll_box, direction=[0, 1], offset=5)
        # mouse_scroll(start=[], scroll=-100)
        for i in range(1, 4):
            box = uis['box_menu_alliance_gifts_claim' + str(i)]
            print('box: {}, box: {}'.format(i, box))
            mouse_click(box)

    # return match_image_box(template=template, image=image, mask=mask, precision=0.999, show=True)


def claim_gifts_normal():
    template = img_path(prefix='bdg_menu_alliance_gifts_normal_new', where='UIS')
    image = expand_box(uis['bdg_menu_alliance_gifts_normal_new'], offset=[10, 10])
    mask = img_path(prefix='msk_menu_alliance_gifts_normal_new', where='UIS')

    if match_image_box(template=template, image=image, mask=mask, precision=0.999):
        series = [
            {'position': uis['tab_menu_alliance_gifts_normal'], 'interval': 3},
            {'position': uis['btn_menu_alliance_gifts_claimAll'], 'interval': 2},
            {'position': uis['btn_menu_alliance_gifts_rewards_confirm'], 'interval': 2},
        ]
        mouse_click_series(series=series)


def claim_gifts():
    """
    기능: 연맹 선물 수령
    Note:
      - 새로운 선물(빨간 동그라미)이 있을 때만 클릭하도록!!
    """
    set_menu_mode(mode='unfold')
    mouse_click(position=uis['btn_menu_alliance'])
    time.sleep(1)

    template = img_path(prefix='bdg_menu_alliance_gifts', where='UIS')
    image = expand_box(uis['bdg_menu_alliance_gifts'], offset=[10, 10])

    if match_image_box(template=template, image=image, precision=0.999): ## 새로운 선물이 있으면
        print('new gifts exist!')
        mouse_click(position=uis['btn_menu_alliance_gifts'])
        time.sleep(2)
        claim_gifts_rare()
        claim_gifts_normal()

        series = [
            {'position': uis['btn_menu_alliance_gifts_CLOSE'], 'interval': 2},
            {'position': uis['btn_menu_alliance_CLOSE'], 'interval':2},
        ]
        mouse_click_series(series=series)
    else:
        print('new gifts not exist!')
        mouse_click(uis['btn_menu_alliance_CLOSE'])
        return False


# def claim_gifts():
#     """
#     기능: 연맹 선물 수령
#     Note:
#       - 새로운 선물(빨간 동그라미)이 있을 때만 클릭하도록!!
#     """
#     series = [
#         {'position': uis['btn_menu_alliance'], 'interval': 2},
#         {'position': uis['btn_menu_alliance_gifts'], 'interval': 2},
#         {'position': uis['tab_menu_alliance_gifts_rare'], 'interval': 3},
#     ]
#     mouse_click_series(series=series)

#     ## rare 선물 claim 누르기
#     for _ in range(0, 50):
#         image_box = expand_box(box=uis['box_menu_alliance_gifts_claim4'], offset=[20, 10])
#         claim = match_image_box(template=set_img_path('btn_menu_alliance_gifts_claim'), image=image_box)
#         if type(claim) is list:
#             mouse_click(claim)
#         else:
#             break

#     series = [
#         {'position': uis['tab_menu_alliance_gifts_normal'], 'interval': 3},
#         {'position': uis['btn_menu_alliance_gifts_claimAll'], 'interval': 2},
#         {'position': uis['btn_menu_alliance_gifts_rewards_confirm'], 'interval': 2},
#         {'position': uis['tab_menu_alliance_gifts_rare'], 'interval': 3},
#     ]
#     mouse_click_series(series=series)
#     time.sleep(2)

#     for i in range(1, 4):
#         box = uis['box_menu_alliance_gifts_claim' + str(i)]
#         print('box: {}, box: {}'.format(i, box))
#         mouse_click(box)
    
#     series = [
#         {'position': uis['btn_menu_alliance_gifts_CLOSE'], 'interval': 2},
#         {'position': uis['btn_menu_alliance_CLOSE'], 'interval':2},
#     ]
#     mouse_click_series(series=series)


def open_tavern_chest(chest='free'):
    """
    기능: 주점 상자 열기
    Note:
      - 자원 수령 주기(time interval) 정할 수 있도록
      - silver 일일퀘스트 완료용 함수 필요
      - 장비, 도감 완료시 버튼 클릭 확인
    """
    series = [
        {'position': buildings['tavern']['box'], 'interval': 2},
        {'position': uis['btn_tavern_open_chest_silver_open']['box'], 'interval': 0.2},
        {'position': buildings['quarry']['box'], 'interval': 0.2},
        {'position': buildings['goldMine']['box'], 'interval': 1}
    ]
    mouse_click_series(series=series)


def do_allianceHelp():
    """
    기능: 연맹 도움 클릭
    """
    # Note: menu가 열려있는지 확인 후 닫혀있으면 연다
    # unfold_menu()
    series = [
        {'position': uis['btn_menu_alliance'], 'interval': 2},
        {'position': uis['btn_menu_alliance_help'], 'interval':2},
        {'position': uis['btn_menu_alliance_help_help'], 'interval': 2},  ## 도움이 있을 때
        {'position': uis['btn_menu_alliance_help_CLOSE'], 'interval': 2},  ## 도움이 없을 때
        {'position': uis['btn_menu_alliance_CLOSE'], 'interval': 1}
    ]
    mouse_click_series(series=series)


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
            center = mouse_click(position=uis[name])
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
        {'position': uis['btn_menu_campaign'], 'interval': 2},
        {'position': uis['btn_menu_campaign_expedition'], 'interval':2},
        {'position': uis['btn_menu_campaign_expedition_chest'], 'interval': 2, 'callback':mouse_click, 'kwargs':{'position':center_from_box(uis['btn_menu_campaign_expedition_rewards']), 'clicks':4, 'interval':0.5}},  ## expedition 상자 오픈
        {'position': uis['btn_menu_campaign_expedition_store'], 'interval': 2},  ## expedition 스토어
    ]
    mouse_click_series(series=series)

    buy_expedition_store(items=['aethelflaed', 'legend', 'goldStar', 'goldStar4', 'training'])

    ## refresh 가격이 무료인 경우, 다시 한번 더
    name = 'txt_menu_campaign_expedition_store_free'
    template = config['_OCR'] + name + config['IMG_EXT']
    free = match_image_box(template=template, image=expand_box(box=uis[name], offset=[10, 10]))
    if type(free) is list:
        mouse_click(position=uis['btn_menu_campaign_expedition_store_refresh'])
        time.sleep(1)
        buy_expedition_store(items=['legend', 'goldStar', 'goldStar4', 'training'])

    series = [
        {'position': uis['btn_menu_campaign_expedition_store_CLOSE'], 'interval': 2},
        {'position': uis['btn_menu_campaign_expedition_BACK'], 'interval':2},
        {'position': uis['btn_menu_campaign_BACK'], 'interval': 2}
    ]
    mouse_click_series(series=series)


def donate_allianceSkills():
    """
    기능: 연맹 기술 기부
    """
    series = [
        {'position': uis['btn_menu_alliance'], 'interval': 2},
        {'position': uis['btn_menu_alliance_technology'], 'interval': 2}
    ]
    mouse_click_series(series=series)

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
            {'position': uis['btn_menu_alliance_technology_donate_CLOSE'], 'interval': 2},
            {'position': uis['btn_menu_alliance_technology_CLOSE'], 'interval': 2},
            {'position': uis['btn_menu_alliance_CLOSE'], 'interval': 2}
        ]
        mouse_click_series(series=series)
    else:
        series = [
            {'position': uis['btn_menu_alliance_technology_CLOSE'], 'interval': 2},
            {'position': uis['btn_menu_alliance_CLOSE'], 'interval': 2}
        ]
        mouse_click_series(series=series)


if __name__ == '__main__':
    time.sleep(5)
    # login('millennium 102') ## 입력값(nick)에 해당하는 캐릭터로 login
    # claim_VIP() ## 매일 주어지는 VIP point/chest gift 수령
    # do_allianceHelp() ## 연맹 도움
    # open_buy_expedition()  ## expedition 상자 오픈, 스토어 아이템 구매
    # donate_allianceSkills()  ## 연맹 기술 기부
    # claim_gifts()  ## 연맹 선물 수령
    # claim_city_resources()  ## 도시 자원 수령

    # search_resources(resource='wood', level=5) ## 자원지 찾기

    # claim_gifts_rare()  ## 희귀 연맹 선물 수령
    # claim_gifts_normal()  ## 일반 연맹 선물 
    claim_gifts()  ## 연맹 선물 수령