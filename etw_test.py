#coding:utf-8
'''
base on python3 
Created on 2017年9月20日
@author: superxiaoxiong
'''


#程序的GUID 使用cmd  命令logman query providers 查看
#硬件的GUID 在设备管理器， 选设备，属性，详细信息中看到
import etw

def some_fuc():
    guid = {'Some provider': etw.GUID("{8E598056-8993-11D2-819E-0000F875A064}")}
    
    job = etw.ETW(guid)
    
    etw.run('etw',job)
    
    
some_fuc()