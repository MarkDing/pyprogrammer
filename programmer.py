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

from PySide import QtGui, QtCore
from mainwindow import MainWindow

import jlink


class Programmer(MainWindow):

    def __init__(self):
        MainWindow.__init__(self)

        self._jlink = jlink.JLinkDll()
        self._is_connected = False
        self._adapter_serial_number = "0"
        self._initialize()
        self.init_timer()
 

    def _initialize(self):
        self._adapter_list = self._jlink._adapter_list

        self.browseButton.pressed.connect(self.browse_file)
        self.connectButton.pressed.connect(self.connect_mcu)
        self.flashButton.pressed.connect(self.flash_mcu)
        self.eraseButton.pressed.connect(self.erase_mcu)
        self.statusBar().showMessage("Ready")
        return None

    def browse_file(self):
        file_name, file_filter = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Download file', "",
            'Intel Hex Files(*.hex);;Binary Files(*.bin);;All Files (*)',
            None,
            QtGui.QFileDialog.DontUseNativeDialog)
        if file_name:
            self.pathLineEdit.setText(file_name)
        # Set start address editable with bin file only.
        split_name = file_name.split(".")
        if split_name[-1].lower() == "hex":
            self.startAddrLineEdit.setText("00000000")
            self.startAddrLineEdit.setReadOnly(True)
        if split_name[-1].lower() == "bin":
            self.startAddrLineEdit.setReadOnly(False)
        return

    def init_connect_group(self):
        self.connectButton.setText("Connect")
        self.deviceLabel.setText("Device:  ")
        self._is_connected = False
        self._adapter_serial_number = "0"

    def connect_mcu(self):
        if self._is_connected:
            self.init_connect_group()
            self._jlink.close()
            msg = "Disconnected"
        else:
            if self.jlinkDeviceCombo.count() == 0:
                return
            serial_number = self.jlinkDeviceCombo.currentText()
            ifc = self.debugIFCombo.currentText()
            result = self._jlink.connect(long(serial_number), ifc)
            if not result:
                msg = "Connect failed."
            else:
                msg = "Connected"
                self.connectButton.setText("Disconnect")
                self.deviceLabel.setText(self._jlink._part_number)
                self._is_connected = True
                self._adapter_serial_number = serial_number
        self.statusBar().showMessage(msg)
        return

    def flash_mcu(self):
        if self._is_connected:
            file_name = self.pathLineEdit.text()
            if os.path.isfile(file_name):
                offset = int("0x" + self.startAddrLineEdit.text(), 16)
                result = self._jlink.erase_chip()
                if not result:
                    self.init_connect_group()
                    self._jlink.close()
                    msg = "Erase failed."
                    self.statusBar().showMessage(msg)
                    return
                self._jlink.download(file_name, offset)
                if self.resetMCUCheckBox.checkState():
                    self._jlink.reset(False)
                msg = "Program done."
            else:
                msg = "Please select a file to download."
        else:
            msg = "Please connect to device."
        self.statusBar().showMessage(msg)
        return

    def erase_mcu(self):
        if self._is_connected:
            result = self._jlink.erase_chip()
            if not result:
                self.init_connect_group()
                self._jlink.close()
                msg = "Erase failed."
            else:
                msg = "Erase done."
        else:
            msg = "Please connect to device."
        self.statusBar().showMessage(msg)
        return

    def scan_adapter(self):
        num_adapters, adapter_list = self._jlink.get_usb_adapter_list()
        combo_list = self.jlinkDeviceCombo.count()

        if (combo_list == 0) and (num_adapters == 0):
            return

        selected_adapter_sn = "0"
        if combo_list != 0:
            if self._is_connected:
                selected_adapter_sn = self._adapter_serial_number
            else:
                selected_adapter_sn = self.jlinkDeviceCombo.currentText()
        self.jlinkDeviceCombo.clear()

        index = -1
        for i in range(num_adapters):
            adapter = adapter_list[i]
            if unicode(adapter.SerialNumber) == selected_adapter_sn:
                index = i
            self.jlinkDeviceCombo.addItem(unicode(adapter.SerialNumber))

        # Original device is removed
        if index == -1:
            if self._is_connected:
                self.connect_mcu()
            if num_adapters != 0:
                index = 0    
        self.jlinkDeviceCombo.setCurrentIndex(index)
        return

    def init_timer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.scan_adapter)
        self.timer.start(1000)


# Main Function
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = Programmer()
    mainWin.show()
    os._exit(app.exec_())