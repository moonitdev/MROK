import actions

characters = ['', '', '']

tasks = [
    {
        'sn':'M001',
        'works': [
            claim_VIP,
            claim_gifts,
            do_allianceHelp,
            buy_expedition_store
        ]
    },
    {
        'sn':'M002',
        'works': [
            claim_VIP,
            claim_gifts,
            do_allianceHelp,
            buy_expedition_store
        ]
    },
]

def do_tasks(tasks):
    for task in tasks:
        # 현재 캐릭터 'sn' != task['sn'] -> login
        for work in works:
            work()