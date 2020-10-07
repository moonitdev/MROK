import os, sys
import copy
from lxml.html import fromstring
#from lxml import etree
from dataFns import *


def get_xml(source='', xpath=None):
    """
    기능: source가 str이면 xml class로 변경, source에 대한 xpath에 해당하는 xml element 반환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - source || str 또는 xml 형식의 html | str / <class 'lxml.html.HtmlElement'> | '' | '<html><body>test</body></html>'
        - xpath || element를 지정하는 xpath | str | None | './/div[@id="test"]
    출력:
        - 의미 | 데이터 타입 | 예시
        - xpath에 해당하는 xml element 반환 | <class 'lxml.html.HtmlElement'> | <Element html at 0x279e5fa0b88>
    """
    if type(source) is str:
        xml = fromstring(source)
        # print('xml in get_xml: {}'.format(xml))
    else:
        xml = source
    if xpath is not None:
        # xml = fromstring(source).xpath(xpath)
        xml = xml.xpath(xpath)

    return xml


def get_xml_node(source='', xpath=None, all=False):
    """
    기능:
        - source가 str이면 xml class로 변경
        - source[xml]의 xpath에 해당하는 xml element node 반환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - source || str 또는 xml 형식의 html | str / <class 'lxml.html.HtmlElement'> | '' | '<html><body>test</body></html>'
        - xpath || element를 지정하는 xpath | str | None | './/div[@id="test"]
        - all || 자손 node 전부 포함 여부 | bool | False | True -> 자식 node만 찾음
    출력:
        - 의미 | 데이터 타입 | 예시
        - xml element node | <class 'list'> | [<Element thead at 0x1588a377228>, <Element tbody at 0x1588a377278>, ..]
    """
    if all: added = '//node()'
    else: added = '/node()'
    return get_xml(source).xpath(xpath + added)


def get_xml_text(source='', xpath=None, all=False):
    """
    기능:
        - source가 str이면 xml class로 변경
        - source[xml]의 xpath에 해당하는 xml element text요소 반환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - source || str 또는 xml 형식의 html | str / <class 'lxml.html.HtmlElement'> | '' | '<html><body>test</body></html>'
        - xpath || element를 지정하는 xpath | str | None | './/div[@id="test"]
        - all || 자손 text 전부 포함 여부 | bool | False | True -> 자식 text만 찾음
    출력:
        - 의미 | 데이터 타입 | 예시
        - xml element text요소 | list | ['text1', 'text2', ..]
    """
    if all: added = '//text()'
    else: added = '/text()'

    # out = ''
    # for xml in list(get_xml(source)):
    #     out = out + xml.xpath(xpath + added)
    return get_xml(source).xpath(xpath + added)


def get_xml_text_edit(source='', xpath=None, all=False, editor=None, edit_opts=None):
    """
    기능:
        - source가 str이면 xml class로 변경
        - source[xml]의 xpath에 해당하는 xml element text요소 반환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - source || str 또는 xml 형식의 html | str / <class 'lxml.html.HtmlElement'> | '' | '<html><body>test</body></html>'
        - xpath || element를 지정하는 xpath | str | None | './/div[@id="test"]
        - all || 자손 text 전부 포함 여부 | bool | False | True -> 자식 text만 찾음
    출력:
        - 의미 | 데이터 타입 | 예시
        - xml element text요소 | list | ['text1', 'text2', ..]
    """
    if all: added = '//text()'
    else: added = '/text()'

    txt = get_xml(source).xpath(xpath + added)
    if editor:
        txt = editor(txt, edit_opts)
    return txt


