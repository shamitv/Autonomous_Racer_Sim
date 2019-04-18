import threading
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

class ImageCaptureThread(QThread):
    """ It will keep taking screenshots till application exists.
    """
    takeScreenShotSignal = pyqtSignal(str, name='takeScreenShot')
    def __init__(self, ui, captureDir, interval=.05 ):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        super().__init__()

        self.ui = ui
        self.interval = interval
        self.seq=0
        self.captureDir=captureDir
        thread = self
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        while True:
            time.sleep(self.interval)
            if(self.ui.captureFrames):
                fileName=self.captureDir+"\\"+str(self.seq)+".png"
                self.takeScreenShotSignal.emit(fileName)
                self.seq+=1
                #print("Emitted signal")
