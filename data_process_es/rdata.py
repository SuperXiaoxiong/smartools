# -*- coding: utf-8 -*-
# @Time    : 2017/12/19 21:21
# @Author  : Superxx
# @File    : rdata.py
# @Desc    :

import os
def gci(filepath):

    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            gci(fi_d)
        else:
            handle_file(os.path.join(filepath, fi_d))
            #cal_file(os.path.join(filepath, fi_d))


count = 0
def cal_file(filename):
    global count
    f = open(filename)
    iter_f = iter(f)
    for line in iter_f:
        count = count + 1
    f.close()

def handle_file(filename):
    global count
    global fdomain_out
    global fusername_out
    global fpasswd_out
    global ferror_out
    f = open(filename)
    iter_f = iter(f)
    count_line = 0
    for line in iter_f:
        count = count + 1
        count_line = count_line + 1
        try:
            pass
            #_line = re.split(":|;", line, maxsplit=1 )
            #account = _line[0]
            #password = _line[1]

            #_account = account.split("@",  1)
            #username = _account[0]
            #domain = _account[1]

            #fdomain_out.write(domain + '\n')
            #fpasswd_out.write(password )
            #fusername_out.write(username + '\n')
        except :
            pass
            #ferror_out.write(line)

    print filename, count_line
    f.close()


def split_file():
    global fdomain_out
    global fusername_out
    global fpasswd_out
    global ferror_out
    fdomain_name = 'D:/data/BreachCompilation/collection/1domain'
    fusername_name = 'D:/data/BreachCompilation/collection/1username'
    fpasswd_name = 'D:/data/BreachCompilation/collection/1passwd'
    ferror_name = 'D:/data/BreachCompilation/collection/1error'
    fdomain_out = open(fdomain_name, 'ab+')
    fusername_out = open(fusername_name, 'ab+')
    fpasswd_out = open(fpasswd_name, 'ab+')
    ferror_out = open(ferror_name, 'ab+')
    gci('D:/data/BreachCompilation/data/a/n')
    fdomain_out.close()
    fusername_out.close()
    fpasswd_out.close()
    ferror_out.close()

fdomain_out = None
fusername_out = None
fpasswd_out = None
ferror_out  = None

'''
split_file()
print count
'''

file = open('D:/data/BreachCompilation/data/a/n/a','rb')
file_e_on = open('D:/data/BreachCompilation/collection/ana','wb')

count_file = 0
f_iter = iter(file)
for line in f_iter:
    count_file = count_file + 1
    file_e_on.write(line)
print count_file

file.close()
file_e_on.close