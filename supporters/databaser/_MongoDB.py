# -*- coding:utf-8 -*-
##@@@@========================================================================
##@@@@ Libraries

##@@@-------------------------------------------------------------------------
##@@@ Basic Libraries
import json
import sys
import os
import re

##@@@-------------------------------------------------------------------------
##@@@ Installed(conda/pip) Libraries
import pymongo
from pymongo import MongoClient
from pymongo import UpdateOne

##@@@-------------------------------------------------------------------------
##@@@ User Libraries
from constants_mongo import *
from functions_basic import *

##@@@@========================================================================
##@@@@ Constants

##@@@-------------------------------------------------------------------------
##@@@ From:: constants_mongo.py

##@@ database client 생성
mongo = {db: MongoClient(MG['host'], MG['port'])[db] for db in MG['db']}

##@@@-------------------------------------------------------------------------
##@@@ From:: here itself

##@@ default collection
DEFAULT_COL = 'bids_service'


##@@@@========================================================================
##@@@@ Functions

##@@@-------------------------------------------------------------------------
##@@@ Utils:: CRUD(Create-Read-Update-Delete)

##@@ brief:: insert single document to (mongo)db
##@@ note:: 
def insert_doc(doc={}, col=DEFAULT_COL, db=MG['db'][0]):
  try:
    mongo[db][col].insert_one(doc)
  except:
    log = {'error': 'insert_doc'}
    insert_log(log)
    sys.exit(1)


##@@ brief:: insert documents to col in db
##@@ note:: error 처리 정교화 필요 [*****]
def insert_docs(docs=[], col=DEFAULT_COL, db=MG['db'][0]):
  try:
    mongo[db][col].insert_many(docs)
  except:
    log = {'error': 'insert_docs'}
    insert_log(log)
    sys.exit(1)


##@@ brief:: insert json(list/dict) to db
##@@ note:: 
def insert_json(data, col=DEFAULT_COL, db=MG['db'][0]):
  if type(data) is list:
    insert_docs(data, col, db)
  elif type(data) is dict:
    insert_doc(data, col, db)
  else:
    return False


##@@ brief:: upsert(insert/update) data to where(find filter)
##@@ note:: _up: upsert=_up
def upsert_doc(query={}, doc={}, col=DEFAULT_COL, db=MG['db'][0]):
  try:
    mongo[db][col].update_one(query, {"$set": doc}, upsert=True)
  except:
    log = {'error': 'upsert_doc'}
    insert_log(log)
    sys.exit(1)


##@@ brief:: upsert(insert/update) data to keys value is matched
##@@ note:: 
def upsert_docs(keys=[], docs=[], col=DEFAULT_COL, db=MG['db'][0]):
  for doc in docs:
    query = {}
    for key in keys:
      try:
        query[key] = doc[key]
        upsert_doc(query, doc, col, db)
      except:
        log = {'error': 'upsert_docs'}
        insert_log(log)
        sys.exit(1)


# ##@@ brief:: upsert(insert/update) data to where(find filter)
# ##@@ note:: _up: upsert=_up
# def upsert_doc(query={}, doc={}, col=DEFAULT_COL, db=MG['db'][0], _up=True):
#   try:
#     mongo[db][col].update_one(query, {"$set": doc}, upsert=_up)
#   except:
#     log = {'error': 'upsert_doc'}
#     insert_log(log)


# ##@@ brief:: upsert(insert/update) data to keys value is matched
# ##@@ note:: 
# def upsert_docs(keys=[], docs=[], col=DEFAULT_COL, db=MG['db'][0], _up=True):
#   for doc in docs:
#     query = {}
#     for key in keys:
#       try:
#         query[key] = doc[key]
#         upsert_doc(query, doc, col, db, _up)
#       except:
#         log = {'error': 'upsert_docs'}
#         insert_log(log)



##@@ brief:: upsert dictionary(json) to db
##@@ note:: keys for query
def upsert_json(data, keys=[], col=DEFAULT_COL, db=MG['db'][0]):
  if type(data) is list:
    upsert_docs(keys, data, col, db)
  elif type(data) is dict:
    upsert_doc({}, data, col, db)  # [*****] 수정 필요
  else:
    return False


