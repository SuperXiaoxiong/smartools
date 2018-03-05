# -*- coding: utf-8 -*-
# @Time    : 2017/12/19 19:17
# @Author  : Superxx
# @File    : es_.py
# @Desc    :


import requests
import json
import os
import re
import time
from gevent.pool import Pool
import multiprocessing

def get_target(test=0):
    '''
    返回测试或者生产环境auth、url和index_info
    :param test: 是否为测试环境
    :return: (auth, index_url)
    '''
    if test == 1:
        auth = ('user', 'test_password')
        url = 'http://url_test/vul_di/'
        index_info = '{"index":{"_index":"vul_di","_type":"user_data"}}\n'
    else:
        auth = ('user','work_password')
        url = 'http://url_work/combo_list/'
        index_info = '{"index":{"_index":"combo_list","_type":"user_data"}}\n'
    return (auth, url, index_info)


def get_auth(test=0):
    '''
    返回登录凭证basic auth
    :param test: 是否使用测试账号
    :return: 账号auth
    '''
    if test == 1:
        auth = ('user', 'test_password')
    else:
        auth = ('user','work_password')

    return auth


def get_index_url(test=0):
    '''
    获取索引
    :param test: 是否使用测试索引
    :return: 返回索引url
    '''
    if test == 1:
        url = 'http://url_test/vul_di/'
    else:
        url = 'http://url_work/combo_list/'

    return url


def get_req():
    req = requests.session()
    return  req


def get_index(test=0):
    '''
    获取索引
    :param test:是否使用测试索引
    :return: 返回索引
    '''
    if test == 1:
        index_info = '{"index":{"_index":"vul_di","_type":"user_data"}}\n'
    else:
        index_info = '{"index":{"_index":"combo_list","_type":"user_data"}}\n'

    return index_info


def get_file(filepath, file_list):
    '''
    获取给定目录下的文件列表，递归完成
    :param filepath:给定目录
    :param file_list: 文件列表
    :return: 文件列表
    '''
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            get_file(fi_d, file_list)
        else:
            file_list.append(os.path.join(filepath, fi_d))

    return file_list


def handle_file(filename, req):
    '''
    上传单个文件，单条上传
    :param filename:文件名， req:request句柄
    :return:None
    '''

    f = open(filename,'rb')
    iter_f = iter(f)
    for line in iter_f:
        try:

            _line = re.split(":|;", line, maxsplit=1 )
            account = _line[0]
            password = _line[1].strip('\n')

            _account = account.split("@",  1)
            username = _account[0]
            domain = _account[1]

            user_dict = {
                "username": username,
                "email": account,
                "password": password,
                "domain": domain,
                "info": "1.4 billion"
            }
            req.post("http://url_test/vul_di/user_data", data=json.dumps(user_dict), auth=('user', 'test_password'))

        except :
            pass
    f.close()


def del_type(req, test=1):
    '''
    删除整个type
    :return: None
    '''
    data = {
        "query": {
            "match_all": {
            }
        }
    }
    auth, url, index_info = get_target(test)
    url = url + 'user_data/_delete_by_query?conflicts=proceed'
    res = req.post(url, data=json.dumps(data), auth=auth)
    print res.content


def del_documets(req):
    '''
    删除单个文档
    :return: None
    '''
    data = {
        "query": {"match_all": {
            '_id': 'AWCLZ_ntBWnuOPYRIOgr?pretty'
        }}
    }
    url = get_index_url(1)
    url = url + 'user_data/_delete_by_query?conflicts=proceed'
    res = req.post(url, data=json.dumps(data), auth=get_auth(1))
    print res.content


def update_bulk(filename, url, req, test):
    '''
    对单个文件上传，3000条数据一个bulk
    :param filename:
    :param url:
    :param req:
    :return:
    '''
    f = open(filename, 'rb')
    iter_f = iter(f)
    count = 0
    data_str = ''
    auth, url_no, index_info = get_target(test)
    for line in iter_f:
        try:
            _line = re.split(":|;", line, maxsplit=1)
            account = _line[0]
            password = _line[1].strip('\n')
            _account = account.split("@", 1)
            username = _account[0]
            domain = _account[1]

            user_dict = {
                    "username": username,
                    "email": account,
                    "password": password,
                    "domain": domain,
                    "info": "test_speed10"

            }

            data_str = data_str + index_info + (json.dumps(user_dict)) + '\n'

            if count == 1500:
                res = req.post(url, data=data_str, auth=auth)
                data_str = ''
                count = 0
            count = count + 1
        except:
            pass
    f.close()
    req.post(url, data=data_str, auth=auth)


def update_gevent_pool(item):
    filelist = item
    test = 1
    auth, url, index_info = get_target(test)
    update_url = url + 'user_data/_bulk'
    req = requests.Session()
    update_bulk(filelist, update_url, req, test)


