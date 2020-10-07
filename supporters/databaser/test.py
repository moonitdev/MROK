# import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'functions')) ## 현재 디렉토리 기준 상대 경로 설정
from dataFns import *  ## (사용자) 상용 함수 라이브러리


# def list_to_dict(ls=[]):
#     """
#     Brief: convert list to dictionary
#     Args: ls = [['h1', 'h2', 'h3', ...], ['c11', 'c12', 'c13', ....], ['c21', 'c22', 'c23', ....], ...]
#     Returns: [{'h1':'c11', 'h2':'c12', ...}, {'h1':'c21', 'h2':'c22', ...}, ...]
#     """
#     return [dict(zip(ls[0], v)) for v in ls[1:]]


# def flatten_list(ls):
#     """
#     Brief: flatten list
#     Args: ls = [['c01', 'c02', 'c03', ...], ['c11', 'c12', 'c13', ....], ['c21', 'c22', 'c23', ....], ...]
#     Returns: ['c01', 'c02', 'c03', ..., 'c11', 'c12', 'c13', ...., 'c21', 'c22', 'c23', ...., ...]
#     """
#     return np.array(ls).flatten()


# def remove_empty_list(ls):
#     """
#     Brief: flatten list
#     Args: ls = [['c01', 'c02', 'c03', ...], ['', '', '', ....], ['c21', 'c22', 'c23', ....], ...]
#     Returns: [['c01', 'c02', 'c03', ...], ['c21', 'c22', 'c23', ....], ...]
#     """
#     return [l for l in ls if any(i != '' for i in l)]


def find_first_filled_col(data=[[]]):
    """
    기능: list들의 list에서 전부 비어있지 않은 row에서 비어있지 않은 첫번째 col의 번호를 구함
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - data || list들의 list || list | [[]] | [['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', 'one', '', '', '', '', '', ''], ['', '03-01-1900', 'two', 'three', 'Buy', '', '', '']]
    출력:
        - 의미 | 데이터 타입 | 예시
        - 전부 비어있지 않은 list의 row의 비어 있지 않은 첫번째 col 번호 | int | 2
    Note:
        -
    """
    for j in range(0, len(data)):
        for i, v in enumerate(flatten_list(data)[j::len(data[0])]):
            if v != '':
                return j + 1

def get_filled_dict(data=[[]], header=0):
    """
    기능: list들의 list에서 전부 비어있지 않은 row에서 비어있지 않은 첫번째 col의 번호를 구함
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - data || list들의 list || list | [[]] | [['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', 'one', '', '', '', '', '', ''], ['', '03-01-1900', 'two', 'three', 'Buy', '', '', '']]
        - header || 공백 열 제거 후 header 열의 상대 위치 || int | 0 | 1 -> 다음 행(heade가 row 2개를 차지?)
    출력:
        - 의미 | 데이터 타입 | 예시
        - | int | 2
    Note:
        -
    """
    """
    Brief: find first filled col
    Args: 
        data = ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', 'one', '', '', '', '', '', ''], ['', '03-01-1900', 'two', 'three', 'Buy', '', '', '']
        header : 공백 열 제거 후 header 열의 상대 위치(ex: 1 -> 다음 행)
    Returns: 2
    """
    return list_to_dict([v[find_first_filled_col(data)-1:] for v in remove_empty_list(data)][header:])



data = [['', '', '', '', '', '', '', ''], ['', 'super1', 'super2', '', '', 'super3', '', 'super4'], ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'], ['', '03-01-1900', 'two', 'three', 'Buy', '', '', ''], ['', '04-01-1999', 'two', 'three', 'Buy', '', '', ''], ['', '05-01-2010', '-', '+', ',', '#', '', '@']]
d = get_filled_dict(data=data, header=1)
print(d)