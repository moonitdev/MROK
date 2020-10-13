# import actions

characters = ['', '', '']

# tasks = [
#     {
#         'sn':'M001',
#         'works': [
#             claim_VIP,
#             claim_gifts,
#             do_allianceHelp,
#             buy_expedition_store
#         ]
#     },
#     {
#         'sn':'M002',
#         'works': [
#             claim_VIP,
#             claim_gifts,
#             do_allianceHelp,
#             buy_expedition_store
#         ]
#     },
# ]

def work1():
    print('this is work1')

def work2():
    print('this is work2')

def work3():
    print('this is work3')

def work4():
    print('this is work4')

def work5():
    print('this is work5')

tasks = [
    {
        'sn':'M001',
        'works': [
            work1,
            work2,
            work3,
            work4
        ]
    },
    {
        'sn':'M002',
        'works': [
            work1,
            work2,
            work3,
            work4,
            work5
        ]
    },
]



def do_tasks(tasks):
    for task in tasks:
        print("I'm :{}".format(task['sn']))
        # 현재 캐릭터 'sn' != task['sn'] -> login
        for work in task['works']:
            work()

do_tasks(tasks)