def update_process_pool(item):
    filelist = item
    test = 1
    auth, url, index_info = get_target(test)
    update_url = url + 'user_data/_bulk'
    req = requests.Session()
    update_bulk(filelist, update_url, req, test)

def post_data(req, test):
    auth, url, index_info = get_target(test)
    url = url + 'user_data/'
    user_dict = {
        "username": "test1111",
        "email": "test@testcom",
        "password": "test",
        "domain": "test.com",
        "info": "1.4_billion"
    }
    res = req.post(url=url, data=json.dumps(user_dict), auth=auth)
    print res.content


def query_resturl(req):
    url = get_index_url(0)
    url = url + '/_search?q=010&pretty'
    res = req.get(url, auth=get_auth(0))
    print res.content


def query_restdata(req):

    url = get_index_url(0)
    url = url + 'user_data/_search?pretty'
    '''
    match_all 查询用来匹配所有文档
    match 派出搜索查询
    from 参数 规定了返回从这个参数开始的文件索引。默认为0
    size 不指定，默认为10
    sort  指定参数 降序排序  需要设置filedata=true
    _source 表示文档所有部分, _source列表中部分表示选中的列  "_source": ["email", "password"]
    "query": {
            "match": {"username":"word1 word2"}
        },       //查询username含有word1或者word2
        
    布尔查询
    "query": {
        "bool": {
            "must": [
                    { "match": { "address": "mill" } },
                    { "match": { "address": "lane" } }
            ],
            "filter": {
                "range": {
                      "balance": {
                        "gte": 20000,
                        "lte": 30000
                      }
                }
            } //filter 设置过滤范围
        }
    }
    multi_match //在多个字段上执行相同的match 查询
    {
        "multi_match": {
            "query":    "full text search",
            "fields":   [ "title", "body" ]
        }
    }
    '''

    '''
    #聚合查询
    data_dict = {

        "from": 0,
        "size": 100,

       "aggs": {
           "group_by_domain":{
               "terms":{
                   "field":"domain",
               }

           }
       }

    }
   '''
    data_dict = {
        "from": 0,
        "size": 20000,
        "query": {
                    "match": {"username":"ga"}
        },



    }

    #print json.dumps(data_dict)
    res = req.get(url, data = json.dumps(data_dict), auth = get_auth(0))
    #print res.content
    data_ = json.loads(res.content)
    data_ = data_["hits"]
    list_ = data_["hits"]
    count = 0
    for item in list_:
        #print len(item['_source']['username'])
        if len(item['_source']['username']) == 7 and item['_source']['username'][0] == 'g' and item['_source']['domain'] == 'yahoo.com':
            print item
            count = count + 1

    print count


def group_init(req, param):
    '''
    设置参数fielddata属性，只有字段fielddata为true才可以进行聚合操作
    :param req:requests
    :param param:字段
    :return:
    '''
    url = get_index_url(0)
    url = url + '_mapping/user_data'
    data_dict = {
        "user_data":{
            "properties":{
                param:{
                    "type": "text",
                    "fielddata": "true"
                }
            }
        }
    }
    res = req.put(url = url, data = json.dumps(data_dict), auth = get_auth(0))
    print res.content


def group_query(req, param):
    url = get_index_url(0)
    url = url + 'user_data/_search?pretty'
    data_dict = {
        "query":{
            "query_string":{
                "query":"*"
            }
        },
        "size":0,
        "aggs": {
            "group_by_param": {
                "terms": {
                    "field": "password.keyword",
                    "size": 100,
                    "order": {
                            "_count": "desc"
                    }
                }
            }
        }
    }
    res = req.get(url=url, data=json.dumps(data_dict), auth=get_auth(0))
    print res.content


def distinct_query(req, field, test):
    auth, url, index_info = get_target(test)
    url = url + 'user_data/_search?pretty'
    data_dict = {
        "query": {
            "query_string": {
                "query": "*"
            }
        },
        "size": 0,
        "aggs": {
            "distinct_param": {
                "cardinality": {
                    "field": field
                }
            }
        }
    }

    res = req.get(url=url, data=json.dumps(data_dict), auth=auth)
    print res.content


def main():
    filedir = 'D:/data/BreachCompilation/data/0'

    #update_bulk()
    file_list = []
    file_list = get_file(filedir, file_list)
    #print len(file_list)
    #for item in file_list:
        #update_bulk(item)
    #update_bulk(file_list)
    pool = multiprocessing.Pool(8)
    pool.map(update_process_pool, file_list)
    req = get_req()
    #del_type(req, 1)
    #del_data(req)
    #query_restdata(req)
    #group_init(req, "password")
    #group_query(req, "password")
    #distinct_query(req, "username.keyword", 0)
    #post_data(req)
    #update(filename)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print "完成时间: %f s" % (end - start)