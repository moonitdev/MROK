import os, sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../supporters'))
from databaser.GoogleSpread import GoogleSpread

gdrive = GoogleSpread()
dicts = gdrive.read_sheet('ROK_SETTINGS', 'config')

print(dicts)

out = {}
for d in dicts:
    out[d['key']] = d['value']

    if d['type'] == 'int':
        out[d['key']] = int(d['value'])
    elif  d['type'] == 'float':
        out[d['key']] = float(d['value'])
    elif  d['type'] == 'json':
        out[d['key']] = json.loads(d['value'])

print(out)

# str_list = '[[ 1.35162297e+00,  6.28326412e-01, -3.39296263e+02], [ 6.93889390e-17,  2.27541342e+00, -4.98846844e+02], [ 2.71050543e-19,  6.51153648e-04,  1.00000000e+00]]'
# str_dict = '{"ROK_UI":"https://docs.google.com/spreadsheets/d/1hJ4OyhvRNKSz1zBIagX9r3_O-t-Go5C0MmmK_Hh1AAs/edit#gid=0", "Coin_Exchanges":"https://docs.google.com/spreadsheets/d/1x4su7uJELgcMMd0MlqvWFKf28QiKNQbDtMARnkAINY0/edit#gid=0"}'
# l = json.loads(str_list)
# d = json.loads(str_dict)

# print(l[0])
# print(d['ROK_UI'])