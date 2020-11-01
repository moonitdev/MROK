import os, sys
import configparser
import json
import gspread  ## google drive gspread
from oauth2client.service_account import ServiceAccountCredentials  ## googledrive 인증
#sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'functions')) ## Note: 부모 디렉토리 기준 상대 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), '../functions')) ## Note: 현재 디렉토리 기준 상대 경로 설정
from dataFns import ( list_to_dict, flatten_list, remove_empty_list )  ## (사용자) 상용 함수 라이브러리


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
    def __init__(self, url, sheet):
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
        self.json = os.path.join(_path, config['GOOLEDRIVE']['json'])
        self.scopes = config['GOOLEDRIVE']['scopes'].split(',')
        self.urls = json.loads(config['GOOLEDRIVE']['urls'])
        # self.user = config['GOOLEDRIVE']['user']

        ## Google Drive Spreadsheet 접속 인증, client 생성
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json, self.scopes)
        self.gc = gspread.authorize(credentials)
        self.file = self.gc.open_by_url(self.urls[url])
        self.sheet = self.file.worksheet(sheet)


    def set_file(self, url=''):
        """
        기능: url(이름)에 해당하는 spreadsheet를 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - url || google spread 파일 url 이름[self.urls의 key값] || str | 'ROK_SETTINGS' | 'ROK_SETTINGS'
        Note:
            - 
        """
        self.file = self.gc.open_by_url(self.urls[url])


    def set_sheet(self, sheet=''):
        """
        기능: url(이름), sheet(이름)에 해당하는 spreadsheet의 sheet를 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - url || google spread 파일 url 이름[self.urls의 key값] || str | 'ROK_SETTINGS' | 'ROK_SETTINGS'
            - sheet || sheet 이름 | str | 'test' | 'test'
        Note:
            - 
        """
        self.sheet = self.file.worksheet(sheet)


    def get_dicts_from_sheet(self, header=0):
        """
        기능: sheet로 부터, dict 배열 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - header || 공백 열 제거 후 header 열의 상대 위치 || int | 0 | 1 -> 2번째 row(header가 row 2개를 차지?)
        출력:
            - 의미 | 데이터 타입 | 예시
            - 해당 sheet의 비어있지 않은 row들 dict 배열 | list(of dict) | [{'h1':'c11', 'h2':'c12'}, {'h2':'c21', 'h2':'c22'}, ...]
        Note:
            - 
        """
        return get_filled_dicts(self.sheet.get_all_values(), header)


    def get_header_col(self, header_row=1, key=''):
        """
        기능: key에 해당하는 header의 열번호를 출력
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - header_row || 해더행 번호 | int | 1 | 1(첫번째 행)
            - key || 해더(필드) 이름 | str | '' | 'header1'
        출력:
            - 의미 | 데이터 타입 | 예시
            - header의 열번호 | int | 5 : 5번째 열
        Note:
            - 
        """
        header_map = self.get_header_map(header_row=header_row)
        for k, v in header_map.items():
            if k == key:
                return v
        return False


    def get_header_map(self, header_row=1):
        """
        기능: url(이름), sheet(이름)에 해당하는 spreadsheet의 sheet에서 header 행(row)의 매핑 딕셔너리({'header1':1, 'header2':2, ...}, key->해더이름, val->열번호)를 반환(해더 빈값 열 제외)
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - header_row || 해더행 번호 | int | 1 | 1(첫번째 행)
        출력:
            - 의미 | 데이터 타입 | 예시
            - 해더행 매핑 딕셔너리 | dict | {'A1': 1, 'B1': 2, 'C1': 3, 'D1': 4}
        Note:
            - 빈값 열 제거 필요!!
        """
        headers = self.sheet.row_values(header_row)
        cols = [i for i in range(1, len(headers) + 1)]
        j = 0
        empty_headers = []

        for i, header in enumerate(headers):
            if header == '':
                empty_headers.append(i)

        for i in empty_headers:
            headers.pop(i-j)
            cols.pop(i-j)
            j += 1

        return dict(zip(headers, cols))


    def read_sheet(self, data_type='dicts'):
        """
        기능: url(이름), sheet(이름)에 해당하는 spreadsheet의 sheet를 data_type형식으로 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - data_type || 출력 데이터 타입 | str | 'dicts' | 'lists'(list of list)
        출력:
            - 의미 | 데이터 타입 | 예시
            - data_type형식의 데이터 | lists -> list(of dict) / dicts -> list(of list) | [[]] / [{}]
        Note:
            - 
        """
        data = self.sheet.get_all_values()
        if data_type == 'dicts':
            data = list_to_dict(data)
        return data


    def write_sheet(self, dicts=[{}], data_type='dicts', new=False):
        """
        기능: sheet에 dicts 데이터를 저장
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
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
        self.file.values_append(self.sheet, {'valueInputOption': 'USER_ENTERED'}, {'values': put_values})


    def share_sheet(self, email='', perm_type='user', role='writer'):
        """
        기능: url의 spreadsheet을 email의 사용자에게 공유
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - email || 이메일 | str | '' | 'deverlife@gmail.com'
            - perm_type || 공유 타입 | str | 'user' | 'user':
            - role || 역할 | str | 'writer' | 'writer': 
        Note:
            - 
        """
        self.file.share(email=email, perm_type=perm_type, role=role)


    def create_header(self, headers=[], header_row=1, first_col=1):
        """
        기능: url의 spreadsheet에 header를 생성
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - sheet || sheet 이름 | str | 'test' | 'test'
            - header_row || 해더 행번호 | int | 1 | 1: 첫번째 행에 해더를 만듬
            - first_col || 해더 시작 열 | int | 1 | 1: 첫번째 열부터 해더값을 넣음
        Note:
            - 
        """
        for i, v in enumerate(headers):
            self.sheet.update_cell(header_row, i+1, v)


    def create_sheet(self, sheet='test', rows=100, cols=20):
        """
        기능: url의 spreadsheet에 sheet이름의 sheet를 생성
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - sheet || sheet 이름 | str | 'test' | 'test'
            - rows || 행 갯수 | int | 100 | 행 갯수 100
            - cols || 열 갯수 | int | 100 | 열 갯수 20
        Note:
            - 
        """
        self.file.add_worksheet(title=sheet, rows=rows, cols=cols)


    def insert_sheet_row(self, data={}, header_row=1):
        """
        기능: url의 spreadsheet에 sheet에 data를 추가
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - data || 추가할 데이터 | dict | {} | {'header1':'contents1', 'header2':'contents2'}
            - header_row || 해더행 번호 | int | 1 | 1: 첫번째 행이 해더행
        Note:
            - 
        """
        ws = self.sheet
        header_map = self.get_header_map(header_row=header_row)
        update_row = len(ws.get_all_values()) + 1

        for k, v in data.items():
            col = header_map[k]
            ws.update_cell(update_row, col, v)


    def insert_sheet_rows(self, dicts=[{}], header_row=1):
        """
        기능: url의 spreadsheet에 sheet에 data를 추가
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - data || 추가할 데이터 | list(of dict) | [{}] | [{'header1':'contents11', 'header2':'contents12'}, {'header1':'contents21', 'header2':'contents22'}]
            - header_row || 해더행 번호 | int | 1 | 1: 첫번째 행이 해더행
        Note:
            - 
        """
        ws = self.sheet
        header_map = self.get_header_map(header_row=header_row)
        last_row = len(ws.get_all_values())

        for data in dicts:
            last_row += 1
            print('last_row: {}'.format(last_row))
            for k, v in data.items():
                col = header_map[k]
                print('col: {}'.format(col))
                ws.update_cell(last_row, col, v)


    def read_sheet_row(self, row=2, header_row=1):
        """
        기능: url의 spreadsheet에 sheet이름의 sheet의 row번째 행 데이터를 dictionary로 반환 
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - row || 반환할 행번호 | int | 2 | 2: 두번째 행 데이터 반환
            - header_row || 해더행 번호 | int | 1 | 1: 첫번째 행이 해더행
        Note:
            - 
        """
        ws = self.sheet
        header_map = self.get_header_map(header_row=header_row)
        
        result = {}
        for k, v in header_map.items():
            val = ws.cell(row, v).value
            if val != '':
                result[k] = ws.cell(row, v).value

        return result


    def read_sheet_rows(self, first_row=None, header_row=1):
        """
        기능: url의 spreadsheet에 sheet이름의 sheet의 데이터를 list(of dict)를 반환 
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - first_row || (내용) 첫번째 행번호 | int | None | 
            - header_row || 해더행 번호 | int | 1 | 1: 첫번째 행이 해더행
        Note:
            - 
        """
        ws = self.sheet
        header_map = self.get_header_map(header_row=header_row)
        last_row = len(ws.get_all_values())
        if not first_row:
            first_row = header_row + 1

        results = []
        for row in range(first_row, last_row + 1):
            result = {}
            for k, v in header_map.items():
                val = ws.cell(row, v).value
                if val != '':
                    result[k] = val
            results.append(result)

        return results


    def find_cell(self, val='', regex=False):
        """
        기능: url의 spreadsheet의 sheet에서 val값을 갖는 cell을 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - val || 찾고자 하는 셀의 내용 | str | '' | 
        Note:
            - 
        """
        return self.sheet.find(val)

    @staticmethod
    def _find_cells(ws=None, val='', regex=False):
        """
        기능: url의 spreadsheet의 sheet에서 val값을 갖는 cell들을 모두 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - ws || worksheet || object | None | worksheet
            - val || 찾고자 하는 셀들의 내용 | str | '' | 
        Note:
            - 
        """
        results = []
        for cell in ws.findall(val):
            results.append([cell.row, cell.col])
        return results


    def find_cells(self, val='', regex=False):
        """
        기능: url의 spreadsheet의 sheet에서 val값을 갖는 cell들을 모두 반환
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - val || 찾고자 하는 셀들의 내용 | str | '' | 
        출력:
            - 의미 | 데이터 타입 | 예시
            - val값을 갖는 cell[행, 열]들 | list(of list) | [[2, 5], [4, 5], [5, 5], [6, 5], [8, 5]]
        Note:
            - 
        """
        return self._find_cells(ws=self.sheet, val=val, regex=regex)


    # def update_sheet_row(self, match={}, data={}, header_row=1):
    #     """
    #     기능: match 조건에 맞는 행의 내용을 data값으로 변경
    #     입력:
    #         - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
    #         - match || 변경할 행 일치 조건 | dict | {} | {'header1':'contents1', 'header2':'contents2'}
    #         - data || 변경할 데이터 | dict | {} | {'header3':'contents3', 'header4':'contents4'}
    #         - header_row || 해더행 번호 | int | 1 | 1: 첫번째 행이 해더행
    #     Note:
    #         - 
    #     """
    #     ws = self.sheet
    #     for v in match:
    #         matches = ws.findall(val)
    #     find_cells(self, url='ROK_SETTINGS', sheet='test', val='', regex=False):

    #     header_map = self.get_header_map(header_row=header_row)
    #     update_row = len(ws.get_all_values()) + 1

    #     for k, v in data.items():
    #         col = header_map[k]
    #         ws.update_cell(update_row, col, v)


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
    spread = GoogleSpread(url='ROK_LOGS', sheet='test1')
    # dicts = spread.get_dicts_from_sheet(header=0)
    # print('dicts: {}'.format(dicts))
    # header_map = spread.get_header_map(header_row=1)
    # print('header map: {}'.format(header_map))

    # data = {'B1': 'B~~!~~', 'A1': 'A~~~!~', 'D1': 'D~!~~'}
    # spread.insert_sheet_row(data=data, header_row=1)
    # dicts = [
    #     {'C1':'C~', 'B1': 'B~~!~~', 'A1': 'A~~~!~', 'D1': 'D~!~~'},
    #     {'B1': 'B~~!!~~', 'A1': 'A~~~!!~', 'D1': 'D~!~'},
    #     {'B1': 'B~~!!!~~', 'A1': 'A~~~!~'}
    # ]
    # spread.insert_sheet_rows(dicts=dicts, header_row=1)

    # row = spread.read_sheet_row(row=3, header_row=1)
    # print(row)

    # rows = spread.read_sheet_rows(header_row=1)
    # print(rows)

    # spread.create_sheet(sheet='test4')

    # spread.set_sheet(sheet='test4')

    # spread.create_header(headers=['header1', 'header2', 'header3', 'header4'], header_row=1, first_col=1)

    # dicts = [
    #     {'header1': 'contents11', 'header2': 'contents12', 'header3': 'contents13', 'header4':'contents14'},
    #     {'header1': 'contents21', 'header2': 'contents22', 'header3': 'contents23', 'header4':'contents24'},
    #     {'header1': 'contents31', 'header2': 'contents32', 'header3': 'contents33', 'header4':'contents34'},
    #     {'header1': 'contents41', 'header3': 'contents43', 'header4':'contents44'}
    # ]
    # spread.insert_sheet_rows(dicts=dicts, header_row=1)

    # cell = spread.find_cell(val='contents33', regex=False)
    # print(cell.row, cell.col)

    cells = spread.find_cells(val='A~~~!~', regex=False)
    print(cells)
