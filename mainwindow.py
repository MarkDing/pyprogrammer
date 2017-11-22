# Copyright (C) 2017 Silicon Laboratories, Inc.
# http://developer.silabs.com/legal/version/v11/Silicon_Labs_Software_License_Agreement.txt
#
# This file is part of Programmer Tool.
#
# PyProgrammer Tool is a free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyProgrammer Tool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Programmer Tool.  If not, see <http://www.gnu.org/licenses/>.


from PySide import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setObjectName("MainWindow")

        # Setup Window display icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/pyprogrammer.png"),QtGui.QIcon.Normal)
        self.setWindowIcon(icon)

        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(self.centralWidget)

        self.createMenu()
        self.createStatusBar()

        mainLayout = QtGui.QVBoxLayout(self.centralWidget)
        mainLayout.addWidget(self.createConnectGroup())
        mainLayout.addWidget(self.createFlashMCUGroup())
        self.setLayout(mainLayout)

        self.setWindowTitle("PyProgrammer")
        self.setFixedSize(640, 260)

    def createMenu(self):
        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the PyProgrammer's About box",
                triggered=self.about)
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)        

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createConnectGroup(self):
        groupBox = QtGui.QGroupBox("Connection",self.centralWidget)

        self.adapterLabel = QtGui.QLabel("Adpater")
        self.connectButton = QtGui.QPushButton("Connect")
        self.jlinkDeviceLabel = QtGui.QLabel("J-Link Device S/N")
        self.jlinkDeviceCombo = QtGui.QComboBox()
        self.debugIFLabel = QtGui.QLabel("Debug Interface")
        self.debugIFCombo = QtGui.QComboBox()
        self.deviceLabel = QtGui.QLabel("Device:")

        # Config each widget
        self.debugIFCombo.addItems("SWD C2".split())

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.adapterLabel)
        layout.addWidget(self.connectButton)
        layout.addWidget(self.jlinkDeviceLabel)
        layout.addWidget(self.jlinkDeviceCombo)
        layout.addWidget(self.debugIFLabel)
        layout.addWidget(self.debugIFCombo)
        layout.addWidget(self.deviceLabel)

        # Set stretch factor for each widget
        layout.setStretchFactor(self.jlinkDeviceCombo, 1.5)
        layout.setStretchFactor(self.deviceLabel, 2)

        groupBox.setLayout(layout)
        return groupBox

    def createBrowseGroup(self):
        groupBox = QtGui.QGroupBox(self.centralWidget)

        self.downloadFileLabel = QtGui.QLabel("Download File")
        self.pathLineEdit = QtGui.QLineEdit()
        self.browseButton = QtGui.QPushButton("Browse")

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.downloadFileLabel)
        layout.addWidget(self.pathLineEdit)
        layout.addWidget(self.browseButton)

        groupBox.setLayout(layout)
        return groupBox

    def createFlashGroup(self):
        groupBox = QtGui.QGroupBox(self.centralWidget)

        self.startAddrLabel = QtGui.QLabel("Flash Start Address(hex):")
        self.startAddrLineEdit = QtGui.QLineEdit()
        self.resetMCUCheckBox = QtGui.QCheckBox("Reset MCU After Flashing")
        self.eraseButton = QtGui.QPushButton("Erase")
        self.flashButton = QtGui.QPushButton("Flash")

        # Config each widget
        self.startAddrLineEdit.setInputMask(">HHHHHHHH; ")
        self.startAddrLineEdit.setText("00000000")
        self.startAddrLineEdit.setAlignment(QtCore.Qt.AlignRight)
        self.startAddrLineEdit.setReadOnly(True)
        self.resetMCUCheckBox.setChecked(True)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.startAddrLabel)
        layout.addWidget(self.startAddrLineEdit)
        layout.addStretch()
        layout.addWidget(self.resetMCUCheckBox)
        layout.addStretch()
        layout.addWidget(self.eraseButton)
        layout.addWidget(self.flashButton)

        groupBox.setLayout(layout)
        return groupBox

    def createFlashMCUGroup(self):
        groupBox = QtGui.QGroupBox("Flash MCU",self.centralWidget)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.createBrowseGroup())
        layout.addWidget(self.createFlashGroup())

        groupBox.setLayout(layout)
        return groupBox

    def about(self):
        QtGui.QMessageBox.about(self, "About PyProgrammer",
                "Copyright Silicon Laboratories, Inc 2018. All rights reserved.\n\n\r"
                "PyProgrammer v1.0 is based on Qt Pyside and SEGGER JlinkARM.\n\n\r"
                "The PyProgrammer example demonstrates how to write a "
                "modern GUI flash programmer applications using Qt Pyside.\n\n\r"
                "This program uses third party libraries covered by the LGPL.\n\r"
                "See the file LGPL.txt for details.")

# Main Function
# if __name__ == '__main__':
#     import sys

#     app = QtGui.QApplication(sys.argv)
#     mainWin = MainWindow()
#     mainWin.show()
#     sys.exit(app.exec_())

