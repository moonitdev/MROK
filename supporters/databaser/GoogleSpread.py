import os, sys
import configparser
import json
import gspread  ## google drive gspread
from oauth2client.service_account import ServiceAccountCredentials  ## googledrive 인증
#sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'functions')) ## Note: 부모 디렉토리 기준 상대 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), '../functions')) ## Note: 현재 디렉토리 기준 상대 경로 설정
from dataFns import *  ## (사용자) 상용 함수 라이브러리


def find_first_filled_row(data=[[]]):
    """
    기능: list들의 list에서 전부 비어있지 않은 list가 몇 번째 row인지를 구함
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - data || list들의 list || list | [[]] | [['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', 'one', '', '', '', '', '', ''], ['', '03-01-1900', 'two', 'three', 'Buy', '', '', '']]
    출력:
        - 의미 | 데이터 타입 | 예시
        - 전부 비어있지 않은 list의 row 번호 | int | 4
    Note:
        -
    """
    for i, v in enumerate(flatten_list(data)):
        if v != '':
            return (i+1)//len(data[0]) + 1


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


def get_filled_dicts(data=[[]], header=0):
    """
    기능: 비어있는 row들을 제거한 후, header(header = 1이면 2번째 row)를 keys로 하고, 이하의 row들을 values로 하는 dict 배열을 반환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - data || list들의 list || list | [[]] | [['', '', '', '', '', '', '', ''], ['', 'super1', 'super2', '', '', 'super3', '', 'super4'], ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'], ['', '03-01-1900', 'two', 'three', 'Buy', '', '', ''], ['', '04-01-1999', 'two', 'three', 'Buy', '', '', ''], ['', '05-01-2010', '-', '+', ',', '#', '', '@']]
        - header || 공백 열 제거 후 header 열의 상대 위치 || int | 0 | 1 -> 다음 행(header가 row 2개를 차지?)
    출력:
        - 의미 | 데이터 타입 | 예시
        - | 값이 있는 list들, header list를 기준으로 생성한 dict 배열 | list(of dict) | [{'h1': '', 'h2': '03-01-1900', 'h3': 'two', 'h4': 'three', 'h5': 'Buy', 'h6': '', 'h7': '', 'h8': ''}, {'h1': '', 'h2': '04-01-1999', 'h3': 'two', 'h4': 'three', 'h5': 'Buy', 'h6': '', 'h7': '', 'h8': ''}, {'h1': '', 'h2': '05-01-2010', 'h3': '-', 'h4': '+', 'h5': ',', 'h6': '#', 'h7': '', 'h8': '@'}]
    Note:
        - 입력/출력 예시: get_filled_dicts(data=data, header=1)
    """
    return list_to_dict([v[find_first_filled_col(data)-1:] for v in remove_empty_list(data)][header:])


