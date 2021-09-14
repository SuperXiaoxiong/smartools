#coding=utf-8
import sys
import socket
from socket import error as socket_error
import urllib.parse
import ssl

'''
增加了ssl 状态下的 t3s 检测
'''

def t3conn(host, port):
    try:
        server_address = (host, port)
        #print 'INFO: Attempting Connection: ' + str(server_address)
        sock = socket.create_connection(server_address, 4)
        sock.settimeout(5)
        headers = 't3 10.3.6\nAS:255\nHL:19\n\n'
        sock.sendall(headers.encode('utf-8'))
        data = ""

        try:
            data = sock.recv(1024)
        except socket.timeout:
            print('ERROR: Socket Timeout Occurred: ' + str(host) + ':' + str(port) + '\n')

        sock.close()
        return data.decode()
    except socket_error:
        print('ERROR: Connection Failed: ' + str(host) + ':' + str(port) + '\n')
        return ""


def parseURL(url):

    result = urllib.parse.urlparse(url)
    protocol = result.scheme
    port = result.port
    host = result.netloc.split(':')[0]
    if port == None and protocol == 'https':
        port = 443
    elif port == None and protocol == 'http':
        port = 80

    return protocol, host, port


def t3sconn(host, port):
    try:
        # server_address = (host, port)
        #print 'INFO: Attempting Connection: ' + str(server_address)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # sock = socket.create_connection(server_address, 4)
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock) as ssock:
                headers = 't3s 10.3.6\nAS:255\nHL:19\n\n'
                ssock.sendall(headers.encode('utf-8'))
                msg = ssock.recv(1024)
                print("receive msg from server :".format(msg.decode()))
                ssock.close()
        return msg.decode()

    except socket_error:
        print('ERROR: Connection Failed: ' + str(host) + ':' + str(port) + '\n' + str(socket_error))
        return ""



def weblogic(url):
    for i in range(0, 10):
        protocol, host, port = parseURL(url)
        if protocol == "https":
            data = t3sconn(host, port)
        else:
            data = t3conn(host, port)
        if data.strip() == 'HELO':
            print('INFO: Sever only returned HELO, retrying to get server version.')
            continue

        if data == "":
            break

        print(data)

        if 'HELO' in data:
            found_weblogic_version = data[5:13]

            print('[+] version: %s' % found_weblogic_version)

            break

def poc(url):
    pass

if __name__ == '__main__':
    """
    python t3_check.py https://192.168.8.2:5559/console
    python t3_check.py http://192.168.8.2:7004/console
    """
    weblogic(sys.argv[1])