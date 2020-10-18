from actions import *
sys.path.append(os.path.join(os.path.dirname(__file__), '../supporters'))
from Connector import *


tasks = [
    {
        'sn':'M003',
        'works': [
            claim_VIP,
            claim_gifts,
            do_allianceHelp,
            buy_expedition_store
        ]
    },
    {
        'sn':'M001',
        'works': [
            claim_VIP,
            claim_gifts,
            do_allianceHelp,
            buy_expedition_store
        ]
    },
]


def do_tasks(tasks):
    conn = Connector()
    for task in tasks:
        print("I'm :{}".format(task['sn']))
        conn.goto_sn(task['sn'])
        time.sleep(30)
        for work in task['works']:
            work()




time.sleep(5)

do_tasks(tasks)