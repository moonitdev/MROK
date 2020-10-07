# -*- coding:utf-8 -*-
from datetime import date, timedelta, datetime
import time


##@@ brief:: 
##@@ note:: bgn=start time, gap=int, unit=[sec]) / time formate '%Y%m%d%H%M'
def add_datetime(bgn='', gap=300, f='%Y%m%d%H%M'):
    """
    기능: 
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - 
        - 
    출력:
        - 의미 | 데이터 타입 | 예시
        - 
    Note:
        -
    """
    base = datetime.strptime(bgn, f) if type(bgn) is str else bgn
    return base + timedelta(seconds=gap)


def add_timedelta_to_now(td, f='%Y-%m-%d %H:%M:%S'):
    return (datetime.utcnow() + datetime_to_timedelta(time_str=td)).strftime(f)


def gap_datetime(end='', bgn='', f='%Y%m%d%H%M'):
    _bgn = datetime.strptime(bgn, f) if type(bgn) is str else bgn
    _end = datetime.strptime(end, f) if type(end) is str else end
    return int((_end - _bgn).total_seconds())


def convert_time_to_sec(t='', f='%H:%M:%S'):
    base = datetime.strptime(bgn, f) if type(bgn) is str else bgn
    return base + timedelta(seconds=gap)


def datetime_to_timedelta(time_str='5d 14:22:33', f='%H:%M:%S'):
    time_arr = time_str.split('d ')

    if len(time_arr) > 1:
        time_arr2 = time_arr[1].split(':')
        if len(time_arr2) > 2:
            td = timedelta(days=int(time_arr[0]), hours=int(time_arr2[0]), minutes=int(time_arr2[1]), seconds=int(time_arr2[2]))
        elif len(time_arr2) > 1:
            td = timedelta(days=int(time_arr[0]), minutes=int(time_arr2[0]), seconds=int(time_arr2[1]))
    else:
        time_arr2 = time_str.split(':')
        if len(time_arr2) > 2:
            td = timedelta(hours=int(time_arr2[0]), minutes=int(time_arr2[1]), seconds=int(time_arr2[2]))
        elif len(time_arr2) > 1:
            td = timedelta(minutes=int(time_arr2[0]), seconds=int(time_arr2[1]))

    return td


##@@ brief:: 
##@@ note:: string: default format ['%Y%m%d%H%M'] -> datetime
def string_to_time(s, f='%Y%m%d%H%M'):
    return datetime.strptime(s, f)