##@@ brief:: update data to keys value is matched
##@@ note:: 
def update_docs(keys=[], docs=[], col=DEFAULT_COL, db=MG['db'][0]):
  for doc in docs:
    query = {}
    for key in keys:
      try:
        query[key] = doc[key]
        update_doc(query, doc, col, db)
      except:
        log = {'error': 'upsert_docs'}
        insert_log(log)
        sys.exit(1)


##@@ brief:: update one data to query is matched
##@@ note:: 
def update_doc(query={}, doc={}, col=DEFAULT_COL, db=MG['db'][0]):
  try:
    mongo[db][col].update_one(query, {"$set": doc}, upsert=False)
  except:
    log = {'error': 'upsert_doc'}
    insert_log(log)
    sys.exit(1)


##@@ brief:: update multiple for query(filter) / doc(upate)
##@@ note:: 
def update_multi(query={}, doc={}, col=DEFAULT_COL, db=MG['db'][0]):
  mongo[db][col].update(query, {"$set": doc}, multi=True)


##@@ brief:: find doc matched query and show in project(ion)
##@@ note:: 
def find_doc(query={}, project={}, col=DEFAULT_COL, db=MG['db'][0]):
  return mongo[db][col].find_one(query, project)


##@@ brief:: find docs matched query and show in project(ion)
##@@ note:: 
def find_docs(query={}, project={}, col=DEFAULT_COL, db=MG['db'][0]):
  if not project:
    return list(mongo[db][col].find(query))
  else:
    return list(mongo[db][col].find(query, project))


##@@ brief:: find docs if exists or not
##@@ note:: Useless??
def find_docs_exists(query={}, project={}, col=DEFAULT_COL, db=MG['db'][0]):
  _query = {}
  if 'e' in query:
    for exist in query['e']:
      _query.update({exist: {'$exists': True}})
  if 'n' in query:
    for notexist in query['n']:
      _query.update({notexist: {'$exists': False}})

  return list(mongo[db][col].find(_query, project))


##@@ brief:: find first doc(ument) sorted docs
##@@ note:: .sort([("field1", pymongo.ASCENDING), ("field2", pymongo.DESCENDING)])
##@@        pymongo.ASCENDING: 1, pymongo.DESCENDING: -1
def find_doc_sort(query={}, project={}, sort=[()], col=DEFAULT_COL, db=MG['db'][0]):
  docs = list(mongo[db][col].find(query, project).sort(sort).limit(1))
  if len(docs) > 0:
    #print(docs)
    return docs[0]
  else:
    return []


##@@ brief:: find docs and sort
##@@ note:: .sort([("field1", pymongo.ASCENDING), ("field2", pymongo.DESCENDING)])
##@@        pymongo.ASCENDING: 1, pymongo.DESCENDING: -1
def find_docs_sort(query={}, project={}, sort=[()], col=DEFAULT_COL, db=MG['db'][0]):
  return list(mongo[db][col].find(query, project).sort(sort))


##@@ brief:: find distinct docs for tag
##@@ note:: .distinct([("field1", pymongo.ASCENDING), ("field2", 
def find_docs_disctinct(query={}, tag='', col=DEFAULT_COL, db=MG['db'][0]):
  return list(mongo[db][col].find(query).distinct(tag))


##@@ brief:: count docs
##@@ note:: 
def count_docs(query={}, col=DEFAULT_COL, db=MG['db'][0]):
  return mongo[db][col].find(query).count()


##@@ brief:: delete doc matched query
##@@ note:: 
def delete_docs(query={}, col=DEFAULT_COL, db=MG['db'][0]):
  mongo[db][col].delete_many(query)
  #db.drop_collection(col)


##@@ brief:: delete doc matched query
##@@ note:: 
def delete_doc(query={}, col=DEFAULT_COL, db=MG['db'][0]):
  mongo[db][col].delete_one(query)
  #db.drop_collection(col)


##@@ brief:: drop collection
##@@ note:: 
def drop_col(col=DEFAULT_COL, db=MG['db'][0]):
  mongo[db].drop_collection(col)


##@@ brief:: drop database
##@@ note:: 
def drop_db(db=MG['db'][0]):
  client.drop_database(name)


