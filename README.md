Jlink Python Programming GUI Tool
===============

## 1 Introduction 
We use Python+Pyside make a GUI programming tool. By calling JLinkARM.Dll, it can access the device via C2 and SWD interface. The EFM8 and EFM32 which are C8051 and ARM cortex M0/M3/M4 core are in the latest Segger JLinkARM.dll support list. It can download hex file, and also binary file with offset setting. 

## 2 Preparation
### 2.1 Install Python 2.7 32-bit
The reason for 32-bit python is because many dll file is 32-bit version.

Goto https://www.python.org/downloads/release/python-2712/ and install the python 2.7 32-bit. 

And also install enum package

```
$pip install enum
```

### 2.2 Install Pyside
Goto https://info.qt.io/download-qt-for-application-development, install QT creator. 

using following command to convert .ui file into .py file. 
$ pyside-uic mainwindow.ui -o mainwindow.py

### 2.3 Pyside API
All Pyside API can be found in http://pyside.github.io/docs/pyside/ It is very good place for Pyside brand new developer. 

![PySide Doc][PySide_doc]


### 2.4 Install Pycharm
Goto http://www.jetbrains.com/pycharm/download/, download community version. 

![PyCharm][PyCharm]

It is an awesome Python development IDE. 

### 2.5 Get JlinkARM.Dll 
The JLinkARM.dll is the key file to access EFM8 and EFM32 through on board segger Jlink controller in Silicon Labs STK board. 

Goto https://www.segger.com/downloads/jlink/, download latest J-link Software and Documentation Pack. 

![Segger jlink download][Segger_jlink_download]

After installation, the JLinkARM.dll can be found in following path: 
C:\Program Files (x86)\SEGGER\JLink_V618c\JLinkARM.dll

## 3 Guide on Coding
Now we need to know elements that the programming tool required. It requires a GUI frame mainwindow.py for what the tools looks like; JlinkARM.dll for communication with device; main control routine programmer.py; jlink.py take response on communication between main control routine and JLinkARM.dll. 

### 3.1 GUI frame
Here is the final view of the programmer tool 

![Programmer view][Programmer]

It is convenient to make a GUI frame using PySide. 
The GUI contains Window Title, Menu, Status Bar and Central Widget. 

#### 3.1.1 Window Title
Define Window Title and Fixed size. 

```python
self.setWindowTitle("PyProgrammer")
self.setFixedSize(640, 260)
```

#### 3.1.2 Menu
Create Help Menu and About dialog. 

```python
def createMenu(self):
    self.aboutAct = QtGui.QAction("&About", self,
            statusTip="Show the PyProgrammer's About box",
            triggered=self.about)
    self.helpMenu = self.menuBar().addMenu("&Help")
    self.helpMenu.addAction(self.aboutAct)        

def about(self):
    QtGui.QMessageBox.about(self, "About PyProgrammer",
            "Copyright Silicon Laboratories, Inc 2018. All rights reserved.\n\n\r"
            "PyProgrammer v1.0 is based on Qt Pyside and SEGGER JlinkARM.\n\n\r"
            "The PyProgrammer example demonstrates how to write a "
            "modern GUI flash programmer applications using Qt Pyside.\n\n\r"
            "This program uses third party libraries covered by the LGPL.\n\r"
            "See the file LGPL.txt for details.")
```

#### 3.1.3 Status Bar
Create Status Bar. 

```python
def createStatusBar(self):
    self.statusBar().showMessage("Ready")
```

#### 3.1.4 Central Widget
The main layout of Central Widget includes two main groups - "Connection" and "Flash MCU". The "Flash MCU" includes two subgroups - "Browse" and "Flash". 

__Main Group Layout__

```python
mainLayout = QtGui.QVBoxLayout(self.centralWidget)
mainLayout.addWidget(self.createConnectGroup())
mainLayout.addWidget(self.createFlashMCUGroup())
self.setLayout(mainLayout)
```

__Sub Group Layout__

```python
    def createFlashMCUGroup(self):
        groupBox = QtGui.QGroupBox("Flash MCU
        ",self.centralWidget)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.createBrowseGroup())
        layout.addWidget(self.createFlashGroup())

        groupBox.setLayout(layout)
        return groupBox
```


### 3.2 Main Control 
The purpose of the tool is to select a image file, connect to device, flash the image into device, response on any event that pop up with the operation. 

#### 3.2.1 Push Button Events
The Pyside provides interface to connect button press event to dedicate function. 
The tool has four buttons -  Browse, Connect, Erase and Flash. 

