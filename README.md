Jlink Python Programming GUI Tool
===============

## 1 Introduction 
We use Python+Pyside make a GUI programming tool. By calling JLinkARM.Dll, it can access the device via C2 and SWD interface. The EFM8 and EFM32 which are C8051 and ARM cortex M0/M3/M4 core are in the latest Segger JLinkARM.dll support list. It can download hex file, and also binary file with offset setting. 

## 2 Preparation
Detailed information on Python + Pyside setup can be found in following link: 

https://confluence.silabs.com/pages/viewpage.action?pageId=46153928

### 2.1 Install Python 2.7 32-bit
The reason for 32-bit python is because many dll file is 32-bit version.

Goto https://www.python.org/downloads/release/python-2712/ and install the python 2.7 32-bit. 

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
Run the Qt Creator, create new project. Make a GUI base on requirement of the tool. 

![QT Creator][Qt_creator]

1. These are components of the UI, just simply drag and drop to right place on the window. 
2. This is a __Push Button__ component. 
3. Change the button name to an easy understand one __connectButton__

Then save the project, we got mainwindow.ui file. Convert it into python file mainwindow.py by using following command in CMD console.

```
$pyside-uic mainwindow.ui - o mainwindow.py
```

Open the mainwindow.py. 

```python
from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(605, 360)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.flashMCUGroup = QtGui.QGroupBox(self.centralWidget)
        self.flashMCUGroup.setGeometry(QtCore.QRect(10, 90, 580, 110))
        self.flashMCUGroup.setObjectName("flashMCUGroup")
        self.startAddrLabel = QtGui.QLabel(self.flashMCUGroup)
        self.startAddrLabel.setGeometry(QtCore.QRect(10, 70, 120, 20))
        self.startAddrLabel.setObjectName("startAddrLabel")
        self.statusLabel = QtGui.QLabel(self.centralWidget)
        self.statusLabel.setGeometry(QtCore.QRect(20, 250, 450, 15))
        self.statusLabel.setObjectName("statusLabel")
        self.resetMCUCheckBox = QtGui.QCheckBox(self.flashMCUGroup)
        self.resetMCUCheckBox.setGeometry(QtCore.QRect(260, 70, 140, 20))
        self.resetMCUCheckBox.setObjectName("resetMCUCheckBox")
        self.pathLineEdit = QtGui.QLineEdit(self.flashMCUGroup)
        self.pathLineEdit.setGeometry(QtCore.QRect(90, 30, 400, 20))
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.flashButton = QtGui.QPushButton(self.flashMCUGroup)
        self.flashButton.setGeometry(QtCore.QRect(500, 70, 75, 23))
        self.flashButton.setObjectName("flashButton")
```

It defines every components of the GUI, including the name, position, size, QtGui module name. etc. Once user get familiar with the QtGui, user can directly modify this file without using QT Creator tool any more.

Here is the final view of the programmer tool 

![Programmer view][Programmer]


### 3.2 Main Control 
The purpose of the tool is to select a image file, connect to device, flash the image into device, response on any event that pop up with the operation. 

#### 3.2.1 Push Button Events
The Pyside provides interface to connect button press event to dedicate function. 
The tool has three buttons -  Browse, Connect and Flash. 

```python
self.browseButton.pressed.connect(self.browse_file)
self.connectButton.pressed.connect(self.connect_mcu)
self.flashButton.pressed.connect(self.flash_mcu)

def browse_file(self):
	...
	return

def connect_mcu(self):
	...
	return

def flash_mcu(self):
	...
	return
``` 

According above code, the three button pressed event was connected to the three functions: browse_file(), connect_mcu(), flash_mcu(). Once user click on the button, it will call the connected function. 

#### 3.2.2 File Browser
The QtGui provides QFileDialog.getOpenFileName to browse the image file. User can define the window name, file default location, file extension. etc

```python
def browse_file(self):
    file_name, filter = QtGui.QFileDialog.getOpenFileName(
        self, 'Open Download file', "./hex_bin",
        'Intel Hex Files(*.hex);;Binary Files(*.bin);;All Files (*)')
    if file_name:
        self.pathLineEdit.setText(file_name)
    return
```

The above open a file dialog, looking for hex, bin and all files. 

![Browse file][Browse_file]

Once choose a file, the full path file name displayed in pathLineEdit component. 

#### 3.2.3 Adapter and Debug IF list
The Combox is used here for a list of adapter and debug interface. 
Adding item into Combox as follows:

```python
# Adding debug interface into Debug IF Combox
self.debugIFCombo.addItem("SWD")
self.debugIFCombo.addItem("C2")

# Adding new adapter into Adapter Combox list
self.jlinkDeviceCombo.addItem(unicode(adapter.SerialNumber))
```

We set two type of debug interface into combox, use choose which interface to connect to the device. For EFM8, it is C2 interface; for EFM32, it is SWD interface. 
Other common usage of Combox as follows:

```python
# Get current selected Combox item. 
ifc = self.debugIFCombo.currentText()

# Checking if any adapter exist by count Combox items. 
if self.jlinkDeviceCombo.count() == 0:
    return

# Clear all Combox items. 
self.jlinkDeviceCombo.clear()

# Set current Combo index
self.jlinkDeviceCombo.setCurrentIndex(index)
```

#### 3.2.4 Part Number and Status Display
The Label component made for the purpose.

```python
# Show message on status label
self.statusLabel.setText("Program Done!")
# Show error message on status label 
self.statusLabel.setText("Please connect to device.")

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
The dynamic scan adapter is basic requirement of a programmer tool. Using Python threading Timer can achieve the purpose. 

```python
from threading import Timer
# Scan adapter every 3 seconds
def mainloop(self):
    self.scan_adapter()
    Timer(3, self.mainloop).start()
    return
```

### 3.3 JLink function
In order to communicate with STK on board Segger JLink controller, the Python script needs to talk with JLinkARM.DLL, and the JLinkARM.DLL pass the command to the STK JLink controller. 

The Jlink.py act as interpret layer between JLinkARM.DLL and Main Control routine. 
There are several useful interface functions used in this programmer tool. 

```python
# Loading JLinkARM.DLL
self._jlink = jlink.JLinkDll()

# Connect jLink device with serial_number, debug interface ifc
retval = self._jlink.connect(long(serial_number), None, [ifc])

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



## 4 User Guide
   Attached STK board to the system via USB cable. for instance, EFM32PG1B STK board. 
Run programmer.py in CMD console, the GUI tool displayed in screen. 

### 4.1 Connect to Device
![PT connect][PT_connect]

1. Select the adapter with correct serial number in __J-link Device S/N__ Combox. 
2. Choose SWD from __Debug IF__ Combox. 
3. Click on __Connect__ button. 

### 4.2 Select Download File
![PT select][PT_select]

1. Select the adapter with correct serial number in __J-link Device S/N__ Combox. 
2. Choose SWD from __Debug IF__ Combox. 
3. Click on __Connect__ button. 


### 4.3 Flashing Device
The Segger J-link v6.18c pop-up a progress dialog

![PT flashing][PT_flashing]

Once the flashing is done, the GUI tool display status message __Program Done!__

![PT program done][PT_program_done]



[PT_connect]:img/pt-connect.png
[PT_select]:img/pt-select.png
[PT_flashing]:img/pt-flashing.png
[PT_program_done]:img/pt-program-done.png
[Segger_jlink_download]:img/segger-jlink-download.png
[PyCharm]:img/pycharm.png
[PySide_doc]:img/pyside-doc.png
[Qt_creator]:img/qt-creator.png
[Programmer]:img/programmer.png
[Browse_file]:img/browse-file.png

