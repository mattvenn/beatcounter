#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import os, time, sys

class Section():

    def __init__(self, length):
        self.length = length
        self.count = 0
        self.widget = QtWidgets.QProgressBar()
        self.widget.setTextVisible(False)
        self.widget.setMinimum(0)
        self.widget.setMaximum(length)

    def reset(self):
        self.count = 0
        self.widget.setValue(self.count)

    def add(self):
        if self.count == self.length:
            return 1
        self.count += 1
        self.widget.setValue(self.count)
        return 0

    def getWidget(self):
        return self.widget

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()

        uic.loadUi('beatcounter/mainwindow.ui', self)

        # buttons
        self.button_start.pressed.connect(lambda: self.start())
        self.button_stop.pressed.connect(lambda: self.stop())
        self.button_reset.pressed.connect(lambda: self.reset())
        self.button_add.pressed.connect(lambda: self.add_section())

        self.lineEdit_bpm.textChanged.connect(lambda: self.update_bpm())

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_beat)

        self.sections = []

        self.reset()

    def add_section(self):
        section = Section(int(self.lineEdit_section.text()))
        self.sections.append(section)
        self.layout_bars.addWidget(section.getWidget())

    def reset(self):
        self.stop()
        self.count_16s = 0
        self.count_beats = 0
        for section in self.sections:
            section.reset()
        self.update_widgets()

    def start(self):
        self.update_beat()
        self.timer.start(self.get_ms_from_bpm())

    def stop(self):
        self.timer.stop()

    def get_ms_from_bpm(self):
        bpm = int(self.lineEdit_bpm.text())
        return 60000/bpm

    def update_bpm(self):
        return
        self.timer.start(self.get_ms_from_bpm())

    def increment_sections(self):
        carry = False
        for section in self.sections:
            if not section.add():
                break

    def update_beat(self):
        self.count_beats += 1
        if self.count_beats > 16:
            self.count_beats = 1
            self.count_16s += 1
            self.increment_sections()

        self.update_widgets()

    def update_widgets(self):
        self.progressBar_beat.setValue(self.count_beats)
        self.label_16s.setText(str(self.count_16s))

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