##@@ brief:: collection backup to json file
##@@ note:: #mongoexport --db test --collection traffic --out traffic.json
def collection_to_json(col='', path='', db=MG['db'][0]):
  json_to_file(find_docs({}, None, col, db), path)


##@@ brief:: bids data backup to json file by date
##@@ note:: 
def backup_bids_to_json(opts={'bgn':'', 'end':''}, col='bids_service', path='', db=MG['db'][0]):
  _bgn = datetime.strptime(opts['bgn'], '%Y%m%d%H%M')
  query = {'bidNtceDt': {'$gte':_bgn}}
  path += 'bids_service_' + opts['bgn']

  if 'end' in opts:
    _end = datetime.strptime(opts['end'], '%Y%m%d%H%M')
    query = {'bidNtceDt': {'$gte':_bgn, '$lt':_end}}
    path += '_' + opts['end']

  json_to_file(find_docs(query, None, col, db), path)

##@@@-------------------------------------------------------------------------
##@@@ Utils:: Aggregate

##@@ brief:: drop database
##@@ note:: distinct multiple keys
# collection = db.tb;
# result = collection.aggregate( 
#             [
#                 {"$group": { "_id": { market: "$market", code: "$code" } } }
#             ]
#         );
# printjson(result);




##@@@-------------------------------------------------------------------------
##@@@ Utils:: Query / Projection

##@@ brief:: set query $and, $or, $not
##@@ note:: 
def set_query_and_or_not(opts={'$and':[{}], '$or':[{}], '$not':[{}]}):
  return {k: [q for q in qs] for k, qs in opts.items()}


##@@ brief:: set upsert query from data dictionary and pks list
##@@ note:: Useless??
def set_query_upsert(data={}, pks=['']):
  return { k : data[k] for k in pks }


##@@ brief:: query for 조달청 또는 나라장터 자체 공고건
##@@ note:: 
def query_inner_bid():
  return {'rgstTyNm': '조달청 또는 나라장터 자체 공고건'}


##@@ brief:: set projection {'_id':0, 'f1':1, ...}
##@@ note:: 
def set_projection_no_id(ps=['']):
  return {**{'_id':0}, **{p:1 for p in ps}}


##@@ brief:: set upsert docs from data dictionary and pks list if v != '' and v != '0'
##@@ note:: Useless??
def set_doc_no_nulls(data={}, pks=[''], nulls=['']):
  return { k : v for k, v in data.items() if not k in pks and not v in nulls}


##@@ brief:: merge queries
##@@ note:: Useless??
def merge_queries(opts=[{}]):
  pass


##@@@-------------------------------------------------------------------------
##@@@ Settings:: User

##@@ brief:: create super user
##@@ note:: 
def create_super_user(doc={'id':'_super_', 'pw':'_Super_1!', 'lv':10}):
  pass


##@@ brief:: create user at db
##@@ note:: 
def create_user(doc={'id':'_super_', 'pw':'_Super_1!', 'lv':1}, db='', col='users'):
  pass


##@@@-------------------------------------------------------------------------
##@@@ Settings:: View / Index

##@@ brief:: create view for col(lection) in db
##@@ note:: 
def create_view(pipe=[], view='bids_notice_view', col=DEFAULT_COL, db=MG['db'][0]):
  mongo[db].command({
      "create": view,
      "viewOn": col, 
      "pipeline": pipe
  })


##@@ brief:: create index for col(lection) in db
##@@ note:: 
def create_view_prj(prj={}, view='bids_notice_view', col=DEFAULT_COL, db=MG['db'][0]):
  mongo[db].command({
      "create": view,
      "viewOn": col, 
      "pipeline": [
        {
          "$project": prj
        }
      ]
  })


##@@ brief:: create unique index for db collection
##@@ note:: create_index(keys, session=None, **kwargs)
def create_index_unique(keys='bidNtceNo', col=DEFAULT_COL, db=MG['db'][0]):
  if type(keys) is str:
    mongo[db][col].create_index(keys, unique=True)
  elif type(keys) is tuple:
    mongo[db][col].create_index([keys], unique=True)
  elif type(keys) is list:
    if type(keys[0]) is tuple:
      mongo[db][col].create_index(keys, unique=True)
    elif type(keys[0]) is str:
      _keys = []
      for key in keys:
        _keys.append((key, -1))
      mongo[db][col].create_index(_keys, unique=True)


