# -*- coding: utf-8 -*-
# @Time    : 2017/12/19 17:45
# @Author  : Superxx
# @File    : wtoexcel.py
# @Desc    :writetoexcel

import collections
import xlwt

'''
f_a_n = 'D:/data/BreachCompilation/collection/passwd_analy_aa'
f_b_n = 'D:/data/BreachCompilation/collection/passwd_analy_ab'
f_c_n = 'D:/data/BreachCompilation/collection/passwd_analy_ac'
f_d_n = 'D:/data/BreachCompilation/collection/passwd_analy_ad'

f_a_r = open(f_a_n,'rb')
f_b_r = open(f_b_n,'rb')
f_c_r = open(f_c_n,'rb')
f_d_r = open(f_d_n,'rb')

f_a_iter = iter(f_a_r)
f_b_iter = iter(f_b_r)
f_c_iter = iter(f_c_r)
f_d_iter = iter(f_d_r)

for line in f_a_iter:
    passwd = (line.split('\t')[0])
    value = int(line.split('\t')[1])
    if dict.get(passwd) != None:
        dict[passwd] = dict[passwd] + value

    else:
        dict[passwd] = value

for line in f_b_iter:
    passwd = (line.split('\t')[0])
    value = int(line.split('\t')[1])
    if dict.get(passwd) != None:
        dict[passwd] = dict[passwd] + value

    else:
        dict[passwd] = value

for line in f_c_iter:
    passwd = (line.split('\t')[0])
    value = int(line.split('\t')[1])
    if dict.get(passwd) != None:
        dict[passwd] = dict[passwd] + value

    else:
        dict[passwd] = value

for line in f_d_iter:
    passwd = (line.split('\t')[0])
    value = int(line.split('\t')[1])
    if dict.get(passwd) != None:
        dict[passwd] = dict[passwd] + value

    else:
        dict[passwd] = value

f_a_r.close()
f_b_r.close()
f_c_r.close()
f_d_r.close()
'''

dict = {}
out = None
def get_dict(filename):
    global dict
    f_in_name = filename
    f_in_r = open(f_in_name,'rb')
    for line in f_in_r:
        passwd = line
        if dict.get(passwd) != None:
            dict[passwd] = dict[passwd] + 1
        else:
            dict[passwd] = 1
    f_in_r.close()

def out_dict(filename):
    global out
    out = collections.OrderedDict(sorted(dict.items(), key=lambda t: t[1], reverse=True))
    fpassrank_out_name = filename
    fpassrank_out = open(fpassrank_out_name, 'wb')
    j = 0
    for passwd, value in out.items():
        if j >= 200:
            break
        print passwd.strip('\n'), str(value)
        fpassrank_out.write(passwd.strip('\n') + '\t' + str(value) + '\n' )
        j = j + 1
    fpassrank_out.close()

get_dict('D:/data/BreachCompilation/collection/1_passwd/passwd_partaa')
#get_dict('D:/data/BreachCompilation/collection/1_passwd/passwd_partab')
#get_dict('D:/data/BreachCompilation/collection/1_passwd/passwd_partac')
#get_dict('D:/data/BreachCompilation/collection/1_passwd/passwd_partad')
#get_dict('D:/data/BreachCompilation/collection/1_passwd/passwd_partae')
#get_dict('D:/data/BreachCompilation/collection/1_passwd/passwd_partaf')
#get_dict('D:/data/BreachCompilation/collection/1_passwd/passwd_partag')
out_dict('D:/data/BreachCompilation/collection/1_passwd/ana_passwd_partaa')


def writetoexcel():
    global out

    style0 = xlwt.easyxf('font:name Times New Roman, color-index black, bold on', num_format_str='#,##0')
    style1 = xlwt.easyxf('font:name Times New Roman, color-index black, bold on', num_format_str='#,##0.00')

    excel_out = xlwt.Workbook(encoding='utf-8')
    excel_w = excel_out.add_sheet('password_len_analysis')

    '''
    输出序号
    '''
    i = 0
    j = 0
    for i in range(200):
        excel_w.write(i, j, i + 1, style0)
        i = i + 1

    '''
    输出密码排名
    '''
    i = 0
    j = 1
    for passwd, value in out.items():
        if passwd == '':
            pass
        elif passwd == ' ':
            pass
        elif passwd == 'myspace1':
            pass
        else:
            excel_w.write(i, j, str(passwd), style0)
            i = i + 1
        if i == 200:
            break

    excel_out.save('C:/Users/i-xiaoxiong/Desktop/leakdata/pass_fin4.xls')

#writetoexcel()