```python
self.browseButton.pressed.connect(self.browse_file)
self.connectButton.pressed.connect(self.connect_mcu)
self.flashButton.pressed.connect(self.flash_mcu)
self.eraseButton.pressed.connect(self.erase_mcu)

def browse_file(self):
	...
	return

def connect_mcu(self):
	...
	return

def flash_mcu(self):
	...
	return

def erase_mcu(self):
    ...
    return
``` 

According above code, the four button pressed event was connected to the dedicate functions. Once user click on the button, it will call the connected function. 

#### 3.2.2 File Browser
The QtGui provides QFileDialog.getOpenFileName to browse the image file. User can define the window name, file default location, file extension. etc

```python
def browse_file(self):
    file_name, file_filter = QtGui.QFileDialog.getOpenFileName(
        self, 'Open Download file', "./hex_bin",
        'Intel Hex Files(*.hex);;Binary Files(*.bin);;All Files (*)')
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
```

The above codes open a file dialog, looking for hex, bin and all files. 

![Browse file][Browse_file]

Once choose a file, the full path file name displayed in pathLineEdit component. 

#### 3.2.3 Adapter and Debug IF list
The Combox is used here for a list of adapter and debug interface. 
Adding item into Combox as follows:

```python
# Adding debug interface into Debug IF Combox
self.debugIFCombo.addItems("SWD C2".split())

# Adding new adapter into Adapter Combox list
self.jlinkDeviceCombo.addItem(unicode(adapter.SerialNumber))
```

We set two type of debug interface into combox, use choose which interface to connect to the device. For EFM8, it is C2 interface; for EFM32, it is SWD interface. 
Other common usage of Combox as follows:

```python
# Get current selected Combox item. 
serial_number = self.debugIFCombo.currentText()

# Checking if any adapter exist by count Combox items. 
if self.jlinkDeviceCombo.count() == 0:
    return

# Clear all Combox items. 
self.jlinkDeviceCombo.clear()

# Set current Combo index
self.jlinkDeviceCombo.setCurrentIndex(index)
```

#### 3.2.4 Part Number and Status Display
The Label and Status Bar components made for the purpose.

```python
# Show message on status bar
msg = "Please connect to device."
self.statusBar().showMessage(msg)

# Show detect part number on device Label 
self.deviceLabel.setText(self._jlink._part_number)
```

#### 3.2.5 Flash Offset Format and Reset MCU Check Box 
The QtGui provides CheckBox component can be used as reset MCU check box. And LineEdit has function setInputMask to limit hex number input only. 

```python
# Checking if user check to option
if self.resetMCUCheckBox.checkState():
	self._jlink.reset(False)

# Make hex number input only and with initial value 00000000. 
self.startAddrLineEdit.setInputMask(">HHHHHHHH; ")
self.startAddrLineEdit.setText("00000000")

```

#### 3.2.6 Scan Adapter Automatic 
The dynamic scan adapter is basic requirement of a programmer tool. Using Python QTimer can achieve the purpose. 

```python
def scan_adapter(self):
    num_adapters, adapter_list = self._jlink.get_usb_adapter_list()
    ...
    return

def init_timer(self):
    self.timer = QtCore.QTimer(self)
    self.timer.timeout.connect(self.scan_adapter)
    self.timer.start(1000)
```

### 3.3 JLink function
In order to communicate with STK on board Segger JLink controller, the Python script needs to talk with JLinkARM.DLL, and the JLinkARM.DLL pass the command to the STK JLink controller. 

The Jlink.py act as interpret layer between JLinkARM.DLL and Main Control routine. 
There are several useful interface functions used in this programmer tool. 

```python
# Loading JLinkARM.DLL
self._jlink = jlink.JLinkDll()

# Connect jLink device with serial_number, debug interface ifc
result = self._jlink.connect(long(serial_number), None, ifc)

# Close JLink connection
self._jlink.close()

# Erase device and download file into device
self._jlink.erase_chip()
self._jlink.download(file_name, offset)

# Reset the device
self._jlink.reset(False)

# Get attached USB adapter list
num_adapters, adapter_list = self._jlink.get_usb_adapter_list()

```


[Segger_jlink_download]:img/segger-jlink-download.png
[PyCharm]:img/pycharm.png
[PySide_doc]:img/pyside-doc.png
[Programmer]:img/programmer.png
[Browse_file]:img/browse-file.png

