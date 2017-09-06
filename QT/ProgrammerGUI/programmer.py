# Copyright (C) 2017 Silicon Laboratories, Inc.
# http://developer.silabs.com/legal/version/v11/Silicon_Labs_Software_License_Agreement.txt
#
# This file is part of Programmer Tool.
#
# Programmer Tool is a free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Programmer Tool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Programmer Tool.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os

from PySide import QtCore, QtGui

from mainwindow import Ui_MainWindow


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.browseButton.pressed.connect(self.browse_file)

    def browse_file(self, img=0):
        fileName, filter = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Download file', "../../",
            'Intel Hex Files(*.hex);;All Files (*)')
        if fileName:
            self.pathLineEdit.setText(fileName)
        return

# Main Function
if __name__ == '__main__':
    Program = QtGui.QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(Program.exec_())
