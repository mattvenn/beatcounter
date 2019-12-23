#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import os, time, sys

class Section(QtWidgets.QProgressBar):

    def __init__(self, length, flash_rate):
        super(self.__class__, self).__init__()
        
        self.length = length
        self.count = 0
        #self.widget = QtWidgets.QProgressBar()
        self.setTextVisible(False)
        self.setMinimum(0)
        self.setMaximum(length)
        self.flash_rate = flash_rate

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.flash)
        self.flash_state = True

    def reset(self):
        self.count = 0
        self.setValue(self.count)

    def add(self):
        if self.count == self.maximum() - 1:
            self.timer.start(self.flash_rate)
            self.count += 1
            self.setValue(self.count)
            return 0

        elif self.count == self.maximum():
            self.flash_state = False
            self.flash()
            self.timer.stop()
            return 1

        else:
            self.count += 1
            self.setValue(self.count)
            return 0
    
    def flash(self):
        palette = QtGui.QPalette(self.palette())
        if self.flash_state:
            colour = QtGui.QColor(QtCore.Qt.green)
        else:
            colour = QtGui.QColor(QtCore.Qt.blue)
        palette.setColor(QtGui.QPalette.Highlight, colour)
        self.setPalette(palette)

        self.flash_state = not self.flash_state

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()


        # working directory
        try:
           self.wd = sys._MEIPASS # if running inside pyinstaller
        except AttributeError:
           self.wd = os.getcwd()

        uic.loadUi(os.path.join(self.wd, 'beatcounter', 'mainwindow.ui'), self)

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
        section = Section(int(self.lineEdit_section.text()), self.get_ms_from_bpm()/2)
        self.sections.append(section)
        self.layout_bars.addWidget(section)

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