##@@ brief:: drop (all) indexes for db collection
##@@ note:: Useless??
def drop_indexes(col=DEFAULT_COL, db=MG['db'][0]):
  mongo[db][col].drop_indexes()


##@@@-------------------------------------------------------------------------
##@@@ Settings:: Create Collection



##@@@-------------------------------------------------------------------------
##@@@ Publics:: bid_helper > users

##@@ brief:: find user keys for search bids
##@@ note:: Useless??
def find_user_keys(id=''):
  print(find_doc({'id':id}, {'_id':0, 'keys':1}, 'users', db=MG['db'][0]))
  return find_doc({'id':id}, {'_id':0, 'keys':1}, 'users', db=MG['db'][0])


##@@ brief:: find user infos
##@@ note:: Useless??
def find_user_info(id='', project=[]):
  return find_doc({'id':id}, set_projection_no_id(project), 'users', db=MG['db'][0])


##@@@-------------------------------------------------------------------------
##@@@ Publics:: bidhelper > log

## @func :: insert log data
## @note :: 
def insert_log(log, col='log_fetch_bids', db=MG['db'][0]):
  insert_doc(log, col, db)


## @func :: insert log data
## @note :: 
def update_log(query, log, col='log_fetch_bids', db=MG['db'][0]):
  update_doc(query, log, col, db)

##@@@-------------------------------------------------------------------------
##@@@ Publics:: bidhelper > find

##@@ brief:: find api request spec[req/res] from info_api_spec by title keyword
##@@ note:: 
def find_api_spec_by_title(opts={'k':{'INC':[], 'EXC':[]}, 'p':['']}):
  query = {"title": {"$regex" : re.compile(set_search_regex(opts['k']))}}
  return find_docs(query, set_projection_no_id(opts['p']), 'view_info_api_specs', 'bidhelper')


##@@ brief:: find fetch all usages
##@@ note:: _order < 6 : notice / _order > 10 : by bidNtceNo
def find_api_usages(task=''):
  prj = set_projection_no_id(['title', 'url', '_req', '_save', '_remark', '_order'])
  return find_docs_sort({'task':task, '_fetch':1}, prj, [('_order', 1)], 'api_usages')


##@@ brief:: find fetch usage
##@@ note:: 
def find_api_usage(url):
  prj = set_projection_no_id(['title', '_req', '_save', '_remark'])
  return find_doc_sort({'url':url}, prj, [('_order', 1)], 'api_usages')


##@@ brief:: find bids
##@@ note:: {'$and':[{'OpengCompt':{'$exists':0}}, {'opengDt':{'$lt': datetime.now()}}]}
##@@        inqryEndDt += 60sec ?? [*****] 확인 필요
##@@        외부 입찰 제외 query 추가("rgstTyNm" : "조달청 또는 나라장터 자체 공고건") [*****] 확인 필요
##@@        재입찰: {'rbidRsn':{'$exists':0}} // 유찰: {'nobidRsn':{'$exists':0}}
def find_bids_for_fetch(inqryDt={}, query={'$and':[{'OpengCompt':{'$exists':0}}, {'rgstTyNm': '조달청 또는 나라장터 자체 공고건'}, {'opengDt':{'$lt': datetime.now()}}]}):
  inqry = [datetime.strptime(v, '%Y%m%d%H%M') for k, v in inqryDt.items()]
  query['$and'].append({'bidNtceDt': {'$gte':inqry[0], '$lt':inqry[1] + timedelta(minutes=1)}})
  return find_docs(set_query_and_or_not(query), {'_id':0, 'bidNtceNo':1}, 'bids_service')


##@@ brief:: find bids by progrsDiv("개찰완료", "유찰", "재입찰")
##@@ note:: {'$and':[{'OpengCompt':{'$exists':0}}, {'opengDt':{'$lt': datetime.now()}}]}
##@@        inqryEndDt += 60sec ?? [*****] 확인 필요
# def find_bids_by_progrsDiv(inqryDt={}, query={'$and':[{'progrsDivCdNm':'개찰완료'}]}):
#   inqry = [datetime.strptime(v, '%Y%m%d%H%M') for k, v in inqryDt.items()]
#   query['$and'].append({'bidNtceDt': {'$gte':inqry[0], '$lt':inqry[1] + timedelta(minutes=1)}})
#   return find_docs(set_query_and_or_not(query), {'_id':0, 'bidNtceNo':1}, 'bids_service')


