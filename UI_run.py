from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap
import sys
import background_threds
from PyQt5 import QtCore
import json
import time;

from http.server import SimpleHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread

http_port = 8842


class EventHandler(QObject):
    keyCodeMap = {Qt.Key_Down:"DownArrow",Qt.Key_Up:"UpArrow", Qt.Key_Left:"LeftArrow", Qt.Key_Right:"RightArrow"}
    keyStatus = {'UpArrow': 'up', 'DownArrow': 'up', 'LeftArrow': 'up', 'RightArrow': 'up', }

    def __init__(self, ui):
        super().__init__()
        self.ui=ui

    def getKeyStr(self, keyCode):
        key=self.keyCodeMap.get(keyCode,"Unknown")
        return key;

    def eventFilter(self, source, event):

        if event.type() == QtCore.QEvent.KeyRelease:
            if (event.isAutoRepeat()):
                return False;
            key=self.getKeyStr(event.key())
            print('KeyRelease:'+key)
            if(key in self.keyStatus.keys()):
                self.keyStatus[key]='up'

        if event.type() == QtCore.QEvent.KeyPress:
            if(self.ui.captureFrames==False):
                self.ui.captureFrames = True
            if (event.isAutoRepeat()):
                #print('Skip :: Auto Event')
                return False;
            key = self.getKeyStr(event.key())
            print('KeyPress: ' + key)
            if(key in self.keyStatus.keys()):
                self.keyStatus[key]='down'

        return False


class UI(QApplication):

    def installKeyFilter(self):
        self._handler = EventHandler(self)
        UI.instance().installEventFilter(self._handler)
        #self.browser.focusProxy().installEventFilter(_handler)

    def __init__(self, argv):
        super(UI, self).__init__(argv)
        margin = 22

        self.browser = QWebEngineView()
        url = 'http://localhost:'+str(http_port)+'/driving_sim/racer1/javascript-racer/v2.curves.html'
        print("Loading URL : "+url)
        self.browser.setGeometry(200, 200, 640 + margin, 480 + margin)
        self.browser.load(QUrl(url))
        self.browser.show()
        self.thread = background_threds.DriverThread.GameDriverThread(ui=self,interval=.05)


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    print("App Init start")
    print("Starting http server on port :: "+str(http_port))
    serveraddr = ('', http_port)
    myServer = ThreadingServer(serveraddr, SimpleHTTPRequestHandler)
    # srvr.serve_forever()
    Thread(target=myServer.serve_forever).start()
    print("server started")
    app=UI(sys.argv)
    sys.exit(app.exec_())