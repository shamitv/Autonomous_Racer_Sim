import threading
import time
from PyQt5.QtCore import QThread, QEvent, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication


class GameDriverThread(QThread):
    """ It will keep taking screenshots till application exists.
    """
    takeScreenShotSignal = pyqtSignal(str, name='driveThread')

    def __init__(self, ui, interval=.05 ):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        super().__init__()

        self.ui = ui
        self.interval = interval
        self.seq=0
        thread = self
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        while True:
            time.sleep(self.interval)
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Up,  Qt.NoModifier)
            recipient = self.ui.browser.focusProxy()
            QApplication.postEvent(recipient, event)
