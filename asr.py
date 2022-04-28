# -*- coding: utf-8 -*-
# @Time : 2022/4/27 22:18
# @Author : zzy
# @File : main
# @Description :
import json

import os
import sys
import threading
import webbrowser
from datetime import date
import requests
import win32com.client
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from asrInterface import Ui_MainWindow
import speech_recognition as sr

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        # Initialize a timer
        self.timer = QTimer(self)
        # Define timeout connection start_app
        self.timer.timeout.connect(self.start)
        # Define time tasks as one-off tasks
        self.timer.setSingleShot(True)
        # Start time task
        self.timer.start()
        # Instantiate a thread
        self.work = WorkThread()

    def start(self):
        self.work.start()


class WorkThread(QThread):

    def __int__(self):
        # Initialization function, default
        super(WorkThread, self).__init__()

    def run(self):
        mic = sr.Microphone()
        r = sr.Recognizer()
        with mic as source:
            while (1):
                try:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    if sys.argv[-1] == 'google':
                        content = r.recognize_google(audio)
                    else:
                        content = r.recognize_sphinx(audio)
                except:
                    print("Speech recognition failed")
                    continue
                print(content)
                if content.lower() == 'play music':
                    threading.Thread(target=play_music).start()
                elif content.lower() == 'open notepad':
                    threading.Thread(target=open_notepad).start()
                elif content.lower() == 'information of the author':
                    threading.Thread(target=open_bilibili).start()
                elif content.lower() == 'news':
                    threading.Thread(target=get_news).start()
                elif content.lower() == 'high risk':
                    threading.Thread(target=get_high_risk).start()



def play_music():
    os.system('music.mp3')

def open_notepad():
    os.system('notepad.exe')

def open_bilibili():
    webbrowser.open('https://space.bilibili.com/435822845?spm_id_from=333.1007.0.0')

def get_news():
    d = date.today()
    url = "http://api.tianapi.com/ncov/index?key=d334721cf6eba2d619a5855420ec352c&data="+str(d)
    # url = "http://api.tianapi.com/ncov/index?key=d334721cf6eba2d619a5855420ec352c&data=" + '2022-04-25'
    r = requests.get(url)
    news = r.json()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(news['newslist'][0]['news'][0]['summary'])

def get_high_risk():
    d = date.today()
    url = "http://api.tianapi.com/ncov/index?key=d334721cf6eba2d619a5855420ec352c&data="+str(d)
    # url = "http://api.tianapi.com/ncov/index?key=d334721cf6eba2d619a5855420ec352c&data=" + '2022-04-25'
    r = requests.get(url)
    news = r.json()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(f'截止{d.year}年{d.month}月{d.day}日，我国疫情高风险地区有，'+','.join(news['newslist'][0]['riskarea']['high']))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())