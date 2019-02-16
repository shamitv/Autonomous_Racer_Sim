import threading
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

class ImageCaptureThread(QThread):
    """ It will keep taking screenshots till application exists.
    """
    takeScreenShotSignal = pyqtSignal(str, name='takeScreenShot')
    def __init__(self, captureDir, interval=.1 ):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        super(ImageCaptureThread, self).__init__()
        self.interval = interval
        self.seq=0
        self.captureDir=captureDir
        thread = self
        thread.daemon = True                            # Daemonize thread
                                         # Start the execution
        thread.start()
    def run(self):
        """ Take screenshots after 5 seconds """
        time.sleep(5)
        while True:
            time.sleep(self.interval)
            fileName=self.captureDir+"\\"+str(self.seq)+".png"

            self.takeScreenShotSignal.emit(fileName)
            self.seq+=1
            #print("Emitted signal")