def get_xml_table(table=None, opts={'is_header':True, 'default_header':[], 'thead': './/tr//th', 'row': './/tr', 'cell':'.//td', 'out': {'type': 'csv', 'separator':',', 'newline':'|'}}):
    """
    기능:
        - table의 row, cell 요소들을 배열([[h1, h2, h3, ...], [c11, c12, c13, ...], [c21, c22, c23, ...]])로 반환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - table || table의 xml node | <class 'lxml.html.HtmlElement'> | '' | <Element table at 0x1e4c2ea4318>
        - opts || table 변환 옵션 | dict | {'xpath':None, 'header':True, '_header':[], 'thead': './/tr//th', 'row': './/tr', 'cell':'.//td', 'out_type': 'csv'} | 디폴트값 참조
        - opts['is_header'] || 테이블 타이틀 존재 여부 | bool | True | False -> 타이틀(헤더)이 없는 테이블
        - opts['default_header'] || 테이블 헤더 디폴트 값 | list | [] -> 디폴트 값 (필요)없음
        - opts['thead'] || 해당 테이블 헤더의 xpath | str | './/tr//th' | './/tr//th'
        - opts['row'] || 해당 테이블 내용[tbody] 안에 있는 테이블 행의 xpath | str | './/tr' | './/tr//th'
        - opts['cell'] || 해당 테이블 행[tbody/tr] 안에 있는 셀의 xpath | str | './/td' | './/td'
        - opts['output'] || 반환 형식 지정 | dict | {'type': 'csv', 'separator':',', 'newline':'|'} | 디폴트값 참조
    출력:
        - 의미 | 데이터 타입 | 예시
        - xml element text요소 | list | ['text1', 'text2', ..]
    Note:
        - <div> 태그로 이루어진 테이블 등에 대한 응용 테스트 필요
        - 'markdown/json/..' 등의 opts['output'] 구현 필요
    """
    table_res = []
    headers = []

    # print('table: {}, type(table): {}'.format(table, type(table)))

    if opts['thead'] is not None:
        headers = get_xml_text(table, opts['thead'], all=True)
        # print('headers: {}'.format(headers))

    if len(opts['default_header']) > 1:
        headers = opts['default_header']

    if len(headers) > 1:
        table_res.append(headers)

    start_row = 1
    if not opts['is_header']:
        start_row = 0

    for row in table.xpath(opts['row'])[start_row:]:
        cells = []
        for cell in row.xpath(".//td"):
            # cells.append('_'.join(cell.text_content().split()))
            cells.append(cell.text_content())

        table_res.append(cells)

    return table_res


def get_xml_tables(source='', users=None, defaults={'...':{'is_header':True, 'default_header':[], 'thead': './/tr//th', 'row': './/tr', 'cell':'.//td', 'out': {'type': 'csv', 'separator':',', 'newline':'|'}}}):
    """
    기능:
        - source가 str이면 xml class로 변경
        - source[xml] 내에 있는 table들을 지정 옵션(여러 옵션 = users, 단일 옵션 = defualts)으로 반환
        - 테이블 순번에 해당하는 옵션 지정 가능('...': 전체, '1...5': table[1]~table[5], '3,4,7': table[3], table[4], table[7])
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - source || str 또는 xml 형식의 html | str / <class 'lxml.html.HtmlElement'> | '' | '<html><body>test</body></html>'
        - users || 테이블 변환 옵션 | dict | None | {'0,1,8,9':{opts1}, '2...7':{opts2}}
            - users[key] : 옵션을 적용할 테이블 순번 | str | None | ('...': 전체, '1...5': table[1]~table[5], '3,4,7': table[3], table[4], table[7])
        - opts || table 변환 옵션 | dict | {'...':{'is_header':True, 'default_header':[], 'thead': './/tr//th', 'row': './/tr', 'cell':'.//td', 'out': {'type': 'csv', 'separator':',', 'newline':'|'}}} | 디폴트값 참조
        -
    출력:
        - 의미 | 데이터 타입 | 예시
        - 옵션 형식으로 변환된 테이블 | str | 옵션에 따라 다름
    Note:
        - users 옵션 지정 숙지 필요(테이블에 따른 입력/변환 옵션을 미리 테스트 해봐야 함)
    """
    if users is not None:
        defaults = users

    tables = get_xml(source=source, xpath='.//table')
    #print('type(tables): {}, len(tables): {}'.format(type(tables), len(tables)))

    no_of_table = len(tables)
    table_nos = list(defaults.keys())
    table_opts = list(defaults.values())

    for i, table_no in enumerate(table_nos):
        if table_no == '...':
            table_nos = ['_' + '_,_'.join([str(j) for j in range(0, no_of_table)]) + '_']
            break
        elif '...' in table_no:
            start_end = table_no.split('...')
            table_nos[i] = '_' + '_,_'.join([str(j) for j in range(int(start_end[0]), int(start_end[1])  + 1)]) + '_'
        elif ',' in table_no:
            table_nos[i] = '_' + '_,_'.join([str(j) for j in table_no.split(',')]) + '_'

    #print(table_nos)
    tables_res = []
    for i, table in enumerate(tables):
        for j, table_no in enumerate(table_nos):
            if '_' + str(i) + '_' in table_no:
                # print('\n[ {} ]------------------------------------------\n'.format(i))
                table_res = get_xml_table(table, table_opts[j])
                # print(table_res)
                tables_res.append(table_res)
                break

    return tables_res


