import re
import os
import xlwt

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
    f = open(filename,'rb')
    iter_f = iter(f)
    count = count + 1
    for line in iter_f:
        try:

            _line = re.split(":|;", line, maxsplit=1 )
            account = _line[0]
            password = _line[1]

            _account = account.split("@",  1)
            username = _account[0]
            domain = _account[1]

            fdomain_out.write(domain + '\n')
            fpasswd_out.write(password )
            fusername_out.write(username + '\n')
        except :
            ferror_out.write(line)
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
    gci('D:/data/BreachCompilation/data/')
    fdomain_out.close()
    fusername_out.close()
    fpasswd_out.close()
    ferror_out.close()

fdomain_out = None
fusername_out = None
fpasswd_out = None
ferror_out  = None


#split_file()

def analysis_passwd():
    fpasswd_name = 'D:/data/BreachCompilation/collection/1passwd'
    fpasswd_out = open(fpasswd_name, 'ab+')
    iter_f_passwd = iter(fpasswd_out)

    passwd_analysis_out =  'D:/data/BreachCompilation/collection/1passwd_analysis_out'
    fpasswd_analysis_out = open(passwd_analysis_out, 'wb+')

    len_passwd = [0 for n in range(200)]
    for line in iter(iter_f_passwd):
        _len = len(line)
        if _len < 200:
            len_passwd[_len] = len_passwd[_len] + 1

    for n in range(200):
        fpasswd_analysis_out.write(str(n) + "\t" + str(len_passwd[n]) + "\n")

    fpasswd_out.close()
    fpasswd_analysis_out.close()

#analysis_passwd()

def passtoexcel():
    data_in = open('D:/data/BreachCompilation/collection/1passwd_analysis_out')
    iter_data = iter(data_in)
    len_passwd = [0 for n in range(200)]

    for line in iter_data:
        _line = line.split("\t",1)
        len_passwd[int(_line[0])] = _line[1]

    style0 = xlwt.easyxf('font:name Times New Roman, color-index black, bold on', num_format_str='#,##0')
    style1 = xlwt.easyxf('font:name Times New Roman, color-index black, bold on', num_format_str='#,##0.00')

    excel_out = xlwt.Workbook(encoding='utf-8')
    excel_w = excel_out.add_sheet('password_len_analysis')
    total_passwd = 11111111111111111
    for i in range(3):
        for j in range(200):
            if i == 0:
                excel_w.col(j).width = 256*15
                excel_w.write(i, j, j , style0)
            else :
                excel_w.write(i, j, int(len_passwd[j]), style0)
            #elif i == 2:
                #excel_w.write(i, j, float(len_passwd[j]/total_passwd),style1 )
    excel_out.save('C:/Users/i-xiaoxiong/Desktop/leakdata/1pass_len.xls')

passtoexcel()


#gci('D:/data/BreachCompilation/data/')
#print count