class GoogleSpread:
    """
    기능: GoogleDrive Spreadsheet 사용[gspread래핑(Wrapping)]
    Note:
        - [구글 클라우드 플랫폼](https://console.cloud.google.com/home/)
    """
    def __init__(self):
        """
        기능: GoogleSpread 인스턴스 생성시 실행
            - conf/_config.ini 파일에서 GoogleDrive 접속 정보 로딩
            - 접속 정보를 이용해 GoogleDrive 접속에 사용할 clinet(self.gc) 생성
        Note:
            - 인스턴스 생성시, spread, sheet 지정
            - method들 입력(url, sheet) -> ws
        """
        _path = os.path.dirname(__file__)
        config = configparser.RawConfigParser()
        config.read(os.path.join(_path, 'conf/_config.ini'))
        #self.json = config['GOOLEDRIVE']['json'] ## Note: error(파일 경로를 못찾음!!)
        self.json = os.path.join(_path, config['GOOLEDRIVE']['json'])
        self.scopes = config['GOOLEDRIVE']['scopes'].split(',')
        self.urls = json.loads(config['GOOLEDRIVE']['urls'])
        # self.user = config['GOOLEDRIVE']['user']

        ## Google Drive Spreadsheet 접속 인증, client 생성
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json, self.scopes)
        self.gc = gspread.authorize(credentials)


    def open_url(self, url=''):
        """
        기능: url(이름)에 해당하는 spreadsheet를 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - url || google spread 파일 url 이름[self.urls의 key값] || str | 'ROK_SETTINGS' | 'ROK_SETTINGS'
        Note:
            - 
        """
        return self.gc.open_by_url(self.urls[url])


    def open_sheet(self, url='', sheet=''):
        """
        기능: url(이름), sheet(이름)에 해당하는 spreadsheet의 sheet를 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - url || google spread 파일 url 이름[self.urls의 key값] || str | 'ROK_SETTINGS' | 'ROK_SETTINGS'
            - sheet || sheet 이름 | str | 'test' | 'test'
        Note:
            - 
        """
        return self.gc.open_by_url(self.urls[url]).worksheet(sheet)


    def get_dicts_from_sheet(self, url='ROK_SETTINGS', sheet='test', header=0):
        """
        기능: sheet로 부터, dict 배열 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - url || google spread 파일 url 이름[self.urls의 key값] || str | 'ROK_SETTINGS' | 'ROK_SETTINGS'
            - sheet || sheet 이름 | str | 'test' | 'test'
            - header || 공백 열 제거 후 header 열의 상대 위치 || int | 0 | 1 -> 2번째 row(header가 row 2개를 차지?)
        출력:
            - 의미 | 데이터 타입 | 예시
            - 해당 sheet의 비어있지 않은 row들 dict 배열 | list(of dict) | [{'h1':'c11', 'h2':'c12'}, {'h2':'c21', 'h2':'c22'}, ...]
        Note:
            - 
        """
        return get_filled_dicts(self.open_sheet(url=url, sheet=sheet).get_all_values(), header)


    def get_header_map(self, url='', sheet='', row=1, col=1):
        """
        기능: url(이름), sheet(이름)에 해당하는 spreadsheet의 sheet에서 header 행(row)의 매핑 딕셔너리({'header1':1, 'header2':2, ...}, key->해더이름, val->열번호)를 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - url || google spread 파일 url 이름[self.urls의 key값] || str | 'ROK_SETTINGS' | 'ROK_SETTINGS'
            - sheet || sheet 이름 | str | 'test' | 'test'
            - row || 해더행 번호 | int | 1 | 1(첫번째 행)
            - col || 해더행 시작 열 | int | 1 | 1(첫번째 열)
        출력:
            - 의미 | 데이터 타입 | 예시
            - 해더행 매핑 딕셔너리 | dict | {'A1': 1, 'B1': 2, 'C1': 3, 'D1': 4}
        Note:
            - 
        """
        headers = self.open_sheet(url=url, sheet=sheet).row_values(row)
        cols = [i for i in range(col, col+ len(headers))]
        return dict(zip(headers, cols))


    def read_sheet(self, url='', sheet='', data_type='dicts'):
        """
        기능: url(이름), sheet(이름)에 해당하는 spreadsheet의 sheet를 data_type형식으로 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - url || google spread 파일 url 이름[self.urls의 key값] || str | 'ROK_SETTINGS' | 'ROK_SETTINGS'
            - sheet || sheet 이름 | str | 'test' | 'test'
            - data_type || 출력 데이터 타입 | str | 'dicts' | 'lists'(list of list)
        출력:
            - 의미 | 데이터 타입 | 예시
            - data_type형식의 데이터 | lists -> list(of dict) / dicts -> list(of list) | [[]] / [{}]
        Note:
            - 
        """
        data = self.open_sheet(url=url, sheet=sheet).get_all_values()
        if data_type == 'dicts':
            data = list_to_dict(data)
        return data


    def write_sheet(self, url='ROK_SETTINGS', sheet='test', dicts=[{}], data_type='dicts', new=False):
        """
        기능: sheet에 dicts 데이터를 저장
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - url || google spread 파일 url 이름[self.urls의 key값] || str | 'ROK_SETTINGS' | 'ROK_SETTINGS'
            - sheet || sheet 이름 | str | 'test' | 'test'
            - dicts || 입력 데이터 || list(of dict) | [{}] | [{'action':'action1', 'device':'device1', 'character':'character1', 'time':'time1', 'done':'done1', 'next':'next1'}, {'action':'action2', 'device':'device2', 'character':'character2', 'time':'time2', 'done':'done2', 'next':'next2'}]
            - data_type || 입력 데이터 타입 | str | 'dicts' | 'lists'(list of list)
            - new || 비어있는 sheet 여부 | bool | False | False -> 데이터 추가 / True -> 신규 데이터 입력
        출력:
            - 의미 | 데이터 타입 | 예시
            - 해당 sheet의 비어있지 않은 row들 dict 배열 | list(of dict) | [{'h1':'c11', 'h2':'c12'}, {'h2':'c21', 'h2':'c22'}, ...]
        Note:
            - 
        """
        if data_type == 'lists':
            dicts = list_to_dict(dicts)

        headers = [key for key, val in dicts[0].items()]

        put_values = []

        if new is True:
            put_values.append(headers)
        
        for v in dicts:
            temp = []
            for h in headers:
                temp.append(v[h])
            put_values.append(temp)
        # print(put_values)
        self.open_url(url).values_append(sheet, {'valueInputOption': 'USER_ENTERED'}, {'values': put_values})


    def update_sheet_row(self, url='ROK_SETTINGS', sheet='test', data={}, row=1, col=1):
        ws = self.open_sheet(url=url, sheet=sheet)
        header_map = self.get_header_map(url=url, sheet=sheet, row=row, col=col)
        update_row = len(ws.get_all_values()) + 1

        for k, v in data:
            col = header_map[k]
            ws.update_cell(update_row, col)