##@@ brief:: find bids by progrsDiv("개찰완료") 중 개찰상세내역('OpengCompt')이 없는 입찰 건 재요청 [***]
##@@ note:: {'$and':[{'OpengCompt':{'$exists':0}}, {'opengDt':{'$lt': datetime.now()}}]}
##@@        inqryEndDt += 60sec ?? [*****] 확인 필요
def find_bids_by_progrsDiv_backup(inqryDt={}):
  bgn = datetime.strptime(inqryDt['inqryBgnDt'], '%Y%m%d%H%M')
  end = datetime.strptime(inqryDt['inqryEndDt'], '%Y%m%d%H%M')
  query={'$and':[{'OpengCompt':{'$exists':0}}, {'progrsDivCdNm':'개찰완료'}, {'bidNtceDt': {'$gte':bgn, '$lt':end}}]}

  #print(query)
  return find_docs(query, {'_id':0, 'bidNtceNo':1}, 'bids_service')


##@@ brief:: find bids by progrsDiv("개찰완료") 중 개찰상세내역('OpengCompt')이 없는 입찰 건 재요청 [***]
##@@ note:: {'$and':[{'OpengCompt':{'$exists':0}}, {'opengDt':{'$lt': datetime.now()}}]}
##@@        inqryEndDt += 60sec ?? [*****] 확인 필요
def find_bids_by_progrsDiv_auto(inqryDt={}):
  bgn = datetime.strptime(inqryDt['inqryBgnDt'], '%Y%m%d%H%M')
  end = datetime.strptime(inqryDt['inqryEndDt'], '%Y%m%d%H%M')
  query={'$and':[{'OpengCompt':{'$exists':0}}, {'progrsDivCdNm':'개찰완료'}, {'opengDt': {'$gte':bgn, '$lt':end}}]}

  #print(query)
  return find_docs(query, {'_id':0, 'bidNtceNo':1}, 'bids_service')


##@@ brief:: find bids for preprice : 예비가격 fetch용
##@@ note:: {'$and':[{'OpengCompt':{'$exists':0}}, {'opengDt':{'$lt': datetime.now()}}]}
##@@        inqryEndDt += 60sec ?? [*****] 확인 필요
def find_bids_for_preprice(inqryDt={}):
  bgn = datetime.strptime(inqryDt['inqryBgnDt'], '%Y%m%d%H%M')
  end = datetime.strptime(inqryDt['inqryEndDt'], '%Y%m%d%H%M')
  query={'$and':[{'OpengCompt':{'$exists':1}}, {'ServcPreparPcDetail':{'$exists':0}}, {'bidNtceDt': {'$gte':bgn, '$lt':end}}]}
  #query={'$and':[{'OpengCompt':{'$exists':1}}, {'ServcPreparPcDetail':{'$exists':0}}, {'rgstTyNm':'조달청 또는 나라장터 자체 공고건'}, {'bidNtceDt': {'$gte':bgn, '$lt':end}}]}
  #'sucsfbidMthdNm':'제한최저'
  # db.view_bid_2018_results_en.distinct('sucsfbidMthdNm', {'$and':[{'OpengCompt':{'$exists':1}}, {'ServcPreparPcDetail':{'$exists':1}}]})

  #print(query)
  #return find_docs(query, {'_id':0, 'bidNtceNo':1}, 'bids_service')
  docs = find_docs(query, {'_id':0, 'bidNtceNo':1}, 'bids_service_2018')
  print('len: {}, end: {}'.format(len(docs), inqryDt['inqryEndDt']))
  if len(docs):
    print(docs)
  return docs


