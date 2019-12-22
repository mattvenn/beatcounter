#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import os, time, sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
#        self.setWindowIcon(QtGui.QIcon('logo_pancom.ico'))

        uic.loadUi('beatcounter/mainwindow.ui', self)

        # buttons
        self.button_start.pressed.connect(lambda: self.start())
#        self.button_stop.pressed.connect(lambda: self.start())
        self.lineEdit_bpm.textChanged.connect(lambda: self.update_bpm())

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_beat)

        self.beat_count = 1
        self.count16s = 1
        self.count64s = 1

    def start(self):
        self.timer.start(self.get_ms_from_bpm())

    def stop(self):
        self.timer.stop()

    def get_ms_from_bpm(self):
        bpm = int(self.lineEdit_bpm.text())
        return 60000/bpm

    def update_bpm(self):
        self.timer.start(self.get_ms_from_bpm())

    def update_beat(self):
        self.progressBar_beat.setValue(self.beat_count)
        self.progressBar_16s.setValue(self.count16s)
        self.progressBar_64s.setValue(self.count64s)

        self.label_beats.setText(str(self.beat_count))
        self.label_16s.setText(str(self.count16s))
        self.label_64s.setText(str(self.count64s))
        self.beat_count += 1
        if self.beat_count > 16:
            self.beat_count = 1
            self.count16s += 1

        if self.count16s > 4:
            self.count16s = 1
            self.count64s += 1

        if self.count64s > 16:
            self.count64s = 1

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

