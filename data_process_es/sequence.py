# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 10:44
# @Author  : Superxx
# @File    : sequence.py
# @Desc    : 对文件中出现的字符串的次数进行从大到小排序

from collections import OrderedDict, Counter
import heapq


'''
1. hepq.nsmallest模板，取列表中dict最大或者最小的api
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
print cheap
print expensive

2. collections.Counter most_common模块，返回列表中Top([N]) 列表
'''

'''
思路:遍历取出文件内容，直接使用迭代器，再使用Counter.most_common模块
'''
import xlwt
def domain_rank():
    passwd_name_fin = 'C:\Users\i-xiaoxiong\Desktop\www.ansbase5.org'
    passwd_analy_fout = 'C:\Users\i-xiaoxiong\Desktop\www.ansbase5.org.out'
    passwd_fin = open(passwd_name_fin, 'rb')
    #passwd_analy_fout = open(passwd_analy_fout, 'wb')
    ip = []
    passwd_iter = iter(passwd_fin)
    for line in passwd_iter:
        _line = line.split('\t')
        ip.append(_line[1])
    #passwd_lst_counter = Counter(passwd_iter)
    #passwd_lst_counter.
    #for key, value in passwd_lst_counter.most_common(200):
        #print key.strip('\n'), value
        #passwd_analy_fout.write(key.strip('\n') +'\t' +  str(value) + '\n')

    print len(set(ip))
    ip_lst_counter = Counter(ip)
    for key, value in ip_lst_counter.most_common(2000):
        print key.strip('\n'), value
    passwd_fin.close()
    #passwd_analy_fout.close()
domain_rank()


def domaintoexcel():
    data_in = open('D:/data/BreachCompilation/collection/1_domain_analys','rb')
    iter_data = iter(data_in)


    style0 = xlwt.easyxf('font:name Times New Roman, color-index black, bold on', num_format_str='#,##0')
    style1 = xlwt.easyxf('font:name Times New Roman, color-index black, bold on', num_format_str='#,##0.00')


    excel_out = xlwt.Workbook(encoding='utf-8')
    excel_w = excel_out.add_sheet('domain_analysis')
    total_domain = 1399064600
    i = 0
    j = 0
    '''
    第一列，j = 0, 写入序号 ,序号为 i + 1
    第二列，j = 1，写入每个域名总数
    第三列, j = 2，写入百分比 
    第四列，j = 3, 写入域名源
    '''
    for line in iter_data:
        domain = line.split('\t')[0]
        value = line.split('\t')[1]
        excel_w.write(i, 0, i + 1,  style0)
        excel_w.write(i, 1, int(value), style1)
        excel_w.write(i, 2, float(float(value)/ total_domain), style1)
        excel_w.write(i, 3, domain, style1)
        i = i + 1
    excel_out.save('C:/Users/i-xiaoxiong/Desktop/leakdata/1_domain_analy.xls')


#domain_rank()
#domaintoexcel()