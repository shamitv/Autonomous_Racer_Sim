from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap
import sys
import screencap
from PyQt5 import QtCore
import json
import time;


class EventHandler(QObject):
    keyCodeMap = {Qt.Key_Down:"DownArrow",Qt.Key_Up:"UpArrow", Qt.Key_Left:"LeftArrow", Qt.Key_Right:"RightArrow"}
    keyStatus = {'UpArrow': 'up', 'DownArrow': 'up', 'LeftArrow': 'up', 'RightArrow': 'up', }
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
        self._handler = EventHandler()
        UI.instance().installEventFilter(self._handler)
        #self.browser.focusProxy().installEventFilter(_handler)

    def __init__(self, argv):
        super(UI, self).__init__(argv)
        margin = 22

        self.browser = QWebEngineView()
        url = 'http://localhost:5500/v2.curves.html'
        self.browser.setGeometry(200, 200, 640 + margin, 480 + margin)
        self.browser.load(QUrl(url))
        self.browser.show()
        self.thread = screencap.CaptureThread.ImageCaptureThread("F:\\ml\\js_racing\\screens")
        self.thread.takeScreenShotSignal.connect(self.captureWindowImage)
        print("adding key filter")
        self.installKeyFilter()





    #@QtCore.pyqtSlot(str, name='takeScreenShot')
    def captureWindowImage(self,filePath):
        #print("Got signal")
        windowSize = self.browser.size()
        #print(windowSize)
        pixmap = QPixmap(windowSize)
        self.browser.render(pixmap)
        #print("Rendered Browser Window")
        pixmap.save(filePath)
        jsonPath=filePath+".json"
        jsonStr= json.dumps(self._handler.keyStatus)
        #print(jsonStr)
        localtime = time.asctime(time.localtime(time.time()))
        print("Screenshot at ", localtime)

        with open(jsonPath, "w") as jsonFile:
            jsonFile.write(jsonStr)

if __name__ == '__main__':
    print("App Init start")
    app=UI(sys.argv)
    sys.exit(app.exec_())