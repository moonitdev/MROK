# -*- coding:utf-8 -*-
import os, sys
from pathlib import Path
import json
import yaml
import re
import numpy as np

##-------------------------------------------------------------------
## 파일 관리(File Management)
def create_folder(path=None):
    """
    기능: 해당 폴더(folder, directory)가 없으면 새로 만듬
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 폴더 경로 || str | None | 'C:/dir1/dir2' 또는 'dir3/dir4'
    """
    if not os.path.exists(path):
        # print('Creating folder ' + path)
        os.makedirs(path)


def json_to_file(data={'a':'A', 'b':'B'}, path=None, encoding='UTF-8'):
    """
    기능: data(json 형식)를 path(파일 이름 포함: '')에 파일로 저장
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - data || 저장할 데이터 | str | None | {'a':'A', 'b':'B'}
        - path || 저장할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.json' 또는 'dir3/fn2.json'
        - encoding || 저장할 파일 인코딩 값 | str | 'UTF-8' | 'UTF-8'
    """
    with open(path, 'w', encoding=encoding) as file:
        file.write(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def file_to_json(path, encoding='UTF-8'):
    """
    기능: path(파일 이름 포함)의 파일을 json 형태로 출력
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 저장할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.json' 또는 'dir3/fn2.json'
        - encoding || 저장할 파일 인코딩 값 | str | 'UTF-8' | 'UTF-8'
    출력:
        - 의미 | 데이터 타입 | 예시
        - json 데이터 | str | {'a':'A', 'b':'B'}
    """
    with open(path, encoding=encoding) as f:
        return json.load(f)


def modify_file(path=None, replacements=None):
    """
    기능: path(파일 이름 포함)의 파일 내용을 replacements를 이용해서 교체
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 변경할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.json' 또는 'dir3/fn2.json'
        - replacements || 문자열 변경 매핑 딕셔너리 | dict | None | {'org1':'rep1', 'org2':'rep2'}
    출력:
        - 의미 | 데이터 타입 | 예시
        - json 데이터 | str | {'a':'A', 'b':'B'}
    Note:
        - 교정 필요: _traning/lecture/nomardcorders 참조
    """
    # Read in the file
    with open(path, 'r') as file :
        data = file.read()

    # Replace the target string
    for key, val in replacements.items():
        data = data.replace(key, val)

    # Write the file out again
    with open(path, 'w') as file:
        file.write(data)


def file_to_set(path=None):
    """
    기능: path(파일 이름 포함)의 파일 내용을 줄단위로 set로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.txt' 또는 'dir3/fn2.txt'
    출력:
        - 의미 | 데이터 타입 | 예시
        - 줄단위 변환 set | set | ('첫번째 줄', '두번째 줄', '세번째 줄')
    Note:
        - 교정 필요: 좀더 최적화가 될 수도?
        - 변경할 데이터 형식을 입력값으로 지정하여 하나의 함수로 만드는 것도 고려할 필요있음
    """
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def set_to_file(_set=(), path=None, sorted=False):
    """
    기능: set 형식의 데이터를 path(파일 이름 포함)의 파일(줄단위)로 저장
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - _set || set형식의 데이터 | set | () | ('우리는', '민족중흥의', '역사적 사명을')
        - path || 저장 할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.txt' 또는 'dir3/fn2.txt'
        - sorted || _set의 소팅 여부 | bool | False | True
    Note:
        - 교정 필요: 분리 기호(separator)를 입력값으로 지정, 입력 순서에 무관하도록 **kwargs로 변환 고려
    """
    with open(path, "w") as f:
        if sorted: _set = sorted(_set)
        for s in _set:
            f.write(s+"\n")


def write_file(path=None, data=None, encoding='UTF-8'):
    """
    기능: path(파일 이름 포함)의 파일을 새로 만들어 data를 저장하거나, 기존 path의 파일에 data를 덮어씀
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 저장 할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.txt' 또는 'dir3/fn2.txt'
        - data || 저장할 내용 | str | None | '저장할 내용입니다'
    """
    with open(path, 'w', encoding=encoding) as f:
        f.write(data)


def copy_file(source_path=None, copy_path=None, encoding='UTF-8'):
    """
    기능: path(파일 이름 포함)의 파일을 새로 만들어 data를 저장하거나, 기존 path의 파일에 data를 덮어씀
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 저장 할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.txt' 또는 'dir3/fn2.txt'
        - data || 저장할 내용 | str | None | '저장할 내용입니다'
    """
    # Read in the file
    with open(source_path, 'r', encoding=encoding) as file :
        data = file.read()
        # Write the file
        with open(copy_path, 'w', encoding=encoding) as file:
            file.write(data)


def append_to_file(path=None, data=None):
    """
    기능: path(파일 이름 포함)의 파일에 data 추가
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 저장할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.json' 또는 'dir3/fn2.json'
        - data || 추가할 내용 | str | None | '추가할 내용입니다'
    """
    with open(path, 'a') as file:
        file.write(data + '\n')


def delete_file_contents(path=None):
    """
    기능: path(파일 이름 포함)의 파일 삭제
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 저장할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2/fn1.json' 또는 'dir3/fn2.json'
    """
    open(path, 'w').close()


def rename_all(path=None, callback=None):
    """
    기능: path(파일 이름 제외)에 있는 모든 파일에 대해 callback(함수)를 통해 이름 변경
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 저장할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/dir2' 또는 'dir3/dir4'
        - callback || 이름 변경시 사용할 replace 함수 | function | None | lambda filename : re.sub(r'\D', '', filename) + '.png'
    Note:
        - 콜백[callback] 함수, 사용법에 대한 이해가 필요
    """
    for filename in os.listdir(path):
        os.rename(path + filename, path + callback(filename))


def yml_update(path=None, data={}):
    """
    기능: path에 있는 yml 파일을 data를 이용하여 변경
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - path || 저장할 파일 경로(파일 이름 포함) | str | None | 'C:/dir1/settings.yml'
        - data || 변경할 데이터 | dict | {} | {'k1':'v1', 'k2':'v2'}
    """
    with open(path, 'r', encoding='UTF-8') as f:
        doc = yaml.load(f)

    doc = _yml_update(data, doc)
    # for k, v in data.items():
    #     #if type(v) == dict:
    #     doc[k] = v
    with open(path, 'w', encoding='UTF-8') as f:
        # doc = yaml.load(f)
        # for k, v in data.items():
        #     #if type(v) == dict:
        #     doc[k] = v
        yaml.dump(doc, f)


##재귀 함수 for yml_update
def _yml_update(data={}, base={}):
    for k, v in data.items():
        if type(v) == dict:
            _yml_update(data=v, base=base[k])
        else:
            base[k] = v
    return base

##-------------------------------------------------------------------
## 데이터 관리(Data Management)

def get_dict_elem(d={}, *keys):
    """
    기능: 다중 레벨 딕셔너리의 요소값을 구함
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - d || 대상 딕셔너리 | dict | {} | { 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }
        - *keys || 요소값을 구할 key 배열 | tuple | None | ('k11', 'k31', 'k41') -> d['k11']['k31']['k41']
    출력:
        - 의미 | 데이터 타입 | 예시
        - 해당 요소값 | any | d['k11']['k31']['k41'] -> 'c41'
    Note:
        - 사용례1: keys = ('k11', 'k31', 'k41') // get_dict_elem({ 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }, *keys)
        - 사용례2: get_dict_elem({ 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }, 'k11', 'k31', 'k41')
        - [참조](https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    for key in keys:
        d = d[key]
    return d


def set_dict_elem(d={}, *args):
    """
    기능: 다중 레벨 딕셔너리의 해당 요소에 값을 넣음
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - d || 대상 딕셔너리 | dict | {} | { 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }
        - *args || key값 + 입력값 | tuple | None | ('k11', 'k31', 'k42', 'v42') -> d['k11']['k31']['k42'] = 'v42'
    Note:
        - 사용례1: args = ('k11', 'k31', 'k42', 'v42') // set_dict_elem({ 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }, *args)
        - 사용례2: get_dict_elem({ 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }, 'k11', 'k31', 'k42', 'v42')
        - 해당 딕셔너리에 d['k11']['k31']['k42'] = 'v42' 가 추가됨
        - [참조](https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    for arg in args[:-2]:
        if type(d.get(arg)) is not dict:
            d[arg] = {}
        d = d[arg]
    d[args[-2]] = args[-1]


def set_dict_elem_callback(d={}, callback=None, *args):
    """
    기능: 다중 레벨 딕셔너리의 해당 요소에 값을 넣음
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - d || 대상 딕셔너리 | dict | {} | { 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }
        - *args || key값 + 입력값 | tuple | None | ('k11', 'k31', 'k42', 'v42') -> d['k11']['k31']['k42'] = 'v42'
    Note:
        - 사용례1: args = ('k11', 'k31', 'k42', 'v42') // set_dict_elem({ 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }, *args)
        - 사용례2: get_dict_elem({ 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }, 'k11', 'k31', 'k42', 'v42')
        - 해당 딕셔너리에 d['k11']['k31']['k42'] = 'v42' 가 추가됨
        - [참조](https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    for arg in args[:-2]:
        if type(d.get(arg)) is not dict:
            d[arg] = {}
        d = d[arg]
    d[args[-2]] = callback(args[-1])

# def get_dict_elem_keys(d, condition, keys, out):
#     """
#     기능: condition(callback 함수)에 맞는 다중 딕셔너리 key값들을 구함
#     입력:
#         - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
#         - d || 대상 딕셔너리 | dict | {} | { 'k11': { 'k21': 'c21', 'k31': { 'k41': 'c41' } } }
#         - conditon || 조건에 따른 True, False 반환 함수 | function | None |
#     Note:
#         - 사용례1:
#         -
#         -
#     """
#     if condition(d):
#         out.append(tuple(copy.deepcopy(keys)))
#     else:
#         for elem in d['elems']:
#             if 'name' in elem:
#                 k = elem['name']
#                 print('k: {}, keys: {}'.format(k, keys))
#                 keys.append(k)
#             get_dict_elem_keys(elem, condition, keys, out)

#     return out


def remove_space_character(data=None, line_chr=True):
    """
    기능: 공백 문자 제거
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - data || 문자열 | str | None | '우리는\n민족중흥의    역사적 \n 사명을'
        - line_chr || 줄바꿈 문자 제거 여부 | bool | True | True
    출력:
        - 의미 | 데이터 타입 | 예시
        - 공백 문자가 제거된 문자열 | str | '우리는 민족중흥의 역사적 사명을'
    """
    if line_chr:
        data = data.replace("\n", ' ')
    data = re.sub(r"\s{2,}", " ", data, flags=re.UNICODE)
    return data


def list_to_dict(lists=[[]]):
    """
    기능: list 형식의 데이터를 dict 형식으로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - lists || 리스트 형식 데이터(첫번째 list는 dict의 key값 배열, 이후는 value값 배열) | list | [[]] | [['h1', 'h2', 'h3'], ['c11', 'c12', 'c13'], ['c21', 'c22', 'c23']]
    출력:
        - 의미 | 데이터 타입 | 예시
        - dict 형식으로 변환된 값 | dict | [{'h1':'c11', 'h2':'c12'}, {'h1':'c21', 'h2':'c22'}]
    """
    return [dict(zip(lists[0], v)) for v in lists[1:]]


def flatten_list(lists=[[]]):
    """
    기능: list 내에 list들을 없앰(2차원 list를 1차원으로 만듬)
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - lists || 리스트 형식 데이터(첫번째 list는 dict의 key값 배열, 이후는 value값 배열) | list | [[]] | [['c01', 'c02', 'c03'], ['c11', 'c12', 'c13'], ['c21', 'c22', 'c23']]
    출력:
        - 의미 | 데이터 타입 | 예시
        - 1차원화된 list | list | ['c01', 'c02', 'c03', 'c11', 'c12', 'c13', 'c21', 'c22', 'c23']
    """
    return np.array(lists).flatten()


def remove_empty_list(lists=[[]]):
    """
    기능: list 내에 전부가 비어있는 list들을 삭제
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - lists || 리스트 형식 데이터(첫번째 list는 dict의 key값 배열, 이후는 value값 배열) | list | [[]] | [['c01', 'c02', 'c03'], ['', '', ''], ['c21', 'c22', 'c23']]
    출력:
        - 의미 | 데이터 타입 | 예시
        - 비어있는 list들이 삭제된 list | list |  [['c01', 'c02', 'c03'], ['c21', 'c22', 'c23']]
    """
    return [l for l in lists if any(i != '' for i in l)]


def dict_to_csv(dt={}, separator="\t", header=True):
    """
    기능: dict 형식 데이터들의 list를 csv(분리기호 지정 가능, 첫번째 줄은 keys, 그 이후는 values)로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - dt || dict 형식의 데이터 | dict | {} | {'h1':'c11', 'h2':'c12'}
        - separator || 분리기호 | str | ',' | '\t' [탭]
        - header || dict의 key값, csv의 header | bool | True
    출력:
        - 의미 | 데이터 타입 | 예시
        - csv | str | 'h1,h2\nc11,c12' (header=False이면, 'c11,c12')
    """
    csv = ''
    if header:
        csv = separator.join(dt.keys())
    values = [ remove_space_character(data=str(value), line_chr=True) for value in dt.values()]
    return (csv + '\n' + separator.join(values)).strip()


def dicts_to_csv(dicts=[{}], separator=","):
    """
    기능: dict 형식 데이터들의 list를 csv(분리기호 지정 가능, 첫번째 줄은 keys, 그 이후는 values)로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - dicts || dict 형식의 데이터들의 list | list | [{}] | [{'h1':'c11', 'h2':'c12'}, {'h1':'c21', 'h2':'c22'}]
        - separator || 분리기호 | str | ',' | '\t' [탭]
    출력:
        - 의미 | 데이터 타입 | 예시
        - csv | str | 'h1,h2\nc11,c12\nc21,c22'
    """
    csv = separator.join(dicts[0].keys())
    for d in dicts:
        csv = csv + '\n' + separator.join(d.values())
    return csv


def csv_to_dicts(csv="", separator=","):
    """
    기능: csv(분리기호 지정 가능, 첫번째 줄은 keys, 그 이후는 values) 데이터를 dict 형식 데이터들의 list로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - csv || csv 형식 데이터(첫번째 줄은 keys, 그 이후는 values) | str | [{}] | 'h1,h2\nc11,c12\nc21,c22'
        - separator || 분리기호 | str | ',' | '\t' [탭]
    출력:
        - 의미 | 데이터 타입 | 예시
        - dict 형식 데이터들의 list | list | [{'h1':'c11', 'h2':'c12'}, {'h1':'c21', 'h2':'c22'}]
    """
    dicts = []
    lines = csv.split('\n')
    keys = lines[0].split(separator)
    print(keys)
    for line in lines[1:]:
        vals = line.split(separator)
        dicts.append({keys[i]: val for i, val in enumerate(vals)})
        # {k: v for k, v in zip(headers, cells)}
    return dicts


# ##@@ 기능:: convert dictionary to list
# ##@@ note::
# ##@@ usage::
# # d = {'a':0, 'b':[1, 2, 3, 4], 'c':[5,6,7,8], 'd':[9,10,11,12]}
# # plus = {'z':100}
# # l = [{'a': 0, 'b': 1, 'c': 5, 'd': 9}, {'a': 0, 'b': 2, 'c': 6, 'd': 10}, {'a': 0, 'b': 3, 'c': 7, 'd': 11}, {'a': 0, 'b': 4, 'c': 8, 'd': 12}]
# # def map_dict_to_list(d):
# #     return [{k: v[i] for k, v in d.items()} for i in range(0, len(d[list(d.keys())[0]]))]
# def map_dict_to_list(d, plus={}):
#     """
#     기능:
#     입력:
#         - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
#         -
#         -
#     출력:
#         - 의미 | 데이터 타입 | 예시
#         -
#     """
#     n = 0
#     for k, v in d.items():
#         if type(v) is list:
#             n = len(v)
#             break

#     for k, v in d.items():
#         if type(v) is not list:
#             d[k] = [v]*n

#     for k2, v2 in plus.items():
#         d[k2] = [v2]*n

#     return [{k: v[i] for k, v in d.items()} for i in range(0, len(d[list(d.keys())[-1]]))]


# ##@@ 기능:: remove dict if pk is overlaped
# ##@@ note::
# def remove_dicts_overlaped(orgs=[{}], pks=['']):
#     mems = []
#     for org in orgs:
#         is_eq = is_equal_dicts(org, mems, pks)
#         if is_eq:
#             org['_o_v_'] = 1
#         else:
#             mems.append(reduce_dict(org, pks))

#     return [d for d in orgs if not '_o_v_' in d]


# ##@@ 기능:: merge dicts if pk key:val is eqaul
# ##@@ note::
# def merge_dicts_overlaped(orgs=[{}], pks=[''], new_key=''):
#     mems = []
#     outs = []

#     for org in orgs:
#         is_eq = is_equal_dicts(org, mems, pks)
#         _org = reduce_dict(org, pks)
#         if is_eq:
#             for out in outs:
#                 if _org.items() == reduce_dict(out, pks).items():
#                     if not is_equal_dicts(reduce_dict_not(org, pks), out[new_key]):
#                         out[new_key].append(reduce_dict_not(org, pks))
#                     break
#         else:
#             mems.append(_org)
#             _org[new_key] = [reduce_dict_not(org, pks)]
#             outs.append(_org)

#     return outs


# ##@@ 기능:: merge dicts all
# ##@@ note::
# def merge_dicts(orgs=[{}], pks=[''], new_key=''):
#     _org = reduce_dict(orgs[0], pks)
#     _org[new_key] = []

#     for org in orgs:
#         _org[new_key].append(reduce_dict_not(org, pks))

#     return _org


# ##@@ 기능::
# ##@@ note::
# def is_equal_dict(org={}, dst={}, pks=[]):
#     if reduce_dict(org, pks).items() == reduce_dict(dst, pks).items():
#         return True

#     return False


# ##@@ 기능::
# ##@@ note::
# def is_equal_dicts(org={}, dsts=[], pks=[]):
#     for dst in dsts:
#         if is_equal_dict(org, dst, pks):
#             return True

#     return False


# ##@@ 기능::
# ##@@ note::
# def reduce_dicts(orgs=[{}], _keys=[]):
#     outs = []
#     for org in orgs:
#         outs.append(reduce_dict(org, _keys))
#     return outs


# ##@@ 기능:: org에서 _keys의 키 필드를 제외하고 제거
# ##@@ note::
# def reduce_dict(org={}, _keys=[]):
#     # pks = [] 인 경우는?
#     #print('reduce_dict org: {}'.format(org))
#     if _keys != []:
#         return {k:v for k, v in org.items() if k in _keys}
#     else:
#         return org


# ##@@ 기능::
# ##@@ note::
# def reduce_dict_not(org={}, _keys=[]):
#     # pks = [] 인 경우는?
#     if _keys != []:
#         return {k:v for k, v in org.items() if not k in _keys}
#     else:
#         return org

if __name__ == '__main__':
    data = {
        'PROJECT': {'name':'test2'}
    }
    base = {
        'PROJECT': {'name':'test1', 'url':'www.dot.com'},
        'LOGIN': {'wait':None, 'url':'www.not.com'}
    }
    result = _yml_update(data, base)
    print(result)