##@@ brief:: find bids by {'$and':[{'OpengCompt':{'$exists':1}}, {'sucsfbidAmt':{'$exists':0}}]}
##@@ note:: 
def find_bids_no_sucsData(inqryDt={}):
  bgn = datetime.strptime(inqryDt['inqryBgnDt'], '%Y%m%d%H%M')
  end = datetime.strptime(inqryDt['inqryEndDt'], '%Y%m%d%H%M')
  #query={'$and':[{'OpengCompt':{'$exists':1}}, {'sucsfbidAmt':{'$exists':0}}, {'bidNtceDt': {'$gte':bgn, '$lt':end}}]}
  query={'$and':[{'OpengCompt':{'$exists':1}}, {'sucsfbidAmt':{'$exists':0}}]}

  #print(query)
  return find_docs(query, {'_id':0, 'bidNtceNo':1}, 'bids_service')


##@@ brief:: 임시 bidNtceOrd 수정용 [*****]
##@@ note:: 
def update_bids_by_OpengCompt():
  docs = find_docs({'OpengCompt':{'$exists':1}}, {'_id':0, 'bidNtceNo':1, 'opengRsltDivNm':1, 'bidClsfcNo':1, 'rbidNo':1,'OpengCompt':1}, 'bids_service_0301_0420')

  json_to_file(docs, "../_files/opengCompt.json")

  update_docs(['bidNtceNo'], docs, 'bids_service_0301_0411_2')

  #print(query)
  #return find_docs(query, {'_id':0, 'bidNtceNo':1, 'OpengCompt'}, 'bids_service')


##@@ brief:: find bids
##@@ note:: 
def find_bids_by_search(query={'$and':[{'OpengCompt':{'$exists':0}}, {'rgstTyNm': '조달청 또는 나라장터 자체 공고건'}, {'opengDt':{'$lt': datetime.now()}}]}):
  return find_docs(set_query_and_or_not(query), {'_id':0, 'bidNtceNo':1}, 'bids_service')


##@@ brief:: find bid results (for fetch / for send info [****])
##@@ note:: 개찰시간: 2일전 ~ 현재 [******] / log 기록에 따라...
def find_bids_result_not_yet(query={'$and':[{'progrsDivCdNm':{'$exists':0}}, {'rgstTyNm': '조달청 또는 나라장터 자체 공고건'}, {'opengDt':{'$lte': datetime.now(), '$gte': add_datetime(datetime.now(), -3600*24*2)}}]}):
  return find_docs(set_query_and_or_not(query), {'_id':0, 'bidNtceNo':1, 'opengDt':1}, 'bids_service')
  #return find_docs(set_query_and_or_not(query), {'_id':0, 'bidNtceNo':1, 'opengDt':1}, 'bids_service')


##@@@-------------------------------------------------------------------------
##@@@ Publics:: bidhelper > find for send info


##@@ brief:: find response info for date data
##@@ note:: 각종 시간 정보 (init_settings.py)
def find_bid_notice_for_send():
  pass



  # _bgn = datetime.strptime(opts['bgn'], '%Y%m%d%H%M')
  # query = {'bidNtceDt': {'$gte':_bgn}}
  # path += 'bids_service_' + opts['bgn']

  # if 'end' in opts:
  #   _end = datetime.strptime(opts['end'], '%Y%m%d%H%M')
  #   query = {'bidNtceDt': {'$gte':_bgn, '$lt':_end}}
  #   path += '_' + opts['end']
##@@@-------------------------------------------------------------------------
##@@@ Publics:: bidhelper > find for init settings


##@@ brief:: find response info for date data
##@@ note:: 각종 시간 정보 (init_settings.py)
def find_res_type_datetime():
  return list(find_docs({'d_type':'date'}, {'_id':0, 'res_en':1, 'res_ko':1, 'd_type':1}, 'specs_res'))


##@@ brief:: find response info for int / long / float data
##@@ note:: 각종 가격/금액/ (init_settings.py)
def find_res_type_number():
  #find_docs({'$or':[{'d_type':'int'}, {'d_type':'long'}, {'d_type':'float'}]}, {'_id':0, 'res_en':1, 'd_type':1}, 'specs_res')
  return list(find_docs({'$or':[{'d_type':'int'}, {'d_type':'long'}, {'d_type':'float'}]}, {'_id':0, 'res_en':1, 'res_ko':1, 'd_type':1}, 'specs_res'))


