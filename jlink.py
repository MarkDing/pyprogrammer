"""
jlink.py:  JLinkARM.dll Wrapper - Python Edition

This module provides access to all functions of JLinkARM.dll.

"""
import ctypes as ct
import os
import sys
import logging
from enum import Enum, unique

from jlink_constants import *

@unique
class JLINKARM_GLOBAL_ERROR(Enum):
    JLINK_ERR_EMU_NO_CONNECTION          = -256
    JLINK_ERR_EMU_COMM_ERROR             = -257
    JLINK_ERR_DLL_NOT_OPEN               = -258
    JLINK_ERR_VCC_FAILURE                = -259
    JLINK_ERR_INVALID_HANDLE             = -260
    JLINK_ERR_NO_CPU_FOUND               = -261
    JLINK_ERR_EMU_FEATURE_NOT_SUPPORTED  = -262
    JLINK_ERR_EMU_NO_MEMORY              = -263
    JLINK_ERR_TIF_STATUS_ERROR           = -264
    JLINK_ERR_FLASH_PROG_COMPARE_FAILED  = -265
    JLINK_ERR_FLASH_PROG_PROGRAM_FAILED  = -266
    JLINK_ERR_FLASH_PROG_VERIFY_FAILED   = -267
    JLINK_ERR_OPEN_FILE_FAILED           = -268
    JLINK_ERR_UNKNOWN_FILE_FORMAT        = -269
    JLINK_ERR_WRITE_TARGET_MEMORY_FAILED = -270

JLINKARM_GLOBAL_ERROR_DESC = {
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_EMU_NO_CONNECTION          : "No connection to emulator / Connection to emulator lost",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_EMU_COMM_ERROR             : "Emulator communication error (host-interface module reproted error)",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_DLL_NOT_OPEN               : "DLL has not been opened but needs to be (JLINKARM_Open() needs to be called first)",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_VCC_FAILURE                : "Target system has no power (Measured VTref < 1V)",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_INVALID_HANDLE             : "File handle / memory area handle needed for operation, but given handle is not valid",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_NO_CPU_FOUND               : "Could not find supported CPU",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_EMU_FEATURE_NOT_SUPPORTED  : "Emulator does not support the selected feature (Usually returned by functions which need specific emulator capabilities)",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_EMU_NO_MEMORY              : "Emulator does not have enough memory to perform the requested operation",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_TIF_STATUS_ERROR           : "Things such as 'TCK is low but should be high'",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_FLASH_PROG_COMPARE_FAILED  : "Flash program compare failure",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_FLASH_PROG_PROGRAM_FAILED  : "Flash program operation failure",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_FLASH_PROG_VERIFY_FAILED   : "Flash program verify failure",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_OPEN_FILE_FAILED           : "Config file open failure",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_UNKNOWN_FILE_FORMAT        : "Config file unknown format",
    JLINKARM_GLOBAL_ERROR.JLINK_ERR_WRITE_TARGET_MEMORY_FAILED : "Write target memory failure",
}

def GetErrorDesc(error):
    try:
        errStr = JLINKARM_GLOBAL_ERROR_DESC[JLINKARM_GLOBAL_ERROR(error)]
    except (ValueError, KeyError) as err:
        errStr = "Unsupported error code '{}' triggered {}".format(error, err)
    return errStr


