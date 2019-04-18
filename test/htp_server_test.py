from http.server import SimpleHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn

from threading import Thread

class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass


serveraddr = ('', 8080)
myServer = ThreadingServer(serveraddr, SimpleHTTPRequestHandler)
#srvr.serve_forever()
Thread(target=myServer.serve_forever).start()

print("server started")