# ## get api request spec[req/res] from info_api_spec
# ## k(eys)  / p(rojection)
# def find_api_spec_by_title(opts={'k':{'AND':[], 'OR':[], 'NOT':[]}, 'p':['']}):
#   query = {"title": {"$regex" : re.compile(get_regex_search(opts['k']))}}
#   projection = {'_id':0}
#   projection.update({v:1 for v in opts['p']})

#   return find_docs(query, projection, DB_VIEWS['스펙'], DEFAULT_DB)



##@@ brief:: find all specs [*****] Not Yet @@@@@@@@@@
##@@ note:: info_api_specs / view_info_api_specs
##       opts={'query':{'res':}, 'project':{''}}
def find_api_specs():
  #find_docs({}, {'_id':0, 'res':1, 'title':1, })
  #info_api_specs
  pass

  #return specs


##@@ brief:: delete bids_service documents by (lessthan) date
##@@ note:: info_api_specs / view_info_api_specs
def delete_bids_service_by_date(lt='201801010000'):
  opts={'$lt':datetime.strptime(lt, '%Y%m%d%H%M')}
  delete_docs({'bidNtceDt':opts}, 'bids_service')


##@@ brief:: delete bids_service documents by (lessthan) date
##@@ note:: info_api_specs / view_info_api_specs
def delete_bids_service_by_date2(lt='201801010000'):
  opts={'$lt':datetime.strptime(lt, '%Y%m%d%H%M')}
  delete_docs({'rgstDt':opts}, 'bids_service')
#----------------------------------
# util functions
#----------------------------------
#-------------------------------
# save data to db / file
#-------------------------------
# opts
#  'to': 'mongo' / 'json' / 
#  'up': 'insert' / 'upsert' / 'update' / ...
#  'pks': ['bidNtceNo', 'bidNtceOrd'] 유일성 식별 필드
#  'path': '../_files/fetched1.json'
def save_data(data, opts={'col':'bids', 'to':'mongo', 'up':'insert', 'pks':['bidNtceNo', 'bidNtceOrd']}):
  #col = opts['col'] or 'bids'
  col = 'bids' if not 'col' in opts else opts['col']

  # 파일로 저장
  if opts['to'] == 'json':
    if 'path' in opts:
      json_to_file(data, opts['path'])
    else:
      return False

  # mongodb에 저장(insert/upsert)
  elif opts['to'] == 'mongo':
    if not 'up' in opts or opts['up'] == 'insert':
      insert_docs(col, data['items'])
    elif opts['up'] == 'upsert':
      for datum in data['items']:
        rs = upsert_doc(col, set_upsert_filter(datum, opts['pks']), set_upsert_doc(datum, opts['pks']))
        #{"n": 1, "nModified": 0, "upserted": {"$oid": "5ca03d14163561899a992514"}, "ok": 1.0, "updatedExisting": false}
        #{"n": 1, "nModified": 1, "ok": 1.0, "updatedExisting": true}
        #{"n": 1, "nModified": 0, "ok": 1.0, "updatedExisting": true}
    elif opts['up'] == 'update':
      pass



##@@@@========================================================================
##@@@@ Main Function (for test)

if __name__ == '__main__':
  # r = find_doc_sort({}, {'_id':0, 'title':1}, [('division', -1)], 'info_api_specs')
  # print(r)
  #r = find_bids_for_fetch({'inqryBgnDt':'201903060900', 'inqryEndDt':'201903060919'})
  # r = find_bids_by_progrsDiv_re({'inqryBgnDt': '201801021200', 'inqryEndDt': '201801021800'})
  # print(r)

  #r = find_user_keys('ilmaceng')
  # r = find_doc({'id':'ilmaceng'}, {'_id':0, 'notification':1}, 'users', 'bid_helper')


  #opts = {'k': {'INC':['공고 용역', '지역정보', '면허'], 'EXC':['나라장터', '구매대상']}, 'p': ['url', 'req_en', 'title']}
  # opts = {'k': {'INC':['용역', '개찰결과 개찰완료', '재입찰', '유찰'], 'EXC':['나라장터', '구매대상', '공고']}, 'p': ['url', 'req_en', 'title']}
  # #opts = {'INC':['용역', '지역정보', '면허'], 'EXC':['나라장터', '구매대상']}
  # r = find_api_spec_by_title(opts)
  # print(len(r))

  #r = find_bids_result_not_yet()
  #print(r)
  #collection_to_json('bids_service', '/Volumes/data/dev/SynologyDrive/projects/_mongo_bk/bids_service_20190101_0502.json')
  #backup_bids_to_json(opts={'bgn':'201904010000'}, col='bids_service', path='/Volumes/data/dev/SynologyDrive/projects/_mongo_bk/', db=MG['db'][0])
  r = find_bids_for_preprice({'inqryBgnDt':'201801010000', 'inqryEndDt':'201801040000'})
  print(r)


