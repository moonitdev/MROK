from actions import *
sys.path.append(os.path.join(os.path.dirname(__file__), '../supporters'))
from connector import *

daily_works = [claim_VIP, claim_gifts, buy_expedition_store]
# hourly_works = [do_allianceHelp, do_resources]

schedules = {
    'deverlife': [
        {
            'sn':'M001',
            'works': daily_works
        },
        {
            'sn':'M002',
            'works': daily_works
        },
        {
            'sn':'M003',
            'works': daily_works
        },
        {
            'sn':'M004',
            'works': daily_works
        },
        {
            'sn':'M005',
            'works': daily_works
        },
        {
            'sn':'M007',
            'works': daily_works
        },
        {
            'sn':'M010',
            'works': daily_works
        },
        {
            'sn':'M011',
            'works': daily_works
        },
    ],
    
    # 'life681225': [
    #     {
    #         'sn':'M201',
    #         'works': [
    #             claim_VIP,
    #             # claim_gifts,
    #             # do_allianceHelp,
    #             # buy_expedition_store
    #         ]
    #     },
    #     {
    #         'sn':'M202',
    #         'works': [
    #             claim_VIP,
    #             # claim_gifts,
    #             # do_allianceHelp,
    #             # buy_expedition_store
    #         ]
    #     },
    # ],

    # 'monwater': [
    #     {
    #         'sn':'M101',
    #         'works': [
    #             claim_VIP,
    #             # claim_gifts,
    #             # do_allianceHelp,
    #             # buy_expedition_store
    #         ]
    #     },
    #     {
    #         'sn':'M102',
    #         'works': [
    #             claim_VIP,
    #             # claim_gifts,
    #             # do_allianceHelp,
    #             # buy_expedition_store
    #         ]
    #     },
    # ]
    
}


def do_tasks(schedules):
    for account, tasks in schedules.items():
        print('account: {}'.format(account))
        goto_account(account)
        for task in tasks:
            print("I'm :{}".format(task['sn']))
            _sn = get_sn(get_nick())
            if _sn != task['sn']:
                goto_sn(task['sn'])
            time.sleep(2)
            for work in task['works']:
                clear_network_error()
                clear_verification()
                work()

# def do_tasks(tasks):
#     conn = Connector()
#     for task in tasks:
#         print("I'm :{}".format(task['sn']))
#         conn.goto_sn(task['sn'])
#         time.sleep(30)
#         for work in task['works']:
#             work()


# connect()

time.sleep(5)

do_tasks(schedules)