# Finding a Cell
# Find a cell matching a string:

# cell = worksheet.find("Dough")

# print("Found something at R%sC%s" % (cell.row, cell.col))
# Find a cell matching a regular expression

# amount_re = re.compile(r'(Big|Enormous) dough')
# cell = worksheet.find(amount_re)



# Updating Cells
# Using A1 notation:

# worksheet.update('B1', 'Bingo!')
# Or row and column coordinates:

# worksheet.update_cell(1, 2, 'Bingo!')
# Update a range

# worksheet.update('A1:B2', [[1, 2], [3, 4]])
# Formatting
# Here’s an example of basic formatting.

# Set A1:B1 text format to bold:

# worksheet.format('A1:B1', {'textFormat': {'bold': True}})
# Color the background of A2:B2 cell range in black, change horizontal alignment, text color and font size:

# worksheet.format("A2:B2", {
#     "backgroundColor": {
#       "red": 0.0,
#       "green": 0.0,
#       "blue": 0.0
#     },
#     "horizontalAlignment": "CENTER",
#     "textFormat": {
#       "foregroundColor": {
#         "red": 1.0,
#         "green": 1.0,
#         "blue": 1.0
#       },
#       "fontSize": 12,
#       "bold": True
#     }
# })



# Using gspread with NumPy
# NumPy is a library for scientific computing in Python. It provides tools for working with high performance multi-dimensional arrays.

# Read contents of a sheet into a NumPy array:

# import numpy as np
# array = np.array(worksheet.get_all_values())
# The code above assumes that your data starts from the first row of the sheet. If you have a hearder row in the first row, you need replace worksheet.get_all_values() with worksheet.get_all_values()[1:].

# Write a NumPy array to a sheet:

# import numpy as np

# array = np.array([[1, 2, 3], [4, 5, 6]])

# # Write the array to worksheet starting from the A2 cell
# worksheet.update('A2', array.tolist())

if __name__ == '__main__':
    spread = GoogleSpread()
    # dicts = spread.get_dicts_from_sheet(url='ROK_LOGS', sheet='test1', header=0)
    # print('dicts: {}'.format(dicts))
    # header_map = spread.get_header_map(url='ROK_LOGS', sheet='test1', row=1, col=1)
    # print('header map: {}'.format(header_map))

    data = {'A1': 'A~~', 'B1': 'B~~', 'C1': 'C~~', 'D1': 'D~~'}
    spread.update_sheet_row(url='ROK_LOGS', sheet='test1', data=data, row=1, col=1)

