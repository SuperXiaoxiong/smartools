from threading import Thread
import http.server
import socketserver
import time
import common

server = None


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=common.CONFIG['nist_data_mirror'], **kwargs)


def start_server(port):
    global server
    server = socketserver.TCPServer(('127.0.0.1', port), Handler)
    print("Start server at port", port)
    server.serve_forever()


def start(port):
    thread = Thread(target=start_server, args=[port])
    thread.start()
    start_time = int(time.time())
    while not server:
        if int(time.time()) > start_time + 60:
            print("Time out")
            break
    return server


def stop():
    if server:
        server.shutdown()