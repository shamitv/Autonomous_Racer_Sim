import sys
import background_threds
import os
import io
import time
from PIL import Image
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtCore import QBuffer

from http.server import SimpleHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread

from keras.models import load_model
import numpy as np

http_port = 8842

def get_data_dir():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(script_dir,'data','set1')
    return os.path.normpath(data_dir)


def get_model_dir():
    model_dir = os.path.join(get_data_dir(),'model')
    return os.path.normpath(model_dir)


def get_model_file():
    model_dir = os.path.join(get_model_dir(),'trained_model_v2.h5')
    return os.path.normpath(model_dir)


def get_model():
    model = load_model(get_model_file())
    return model


def get_action_for_image(img,model):
    image_dim = (256, 256)
    img = img.resize(image_dim, Image.LANCZOS)
    img=img.convert('L')
    img_arr = np.array(img)
    img_arr=img_arr.reshape(image_dim[0],image_dim[1],1)
    test_x=np.array([img_arr])
    output=model.predict(test_x)
    classes = ['Accelerate', 'DoNothing', 'TurnRight', 'TurnLeft']
    action = classes[np.argmax(output)]
    return action;


def get_key_for_action(action):
    key_map={
        'Accelerate': Qt.Key_Up,
        'TurnLeft': Qt.Key_Left,
        'TurnRight': Qt.Key_Right,
        'DoNothing': Qt.Key_Up
    }
    return key_map[action]


class UI(QApplication):

    def installKeyFilter(self):
        UI.instance().installEventFilter(self._handler)
        #self.browser.focusProxy().installEventFilter(_handler)

    def getBrowserScreenshot(self):
        #print('Taking screenshot')
        windowSize = self.browser.size()
        pixmap = QPixmap(windowSize)
        self.browser.render(pixmap)
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        pixmap.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        return pil_im


    def getFrameAndDrive_bkp(self):
        image = self.getBrowserScreenshot()
        action=get_action_for_image(image, self.model)
        key=get_key_for_action(action)
        print(action+" --> "+str(key))
        event_key_press = QKeyEvent(QEvent.KeyPress, key, Qt.NoModifier)
        event_key_up = QKeyEvent(QEvent.KeyRelease, key, Qt.NoModifier)
        recipient = self.browser.focusProxy()
        QApplication.postEvent(recipient, event_key_press)
        #time.sleep(0.025)
        QApplication.postEvent(recipient, event_key_up)
        return


    def sendKey(self,key):
        event_key_press = QKeyEvent(QEvent.KeyPress, key, Qt.NoModifier)
        recipient = self.browser.focusProxy()
        QApplication.postEvent(recipient, event_key_press)


    def getFrameAndDrive(self):
        image = self.getBrowserScreenshot()
        action=get_action_for_image(image, self.model)
        key = get_key_for_action(action)
        print(action + " --> " + str(key))
        self.sendKey(Qt.Key_Up);
        self.sendKey(key);
        return



    def __init__(self, argv):
        super(UI, self).__init__(argv)
        margin = 22

        self.model = get_model()
        self.browser = QWebEngineView()
        url = 'http://localhost:'+str(http_port)+'/driving_sim/racer1/javascript-racer/v2.curves.html'
        print("Loading URL : "+url)
        self.browser.setGeometry(200, 200, 640 + margin, 480 + margin)
        self.browser.load(QUrl(url))
        self.browser.show()
        self.thread = background_threds.DriverThread.GameDriverThread(ui=self,interval=.5)
        self.thread.driveSignal.connect(self.getFrameAndDrive)




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