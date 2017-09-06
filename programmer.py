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
from threading import Timer

from PySide import QtGui
from mainwindow import Ui_MainWindow

import jlink


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self._initialize()
        self.mainloop()

    def _initialize(self):
        self._jlink = jlink.JLinkDll()
        self._is_connected = False
        self._serial_number = "0"
        self._adapter_list = self._jlink._adapter_list
        self.startAddrLineEdit.setInputMask(">HHHHHHHH; ")
        self.startAddrLineEdit.setText("00000000")
        self.debugIFCombo.addItem("SWD")
        self.debugIFCombo.addItem("C2")
        self.browseButton.pressed.connect(self.browse_file)
        self.connectButton.pressed.connect(self.connect_mcu)
        self.flashButton.pressed.connect(self.flash_mcu)
        return None

    def browse_file(self):
        file_name, filter = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Download file', "./hex_bin",
            'Intel Hex Files(*.hex);;Binary Files(*.bin);;All Files (*)')
        if file_name:
            self.pathLineEdit.setText(file_name)
        return

    def connect_mcu(self):
        if self._is_connected:
            self._jlink.close()
            self.connectButton.setText("Connect")
            self.deviceLabel.setText("Device:  ")
            self._is_connected = False
        else:
            if self.jlinkDeviceCombo.count() == 0:
                return
            serial_number = self.jlinkDeviceCombo.currentText()
            ifc = self.debugIFCombo.currentText()
            retval = self._jlink.connect(long(serial_number), None, [ifc])
            if retval == False:
                self._jlink.close()
                return
            self.connectButton.setText("Disconnect")
            self.deviceLabel.setText(self._jlink._part_number)
            self._is_connected = True
        return

    def flash_mcu(self):
        if self._is_connected:
            file_name = self.pathLineEdit.text()
            if os.path.isfile(file_name):
                offset = int("0x" + self.startAddrLineEdit.text(), 16)
                self._jlink.erase_chip()
                self._jlink.download(file_name, offset)
                if self.resetMCUCheckBox.checkState():
                    self._jlink.reset(False)
                self.statusLabel.setText("Program Done!")
            else:
                self.statusLabel.setText("Please select a file to download.")
            return
        else:
            self.statusLabel.setText("Please connect to device.")

    def scan_adapter(self):
        num_adapters, adapter_list = self._jlink.get_usb_adapter_list()
        combo_list = self.jlinkDeviceCombo.count()
        # Attached devices changed, need to refresh combox list
        if combo_list != num_adapters:
            selected_adapter = "0"
            if combo_list != 0:
                selected_adapter = self.jlinkDeviceCombo.currentText()
            self.jlinkDeviceCombo.clear()

            index = -1
            for i in range(num_adapters):
                adapter = adapter_list[i]
                if unicode(adapter.SerialNumber) == selected_adapter:
                    index = i
                self.jlinkDeviceCombo.addItem(unicode(adapter.SerialNumber))

            # The original device is removed.
            if index == -1:
                if self._is_connected:
                    self.connect_mcu()
                if num_adapters != 0:
                    index = 0

            self.jlinkDeviceCombo.setCurrentIndex(index)
        return

    def mainloop(self):
        self.scan_adapter()
        Timer(3, self.mainloop).start()
        return

# Main Function
if __name__ == '__main__':
    Program = QtGui.QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    os._exit(Program.exec_())
