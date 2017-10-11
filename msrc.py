########### Python 2.7 #############
#!/usr/bin/python
# -*- coding: UTF-8 -*-


'''
ex:python msrc.py 2017-Oct

'''

import httplib, urllib, base64
import json, sys, re
        
headers = {
    # Request headers
    'api-key': 'e895ed3d5d7e41d49c71b18e13544777',
    #'Authorization': '{access token}',
}

params = urllib.urlencode({
    'api-version': '2016-01-01',
})
def get_cvrf(id):
    try:
        print id
	conn = httplib.HTTPSConnection('api.msrc.microsoft.com')
	conn.request("GET", "/cvrf/%s?api-version={api-version}&%s" %(id, params), "{body}", headers)
	response = conn.getresponse()
	data = response.read()
	data = data.replace("&lt;","<")
        data = data.replace("&gt;",">")
	conn.close()
	return data
    except Exception as e:
	print("[Errno {0}] {1}".format(e.errno, e.strerror))
	
if __name__ == '__main__':
    id = sys.argv[1]
    data = get_cvrf(id)

    re_Vul = r'<vuln:Vulnerability(.*?)</vuln:Vulnerability>'
    res_Vul = re.findall(re_Vul,data,re.S|re.M)
    f = open('%s.txt'%id,'w')
    count = 0 
    for line in res_Vul:
        if line.find('Threats') != -1:
            re_Title = r'<vuln:Title(.*?)</vuln:Title>'
            re_CVE = r'<vuln:CVE(.*?)</vuln:CVE>'
            res_Title = re.findall(re_Title,line,re.S|re.M)
            #print res_Title
            res_CVE = re.findall(re_CVE,line,re.S|re.M)
            print >> f, "%s\n%s"%(res_Title,res_CVE)
            print >>f,"%s"%('-'*100)
            count = count + 1

    print count
    f.close()
    