# def fork_elem_tables(source='', xpath=None, header=['필드', '설명', '타입']):
#     if type(source) is str:
#         tables = fromstring(source).xpath(xpath)

#     for table in tables:
#         table_res = []
#         column_headers = table.xpath(".//tr//th/text()")

#         _header = True
#         if not header[0] in column_headers: ## Note: header가 없는 경우
#             _header = False
#             _cell1 = column_headers
#             column_headers = header

#         for row in table.xpath(".//tr")[1:]:
#             cells = []
#             if _header is False:
#                 cells = _cell1
#             for i, cell in enumerate(row.xpath(".//td")):
#                 cells.append(' '.join(cell.text_content().split()))

#             table_res.append({k: v for k, v in zip(column_headers, cells)})
#         tables_res.append(table_res)
#     return tables_res


# def fork_all_tables(source='', xpath=None):
#     tables = fromstring(source).xpath('//table')
#     result = []
#     for table in tables:
#         table_res = []
#         column_headers = table.xpath(".//tr//th/text()")
#         for row in table.xpath(".//tr")[1:]:
#             cells = []
#             for i, cell in enumerate(row.xpath(".//td")):
#                 cells.append(' '.join(cell.text_content().split()))
#             table_res.append({k: v for k, v in zip(column_headers, cells)})
#         result.append(table_res)
#     return result


def fork_links(source='', xpath=None):
    """
    기능:
        - source가 str이면 xml class로 변경
        - source[xml]의 xpath에 해당하는 link
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - source || str 또는 xml 형식의 html | str / <class 'lxml.html.HtmlElement'> | '' | '<html><body>test</body></html>'
        - xpath || element를 지정하는 xpath | str | None | '//img[@src]'
        - 'LINKS' : {'html': '//a[@href]', 'img': '//img[@src]', 'js': '//script[@src]', 'css': '//link[@href]', 'multi': '//source[@src]'}
    출력:
        - 의미 | 데이터 타입 | 예시
        - xpath에 해당하는 link값 배열 | list | ['./images/img001.gif', './images/img002.gif', ..]
    Note:
        - xpath는 '//a[@href]' 와 같은 형식을 유지해야 함. 특히, '@' 와 ']' 사이에 attribute가 꼭 들어가야 함
        - 원래 link값, down받기 위한 link값, local 페이지로 전환하기 위한 link값 조정이 필요
    """
    links = []
    for link in get_xml(source).xpath(xpath):
        links.append(link.get(xpath.split('@')[1][:-1]))
    return links


# def yield_texts_dicts(self, url=None, source=None, opts_texts=None):
#     if url==None: url=self.url
#     if source==None: source=self.fetch(url)
#     if type(source) != str:
#         source=self.fetch(url).text
#     if opts_texts==None: opts_texts=self.opts['PIECES']['texts']

#     return {name: "\n".join(self.fork_elem_text(source=source, xpath=xpath)) for name, xpath in opts_texts.items()}


# def yield_tables_dicts(self, url=None, source=None, opts_tables=None):
#     if url==None: url=self.url
#     if source==None: source=self.fetch(url)
#     if type(source) != str:
#         source=self.fetch(url).text
#     if opts_tables==None: opts_tables=self.opts['PIECES']['tables']

#     tables = {}
#     for key, xpath in opts_tables.items():
#         ts = self.fork_elem_tables(source=source, xpath=xpath)
#         # print(len(ts))
#         names = key.split(',')
#         # print('names: {}, ts: {}'.format(names, ts))
#         if len(ts) == 1: ## bithumb docs 용(table이 1개 일 때, 2번째 이름으로...)
#             tables.update({names[1]: ts[0]})
#         else:
#             for i, k in enumerate(ts):
#                 tables.update({names[i]: ts[i]})
#     return tables


