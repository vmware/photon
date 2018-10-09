import sys
import time
import threading

class BuildProgressBar:
    done = True
    wait = 1

    @staticmethod
    def progress_indicator():
        while 1: 
            for indicator in '/|\\': yield indicator

    def __init__(self):
        self.progressBar = BuildProgressBar.progress_indicator()

    def progress_bar(self):
        while not self.done:
            print(next(self.progressBar), end='', flush=True)
            time.sleep(self.wait)
            print('\b', end='', flush=True)

    def begin(self):
        self.done = False
        threading.Thread(target=self.progress_bar).start()

    def end(self):
        self.done = True
        time.sleep(self.wait)