"""
# @@@@@@@@@@
## aggregate

### project


### match


"""


'''

# Requires pymongo 3.6.0+
from pymongo import MongoClient

client = MongoClient("mongodb://host:port/")
database = client["bidhelper"]
collection = database["info_bidnotice"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

pipeline = [
    {
        u"$project": {
            u"_id": 0.0,
            u"url": u"$summary.\uC694\uCCAD\uC8FC\uC18C",
            u"req": u"$req.\uD56D\uBAA9\uBA85(\uC601\uBB38)",
            u"res": u"$res.\uD56D\uBAA9\uBA85(\uC601\uBB38)"
        }
    }
]

cursor = collection.aggregate(
    pipeline, 
    allowDiskUse = False
)
try:
    for doc in cursor:
finally:
    client.close()


db.info_bidnotice.aggregate([
    { "$project": {
        "_id": 0,
        "url": "$summary.요청주소",
        "req": "$req.항목명(영문)",
        "res": "$res.항목명(영문)"
    }}
])
'''




"""
operations = [
    UpdateOne({ "field1": 1},{ "$push": { "vals": 1 } },upsert=True),
    UpdateOne({ "field1": 1},{ "$push": { "vals": 2 } },upsert=True),
    UpdateOne({ "field1": 1},{ "$push": { "vals": 3 } },upsert=True)
]

result = collection.bulk_write(operations)



## insert

### result
WriteResult({
   "nInserted" : 1,
   "writeConcernError" : {
      "code" : 64,
      "errmsg" : "waiting for replication timed out at shard-a"
   }
})

## update


### result
WriteResult({
   "nMatched" : 1,
   "nUpserted" : 0,
   "nModified" : 1,
   "writeConcernError" : {
      "code" : 64,
      "errmsg" : "waiting for replication timed out at shard-a"
   }
})

?
print(rs.nMatched)




db.people.findAndModify({
  query: { name : "Andy" },
  sort: { rating : 1 },
  update: { $inc : { score: 1 } },
  upsert: true
})

db.update({"_id": acs_num}, {"$set": mydata}, upsert = True)

db.monsters.update({ name: 'Slime' }, { $set: { hp: 30 } })
s
db.noticeList.find({"dminsttNm" : "충청남도교육청 충청남도공주교육지원청"}, {"resultList":1})



docs = collection.find({"student_id": {"$gt":90}})

>>> d1 = dict(d.items()[len(d)/2:])
>>> d2 = dict(d.items()[:len(d)/2])


{ students: { $elemMatch: { school: 102 } } }

{ resultList: { $elemMatch: {"prcbdrCeoNm" : "이선근"} }}
db.noticeList.find({ resultList: { $elemMatch: {"prcbdrCeoNm" : '문정일'} }})

db.noticeList.find({ resultList: { $elemMatch: {"opengRank" : 1, "prcbdrCeoNm" : '문정일'} }})
db.noticeList.find({ resultList: { $elemMatch: {"opengRank" : 1, "prcbdrCeoNm" : '문정일'} }}).count()

db.noticeList.find({ resultList: { $elemMatch: {"opengRank" : 1, "prcbdrCeoNm" : "이선근"} }}).count()

db.noticeList.find({ "resultList" : { $elemMatch: {"opengRank" : 1, "bidprcAmt": { $gt: 68200000} }}}).count()

db.noticeList.find({"resultList": {$not: {$size: 0}}})

db.noticeList.find({"resultList": {"$not": {"$size": 0}}}, {"bidNtceNo" : 1, "bidNtceOrd" : 1})


"""