# def yield_texts_csv(self, url=None, source=None, opts_texts=None, separator="\t", header=False):
#     texts = self.yield_texts_dicts(url=url, source=source, opts_texts=opts_texts)
#     return dict_to_csv(dt=texts, separator=separator, header=header)


# def yield_tables_csv(self, url=None, source=None, opts_tables=None, separator="\t", header=True):
#     tables = self.yield_tables_dicts(url=url, source=source, opts_tables=opts_tables)
#     return dict_to_csv(dt=tables, separator=separator, header=header)


# ## test용
# def save_texts_csv(self, url=None, source=None, opts_texts=None, separator="\t", header=True):
#     print('save_texts_csv: {}'.format(self.yield_texts_csv()))
#     write_file(path='test.csv', data=self.yield_texts_csv())


# ## test용
# def save_tables_csv(self, url=None, source=None, opts_tables=None, separator="\t", header=True):
#     write_file(path='test.csv', data=self.yield_tables_csv())


# def yield_links_dicts(self, url=None, source=None, opts_links=None):
#     if url==None: url=self.url
#     if source==None: source=self.fetch(url)
#     if type(source) != str:
#         source=self.fetch(url).text
#     if opts_links==None: opts_links=self.opts['LINKS']

#     return {name: self.fork_links(source=source, xpath=xpath) for name, xpath in opts_links.items()}


if __name__ == '__main__':
    _path = os.path.dirname(__file__)
    _path = os.path.join(_path, os.path.abspath('../../_downloads'), 'test.html')
    # print(_path)

    with open(_path, 'rt', encoding='UTF8') as f:
        source = f.read()

    opts = {
        '__name':  './/header//h2',
        '_name': 'test',
        'current': './/div[@class="hub-reference"]',
        'outer': './/div[contains(@class, \"content-body"\)]',
        'depth': 1,
        'elems': [
            {
                '_name': 'title',
                'current': ".//header//h2",
                'depth': 2,
                'in': 'text',
                'out': {
                    'type': 'txt'
                }
            },
            {
                '_name': 'description',
                'current': ".//header//div[contains(@class, \"markdown-body\")]//p",
                'in': 'text',
                'depth': 2,
                'out': {
                    'type': 'txt'
                }
            },
            {
                '_name': 'method',
                'current': ".//span[contains(@class, \"pg-type-big\")]",
                'in': 'text',
                'depth': 2,
                'out': {
                    'type': 'txt'
                }
            },
            {
                '_name': 'url',
                'current': ".//span[@class=\"api-text\"]",
                'in': 'text',
                'depth': 2,
                'out': {
                    'type': 'txt'
                }
            },
            {
                '_name': 'params',
                'name': './/div[@class=\"param-type-header\"]/h3',
                'current': ".//form[contains(@id, \"form-header\")]",
                'in': 'text',
                'depth': 2,
                'out': {
                    'type': 'txt'
                }
            },
        ]
    }


    def get_dict_elem_keys(d, condition, keys, out):
        if condition(d):
            out.append(tuple(copy.deepcopy(keys)))
        else:
            for i, elem in enumerate(d['elems']):
                print('parent: {}'.format(d['_name']))
                if '_name' in elem:
                    k = elem['_name']
                    print('k: {}, keys: {}'.format(d['_name'], k, keys))
                    if len(keys) > elem['depth']:
                        keys = keys[:elem['depth']]
                        keys.append(k)
                    else:
                        keys.append(k)
                    keys.append(elem['current'])
                get_dict_elem_keys(elem, condition, keys, out)

        return out

    def has_elems(d):
        if not 'elems' in d: return True
        else: return False


    results = get_dict_elem_keys(opts, has_elems, ['test'], [])

    print(results)

    xmls = get_xml(source)
    got = {}

    def set_current_xpath(key):
        return key + "test"

    def set_element_xml(key):
        return xmls.xpath(key)[0].text_content()

    # output = get_xml_out_recursive(source=xmls, opts=opts, out={})
    # print(output)

    for result in results:
        set_dict_elem_callback(got, set_element_xml, *result)

    print('got it: {}'.format(got))