class JLinkDll:
    """
    Object for accessing and controlling a JLink adapter
    """
    # Maximum number of adapters this wrapper can find.
    MAX_NUM_ADAPTERS = 32
    logger = None
    def __init__(self):
        try:
            # Get the path to slab8051.dll in the Studio installation
            cwd = os.getcwd()
            # Load JLinkARM.dll
            self._dll = ct.cdll.LoadLibrary("JLinkARM.dll")
            self._windll = ct.windll.LoadLibrary("JLinkARM.dll")
            os.chdir(cwd)
        except:
            print("Unable to load JLinkDll class")

        # Keep a list of all adapters
        self._num_adapters, self._adapter_list = self.get_usb_adapter_list()

        # Initialize all properties of the connected MCU
        self._initialize_mcu_properties()

        # Suppress dialog from the DLL
        self._suppress_usb_dialog()

        self._init_logger()

    def _init_logger(self):
        logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s: %(message)s') 
        self.logger = logging.getLogger()

    def abort(self, errMsg):
        self.logger.error(errMsg)
        self._dll.JLINKARM_Close()
        self._initialize_mcu_properties()

    def _jlink_arm_execute_command_string(self, command_string):
        """
        Execute a JLink command string.

        Keyword arguments:
        command_string -- the string to execute with JLINKARM_ExecCommand()

        Returns the return value of the executed command.
        """
        command_string = ct.c_char_p(command_string)
        error = ct.create_string_buffer(256)
        buffer_size = ct.c_int(256)
        retval = self._dll.JLINKARM_ExecCommand(command_string,
                                                error,
                                                buffer_size)

        # If error has a value, report that value as an exception
        if error[0] != "\0":
            errMsg = "JLINKARM_ExecCommand() returned error {}".format(error.raw)
            self.abort(errMsg)
            return False

        return retval

    def _initialize_mcu_properties(self):
        """
        Resest all internal variables tracking the properties of the
        attached MCU.
        """
        self._mcu_interface_type = None
        self._mcu_core = None
        self._id_code = None
        self._part_family = None
        self._part_number = None
        self._part_number_id = None
        self._flash_size = None

    def _suppress_usb_dialog(self):
        """
        Suppresses dialog message from JLinkARM.dll.
        """
        result = self._jlink_arm_execute_command_string("SuppressEmuUSBDialog")
        if result != 0:
            errMsg = "Connect: JLINKARM_ExecCommand({}): {}".format("SuppressEmuUSBDialog", GetErrorDesc(result))
            self.abort(errMsg)

    def _locked_part_callback(self, sTitle, sMessage, Flags):
        """
        Callback function called if attached part is locked.
        This prevents pop-up dialog from JLINK DLL.
        """
        JLINK_DLG_BUTTON_NO = (1 << 1)

        return JLINK_DLG_BUTTON_NO

    def get_usb_adapter_list(self):
        """
        Returns a list of all adapters connected to the host via USB.
        """
        host_ifs = ct.c_int(JLINKARM_HOSTIF_USB)
        connect_info = \
            (JLinkArmEmuConnectInfo_CStruct * self.MAX_NUM_ADAPTERS)()
        max_info = ct.c_int(self.MAX_NUM_ADAPTERS)

        num_adapters = self._dll.JLINKARM_EMU_GetList(host_ifs,
                                                      ct.byref(connect_info),
                                                      max_info)
        # Create a list of information for each adapter
        adapter_list = []
        for i in range(num_adapters):
            adapter_list.append(connect_info[i])
        self._num_adapters = num_adapters
        self._adapter_list = adapter_list
        return num_adapters, adapter_list

    def get_tcp_ip_adapter_list(self):
        """
        Returns a list of all adapters connected to the host via TCP/IP.
        """
        host_ifs = ct.c_int(JLINKARM_HOSTIF_IP)
        connect_info = \
            (JLinkArmEmuConnectInfo_CStruct * self.MAX_NUM_ADAPTERS)()
        max_info = ct.c_int(self.MAX_NUM_ADAPTERS)

        num_adapters = self._dll.JLINKARM_EMU_GetList(host_ifs,
                                                      ct.byref(connect_info),
                                                      max_info)
        # Create a list of information for each adapter
        adapter_list = []
        for i in range(num_adapters):
            adapter_list.append(connect_info[i])

        return num_adapters, adapter_list

    def get_adapter_list(self):
        """
        Returns a list of all adapters connected to the host via TCP/IP or USB.
        """
        host_ifs = ct.c_int(JLINKARM_HOSTIF_USB | JLINKARM_HOSTIF_IP)
        connect_info = \
            (JLinkArmEmuConnectInfo_CStruct * self.MAX_NUM_ADAPTERS)()
        max_info = ct.c_int(self.MAX_NUM_ADAPTERS)

        num_adapters = self._dll.JLINKARM_EMU_GetList(host_ifs,
                                                      ct.byref(connect_info),
                                                      max_info)
        # Create a list of information for each adapter
        adapter_list = []
        for i in range(num_adapters):
            adapter_list.append(connect_info[i])

        return num_adapters, adapter_list

    def connect(self,
                serial_number,
                ifc):
        # First, look for the adapter in the adapter list
        # num_adapters, adapter_list = self.get_usb_adapter_list()
        found_adapter = False
        for adapter in self._adapter_list:
            if adapter.SerialNumber == serial_number:
                found_adapter = True
                break

        if not found_adapter:
            errMsg = "Unable to find adapter with serial number {}".format(serial_number)
            self.abort(errMsg)
            return False

        self._suppress_usb_dialog()
        # serial_number = ct.c_uint32(serial_number)

        # USB Adapter
        if adapter.Connection == JLINKARM_HOSTIF_USB:
            error = self._dll.JLINKARM_EMU_SelectByUSBSN(serial_number)
            if error < 0:
                errMsg = "Connect: {} Unable to select {} on USB interface".format(error, serial_number)
                self.abort(errMsg)
                return False
        else:
            print("TCP/IP support currently not implemented in jlink.py.")
            return False

        # register local error handler to suppress blocking dialog pop-up errors
        # _REF_ErrorOutHandler = self._dll.JLINKARM_LOG(self.ErrorOutHandler)
        # self._dll.JLINKARM_SetErrorOutHandler(_REF_ErrorOutHandler)

        # register local error handler to suppress blocking dialog pop-up errors
        # _REF_WarnOutHandler = self._dll.JLINKARM_LOG(self.WarnOutHandler)
        # self._dll.JLINKARM_SetWarnOutHandler(_REF_WarnOutHandler)

        self._initialize_mcu_properties()
        result = self._dll.JLINKARM_Open()
        if result:
            errMsg = "Connect: JLINKARM_Open: {}".format(result)
            self.abort(errMsg)
            return False

        result = self._dll.JLINKARM_HasError()
        if result:
            errMsg = "Connect: JLINKARM_HasError: {}".format(result)
            self.abort(errMsg)
            return False

        if ifc.upper() == "C2":
            interface = JLINKARM_TIF_C2
            self._dll.JLINKARM_TIF_Select(interface)
            self.set_device("EFM8SB20F64G")
        elif ifc.upper() == "SWD":
            interface = JLINKARM_TIF_SWD
            self._dll.JLINKARM_TIF_Select(interface)
            self.set_device("EFM32GG990F1024")
        else:
            errMsg = "Unkown Debug Interface: {}".format(ifc)
            self.abort(errMsg)
            return False

        # self._windll.JLINK_SetHookUnsecureDialog(
        #     JLINK_UNSECURE_DIALOG_CB_FUNC_TYPE(self._locked_part_callback))

        # self._dll.JLINKARM_TIF_Select(interface)

        # Set to maximum speed
        speed_info = self.get_speed_info()
        self._dll.JLINKARM_SetSpeed(ct.c_uint32(speed_info["BaseFreq"] / 
            speed_info["MinDiv"] / 1000))
        
        result = self._dll.JLINKARM_ExecCommand("SuppressEmuUSBDialog", 0, 0)
        if result < 0:
            errMsg = "Connect: JLINKARM_ExecCommand({}): {}".format(
                "SuppressEmuUSBDialog", GetErrorDesc(result))
            self.abort(errMsg)
            return False
        self._suppress_usb_dialog()

        # Connect, halt, and get the Part ID
        result = self._dll.JLINKARM_Connect()
        if result < 0:
            errMsg = "Connect: JLINKARM_Connect: {}".format(GetErrorDesc(result))
            self.abort(errMsg)
            return False

        self._dll.JLINKARM_Halt()

        id_data = self.get_id_data()
        
        SWD_PREFIXES = ["EFM32", "EFR32"]
        C2_PREFIXES = ["EFM8", "C8051", "Si"]

        if interface == JLINKARM_TIF_SWD:
            # self.reset()
            # Get the ID code in the correct format
            self._idcode = id_data.aId[0] / 0x10000 + id_data.aId[1] * 0x10000
            if self._idcode == 0x0BC11477:
                self._core = MCU_CORE_M0
                core_string = "M0+"
            elif self._idcode == 0x2BA01477:
                self._core = MCU_CORE_M3_M4
                core_string = "M3/M4"
            # Get the part number
            self._part_number_id = self.read_ram_arm_16(0x0FE081FC, 1)[0]
            self._part_family = self.read_ram_arm_8(0x0FE081FE, 1)[0]
            self._flash_size = self.read_ram_arm_16(0x0FE081F8, 1)[0]
            # self._temp_grade = self.read_ram_arm_8(0x0FE081E4, 1)[0]
            # self._pkg_type = self.read_ram_arm_8(0x0FE081E5, 1)[0]
            self._pin_count = self.read_ram_arm_8(0x0FE081E6, 1)[0]

            self._part_number = EFM32_PART_PREFIX[self._part_family] + \
                str(self._part_number_id) + 'F' + str(self._flash_size)

            # For now, only EFM32JG and EFM32PG needs pin count. And "GM"
            # only for the current support list.
            if EFM32_PART_PREFIX[self._part_family] == "EFM32JG1B" or \
                    EFM32_PART_PREFIX[self._part_family] == "EFM32PG1B":
                self._part_number += "GM" + str(self._pin_count)

        elif interface == JLINKARM_TIF_C2:
            self._idcode = id_data.aId[0] / 0x10000
            self._part_family = self._idcode
            self._core = MCU_CORE_8051
            core_string = "8051"
            self._part_number_id = self.read_mem(
                JLINK_EFM8_START_ADDR_DSR + JLINK_EFM8_OFF_REG_DSR_DERIVATIVE,
                1)[0]
            self._part_number = MCU_EFM8_DERIVS[self._part_family][self._part_number_id]

        self.set_device(self._part_number)
        # self._dll.JLINKARM_Connect()

        # print("Adapter Connection Information:")
        # print("  Connection Type:      %s" % connection_type_string)
        # print("  MCU Core:             %s" % core_string)
        # if self._core == MCU_CORE_8051:
        #     print("  Hardware Family:      %s, (0x%X)" %
        #           (MCU_8051_FAMILY[self._idcode], self._part_family))
        # elif self._core == MCU_CORE_M0 or self._core == MCU_CORE_M3_M4:
        #     print("  Hardware Family:      %s (0x%X)" %
        #           (MCU_EFM32_FAMILY[self._part_family], self._part_family))
        # else:
        #     print("  ID:                 0x%X" % self._idcode)
        # print("  Part Number:          %s (0x%X)" %
        #       (self._part_number, self._part_number_id))
        return True

    def close(self):
        """
        Closes the connection to the JLink adapter.
        """
        self._dll.JLINKARM_Close()
        self._initialize_mcu_properties()

    def get_speed(self):
        """
        Returns the current JTAG connection speed.
        """
        speed = self._dll.JLINKARM_GetSpeed()
        return speed

    def set_max_speed(self):
        """
        Sets the JTAG connection speed to its maximum value.
        """
        self._dll.JLINKARM_SetMaxSpeed()

    def set_speed(self, speed=4000):
        """
        Sets the JTAG connection speed.

        Keyword arguments:
        speed -- speed of JTAG connection in kHz.
        """
        self._dll.JLINKARM_SetSpeed(ct.c_uint32(speed))

    def get_speed_info(self):
        """
        Gets the target interface speed information.

        Returns a dictionary containing the speed information.
        """
        speed_info = JlinkArm_Speed_Info_CStruct()
        speed_info.SizeOfStruct = ct.c_uint32(ct.sizeof(speed_info))
        self._dll.JLINKARM_GetSpeedInfo(ct.pointer(speed_info))

        return {"BaseFreq": speed_info.BaseFreq,
                "MinDiv": speed_info.MinDiv,
                "SupportAdaptive": bool(speed_info.SupportAdaptive)}

    def get_id(self):
        """
        Retrives ID of the core.
        """
        id = self._dll.JLINKARM_GetId()
        return id

    def get_id_data(self):
        """
        Retrives detailed info of the device on the JTAG bus.
        """
        id_data = JLinkJtagIdData_CStruct()
        self._dll.JLINKARM_GetIdData(ct.pointer(id_data))
        return id_data

    def run(self):
        self._dll.JLINKARM_Go()

    def go_ex(self):
        """
        Runs the currently connected device, skipping over any breakpoint at the current instruction.
        """
        self._dll.JLINKARM_GoEx(ct.c_uint32(JLINKARM_GO_MAX_EMUL_INSTS_DEFAULT),
                                ct.c_uint32(JLINKARM_GO_FLAG_OVERSTEP_BP))

    def step(self):
        self._dll.JLINKARM_Step()

    def halt(self):
        self._dll.JLINKARM_Halt()

    def reset(self, halt=True):
        """
        Resets the currently connected device.

        Keyword arguments:
        halt -- if true, the part will be halted before reset
                if false, the part will not be halted before reset
        """
        if halt:
            self._dll.JLINKARM_Reset()
        else:
            self._dll.JLINKARM_ResetNoHalt()

    def get_device_family(self):
        return self._dll.JLINKARM_GetDeviceFamily()

    def set_device(self, device):
        result = self._jlink_arm_execute_command_string("device = %s" % device)
        if result != 0:
            errMsg = "Connect: JLINKARM_ExecCommand(\"{}\"): {}".format("device = {}".format(device.upper()),
                                                                                GetErrorDesc(result))
            self.abort(errMsg)

    def read_mem(self, address, num_bytes):
        data = ct.create_string_buffer(num_bytes)
        status = ct.create_string_buffer(256)
        result = self._dll.JLINKARM_ReadMem(ct.c_uint32(address),
                                            ct.c_uint32(num_bytes),
                                            ct.pointer(data),
                                            ct.pointer(status))
        if result:
            errMsg = "ReadMem: Failure result {} reading {} bytes at '{:#010x}'".format(result, num_bytes, address)
            self.abort(errMsg)
        # Convert to a list of integers
        ret_buffer = []
        for byte in data.raw:
            ret_buffer.append(ord(byte))

        return ret_buffer

    def read_ram_arm_8(self, address, num_bytes):
        data = ct.create_string_buffer(num_bytes)
        status = ct.create_string_buffer(256)
        self._dll.JLINKARM_ReadMemU8(ct.c_uint32(address),
                                     ct.c_uint32(num_bytes),
                                     ct.pointer(data),
                                     ct.pointer(status))
        # Convert to a list of 8-bit integers
        ret_buffer = []
        for byte in data.raw:
            ret_buffer.append(ord(byte))

        return ret_buffer

    def read_ram_arm_16(self, address, num_words):
        data = ct.create_string_buffer(num_words * 2)
        status = ct.create_string_buffer(256)
        self._dll.JLINKARM_ReadMemU16(ct.c_uint32(address),
                                      ct.c_uint32(num_words),
                                      ct.pointer(data),
                                      ct.pointer(status))
        # Convert to a list of 16-bit integers
        ret_buffer = []
        for i in range(num_words):
            ret_buffer.append(
                (ord(data[(i * 2) + 1]) * 256) + ord(data[i * 2]))

        return ret_buffer

    def read_ram_arm_32(self, address, num_words):
        data = ct.create_string_buffer(num_words * 4)
        status = ct.create_string_buffer(256)
        self._dll.JLINKARM_ReadMemU32(ct.c_uint32(address),
                                      ct.c_uint32(num_words),
                                      ct.pointer(data),
                                      ct.pointer(status))
        # Convert to a list of 32-bit integers
        ret_buffer = []
        for i in range(num_words):
            ret_buffer.append((ord(data[(i * 2) + 3]) * 0x1000000) +
                              (ord(data[(i * 2) + 2]) * 0x10000) +
                              (ord(data[(i * 2) + 1]) * 0x100) +
                              ord(data[i * 2]))

        return ret_buffer

    def read_ram_arm_64(self, address, num_words):
        """
        Reads a block of RAM in 64-bit words.

        Keyword arguments:
        address -- starting address to read
        num_words -- number of 64-bit words to read
        """
        data = ct.create_string_buffer(num_words * 8)
        status = ct.create_string_buffer(256)
        self._dll.JLINKARM_ReadMemU64(ct.c_uint32(address),
                                      ct.c_uint32(num_words),
                                      ct.pointer(data),
                                      ct.pointer(status))
        # Convert to a list of 64-bit integers
        ret_buffer = []
        for i in range(num_words):
            ret_buffer.append((ord(data[(i * 2) + 7]) * 0x100000000000000) +
                              (ord(data[(i * 2) + 6]) * 0x1000000000000) +
                              (ord(data[(i * 2) + 5]) * 0x10000000000) +
                              (ord(data[(i * 2) + 4]) * 0x100000000) +
                              (ord(data[(i * 2) + 3]) * 0x1000000) +
                              (ord(data[(i * 2) + 2]) * 0x10000) +
                              (ord(data[(i * 2) + 1]) * 0x100) +
                              ord(data[i * 2]))

        return ret_buffer

    def clear_breakpoint(self, bp_to_clear):
        '''
        Clears breakpoint on the connected device.

        Keyword arguments:
        bp_to_clear - Handle of the breakpoint to clear. 
            Pass JLINKARM_BP_HANDLE_ALL to clear all breakpoints.
        '''
        result = self._dll.JLINKARM_ClrBPEx(ct.c_int32(bp_to_clear))
        if result:
            errMsg = "JLINKARM_ClrBPEx command failed with return code {}".format(GetErrorDesc(result))
            self.abort(errMsg)

    def clear_all_breakpoints(self):
        result = self._dll.JLINKARM_ClrBPEx(
            ct.c_uint32(JLINKARM_BP_HANDLE_ALL))
        if result:
            errMsg = "JLINKARM_ClrBPEx clear all failed with return code {}".format(GetErrorDesc(result))
            self.abort(errMsg)

    def read_reg(self, register):
        ''' 
        Read an architectural register in the CPU.

        register - Register number (ie in JLINK_EFM8_REG)

        Returns value of register.
        Does not return error message on failure.
        '''
        return self._dll.JLINKARM_ReadReg(ct.c_int32(register))

    def set_breakpoint(self, address, typeflags):
        '''
        Set a breakpoint within the CPU.

        address - Address for the breakpoint.
        typeflags - Flags for the breakpoint.  Ignored for EFM8 devices.
        '''
        result = self._dll.JLINKARM_SetBPEx(ct.c_uint32(address),
                                            ct.c_uint32(typeflags))
        if result:
            errMsg = "JLINKARM_SetBPEx clear all failed with return code {}".format(GetErrorDesc(result))
            self.abort(errMsg)
        return result

    def write_mem(self, address, count, data):
        data_buffer = ct.create_string_buffer(len(data))
        for idx, byte in enumerate(data):
            data_buffer[idx] = chr(byte)

        result = self._dll.JLINKARM_WriteMem(ct.c_uint32(address),
                                             ct.c_uint32(count),
                                             ct.byref(data_buffer))
        if result < 0:
            errMsg = "WriteMem: Failure result {} when writing {} bytes to address {:#010x}".format(GetErrorDesc(result), count, address)
            self.abort(errMsg)
        elif result != byteCnt:
            errMsg = "WriteMem: Incomplete write of {} bytes (expected {}) to address {:#010x}".format(result, count, address)
            self.abort(errMsg)

        return result

    def write_reg(self, register, value):
        result = self._dll.JLINKARM_WriteReg(ct.c_int32(register),
                                             ct.c_uint32(data))
        if result != 0:
            self.abort("WriteReg failure with result '{}'".format(result))

    def write_u8(self, address, data):
        retval = self._dll.JLINKARM_WriteU8(ct.c_uint32(address),
                                            ct.c_uint8(data))

    def write_u16(self, address, data):
        retval = self._dll.JLINKARM_WriteU16(ct.c_uint32(address),
                                             ct.c_uint16(data))

    def write_u32(self, address, data):
        retval = self._dll.JLINKARM_WriteU32(ct.c_uint32(address),
                                             ct.c_uint32(data))

    def write_u64(self, address, data):
        retval = self._dll.JLINKARM_WriteU64(ct.c_uint32(address),
                                             ct.c_uint64(data))

    def erase_chip(self):
        """
        Erases all user flash on the connected device.
        """
        result = self._windll.JLINK_EraseChip()
        if result < 0:
            errMsg = "Erase Chip Failed with Error code {}".format(result)
            self.abort(errMsg)
            return False
        return True

    def download(self, image, offset=0):
        if not os.path.isfile(image):
            print('Could not find image file %s' % image)

        file_name = ct.c_char_p(image)
        retval = self._windll.JLINK_DownloadFile(
            file_name, ct.c_uint32(offset))
        self.reset()

    @classmethod
    def ErrorOutHandler(cls, errorMsg):
        """
        Log error from the DLL.

        :param errorMsg: The DLL error message.
        """
        if cls.logger:
            cls.logger.error(errorMsg.data)

        cls.library_error_list.append(errorMsg.data)

    @classmethod
    def WarnOutHandler(cls, warnMsg):
        """
        Log warning from the DLL.

        :param warnMsg: The DLL error message.
        """
        if cls.logger:
            cls.logger.warn(warnMsg.data)