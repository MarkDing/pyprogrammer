"""
jlink_constants.py:  Constants for JLinkARM.dll Wrapper - Python Edition

This module provides constants used by the JLinkARM.dll wrapper jlink.py.
"""
import ctypes as ct

# Adapter Interfaces
JLINKARM_HOSTIF_USB = 0x01
JLINKARM_HOSTIF_IP  = 0x02

# Debug Interfaces
JLINKARM_TIF_JTAG               =   0
JLINKARM_TIF_SWD                =   1
JLINKARM_TIF_BDM3               =   2
JLINKARM_TIF_FINE               =   3
JLINKARM_TIF_2_WIRE_JTAG_PIC32  =   4
JLINKARM_TIF_SPI                =   5
JLINKARM_TIF_C2                 =   6

# MCU Cores
MCU_CORE_M0                     =   0
MCU_CORE_M3_M4                  =   1
MCU_CORE_8051                   =   2

# EFM32 MCU's
MCU_EFM32_FAMILY = { 16  : "EFR32 Mighty Gecko",
                     17  : "EFR32 Mighty Gecko",
                     18  : "EFR32 Mighty Gecko",
                     19  : "EFR32 Blue Gecko",
                     20  : "EFR32 Blue Gecko",
                     21  : "EFR32 Blue Gecko",
                     22  : "EFR32 Zappy Gecko",
                     23  : "EFR32 Zappy Gecko",
                     24  : "EFR32 Zappy Gecko",
                     25  : "EFR32 Flex Gecko",
                     26  : "EFR32 Flex Gecko",
                     27  : "EFR32 Flex Gecko",
                     71  : "EFM32 Gecko",
                     72  : "EFM32 Giant Gecko",
                     73  : "EFM32 Tiny Gecko",
                     74  : "EFM32 Leopard Gecko",
                     75  : "EFM32 Wonder Gecko",
                     76  : "EFM32 Zero Gecko",
                     77  : "EFM32 Happy Gecko",
                     81  : "EFM32 Pearl Gecko",
                     83  : "EFM32 Jade Gecko",
                     120 : "EZR32 Leopard Gecko",
                     121 : "EZR32 Wonder Gecko",
                     122 : "EZR32 Happy Gecko",
                    }

# 8051 MCU's
MCU_8051_FAMILY = { 0x00 : "C8051F0xx (Cindy)",
                    0x01 : "C8051F2xx (Twiggy)",
                    0x02 : "C8051F0xx (Cindy Plus)",
                    0x03 : "C8051F02x (Dot/YAC)",
                    0x04 : "C8051F30x (Minnie)",
                    0x05 : "C8051F04x (Candy)",
                    0x06 : "C8051F06x (Ginger)",
                    0x07 : "C8051F12x/13x (CindyGT)",
                    0x08 : "C8051F31x (Barbie)",
                    0x09 : "C8051F320/1 (Uma)",
                    0x0A : "C8051F33x (Kellie)",
                    0x0B : "C8051F35x (Chloe)",
                    0x0C : "C8051F41x/42x (Lola)",
                    0x0D : "C8051F326/7 (Ernie)",
                    0x0E : "Si825x (Tonya)",
                    0x0F : "C8051F34x (Umami)",
                    0x10 : "C8051T60x (Piccolo)",
                    0x11 : "C8051F52x/53x (Samson)",
                    0x12 : "C8051F36x (Juno)",
                    0x13 : "C8051T61x (Fife)",
                    0x14 : "C8051F336/7/8/9 (Merlion)",
                    0x15 : "Si81xx (Eliza)",
                    0x16 : "EFM8SB2, C8051F92x/93x (Henry)",
                    0x17 : "C8051T63x (Flute)",
                    0x18 : "C8051T620/1 (Whistle)",
                    0x19 : "C8051T622/3 (Harmonica)",
                    0x1A : "C8051T624/5 (Kazoo)",
                    0x1B : "C8051T606 (Piccolino)",
                    0x1C : "C8051F50x/51x (Hammer)",
                    0x1D : "Si3456F336 (MerlionPOE)",
                    0x1E : "C8051F70x/71x (Centipede)",
                    0x1F : "C8051F901/02/11/12 (Henrietta)",
                    0x20 : "C8051F58x/59x (Cayenne)",
                    0x21 : "C8051F54x",
                    0x22 : "C8051F54x/55x/56x/57x (Boxman)",
                    0x23 : "C8051F8xx",
                    0x24 : "Si401x",
                    0x25 : "EFM8SB1, C8051F99x (Etta)",
                    0x26 : "C8051F610POE",
                    0x27 : "Si114x",
                    0x28 : "EFM8UB2, C8051F38x (Taya)",
                    0x29 : "C8051F75x (Quickdraw)",
                    0x2A : "C8051F96x (Metron)",
                    0x2B : "C8051F37x/39x (Kylin)",
                    0x2C : "WhistlePOE",
                    0x2D : "Si2178",
                    0x2E : "C8051F77x (Roadrunner)",
                    0x2F : "Si7010 (Humidity Sensor)",
                    0x30 : "EFM8BB1, C8051F85x (ULC8)",
                    0x31 : "Si7030",
                    0x32 : "EFM8UB1/BB2 (Shanghai)",
                    0x33 : "POE",
                    0x34 : "EFM8LB1/BB3 (Sydney)",
                    0x35 : "Si1150",
                    0x36 : "EFM8UB3/UB4 (Delphi)",
                    0x37 : "Si5332",
                    0x38 : "Si1170",
                  }

# EFM8UB1/BB2 Derivatives
MCU_EFM8UB1_BB2_DERIVS = { 0x01 : "EFM8BB22F16G",
                           0x02 : "EFM8BB21F16G",
                           0x03 : "EFM8BB21F16G",
                           0x11 : "EFM8BB22F16I",
                           0x12 : "EFM8BB21F16I",
                           0x13 : "EFM8BB21F16I",
                           0x21 : "EFM8BB22F16A",
                           0x22 : "EFM8BB21F16A",
                           0x23 : "EFM8BB21F16A",
                           0x41 : "EFM8UB10F16G",
                           0x43 : "EFM8UB10F16G",
                           0x45 : "EFM8UB11F16G",
                           0x49 : "EFM8UB10F8G",
                           0x4A : "EFM8UB11F16G",
                         }

# EFM8UB2 Derivatives
MCU_EFM8UB2_DERIVS = { 0x60 : "EFM8UB20F64G",
                       0x61 : "EFM8UB20F64G",
                       0x62 : "EFM8UB20F64G",
                       0x63 : "EFM8UB20F32G",
                       0x64 : "EFM8UB20F32G",
                       0x65 : "EFM8UB20F32G",
                       0xD0 : "C8051F380",
                       0xD1 : "C8051F381",
                       0xD2 : "C8051F382",
                       0xD3 : "C8051F383",
                       0xD4 : "C8051F384",
                       0xD5 : "C8051F385",
                       0xD6 : "C8051F386",
                       0xD7 : "C8051F387",
                       0xD8 : "C8051F388",
                       0xD9 : "C8051F389",
                       0xDA : "C8051F38A",
                       0xDB : "C8051F38B",
                       0xDC : "C8051F38C",
                       0xE8 : "C8051F388U",
                       0xE9 : "C8051F389U",
                       0xEA : "C8051F38AU",
                       0xEB : "C8051F38BU",
                       0xEC : "C8051F38CU",
                     }

# EFM8SB1 Derivatives
MCU_EFM8SB1_DERIVS = { 0xD0 : "C8051F990",
                       0xD1 : "C8051F991",
                       0xD2 : "C8051F997",
                       0xD3 : "C8051F980",
                       0xD4 : "C8051F981",
                       0xD5 : "C8051F982",
                       0xD6 : "C8051F996",
                       0xD7 : "C8051F983",
                       0xD8 : "C8051F985",
                       0xD9 : "C8051F986",
                       0xDA : "C8051F987",
                       0xDB : "C8051F988",
                       0xDC : "C8051F989",
                       0xE0 : "C8051F990-B1",
                       0xE1 : "C8051F991-B1",
                       0xE2 : "C8051F997-B1",
                       0xE3 : "C8051F980-B1",
                       0xE4 : "C8051F981-B1",
                       0xE5 : "C8051F982-B1",
                       0xE6 : "C8051F996-B1",
                       0xE7 : "C8051F983-B1",
                       0xE8 : "C8051F985-B1",
                       0xE9 : "C8051F986-B1",
                       0xEA : "C8051F987-B1",
                       0xEB : "C8051F988-B1",
                       0xEC : "C8051F989-B1",
                       0x01 : "EFM8SB10F8G",
                       0x02 : "EFM8SB10F8G",
                       0x03 : "EFM8SB10F8G",
                       0x04 : "EFM8SB10F4G",
                       0x05 : "EFM8SB10F4G",
                       0x06 : "EFM8SB10F4G",
                       0x07 : "EFM8SB10F2G",
                       0x08 : "EFM8SB10F2G",
                       0x09 : "EFM8SB10F2G",
                       0x0A : "EFM8SB10F8G",
                     }

# EFM8SB2 Derivatives
MCU_EFM8SB2_DERIVS = { 0x01 : "EFM8SB20F64G",
                       0x02 : "EFM8SB20F64G",
                       0x03 : "EFM8SB20F64G",
                       0x04 : "EFM8SB20F32G",
                       0x05 : "EFM8SB20F32G",
                       0x06 : "EFM8SB20F32G",
                       0x09 : "EFM8SB20F16G",
                       0xB1 : "C8051F920",
                       0xB3 : "C8051F921",
                       0x56 : "C8051F930",
                       0x5E : "C8051F931",
                       0xD0 : "Si1000",
                       0xD1 : "Si1001",
                       0xD2 : "Si1002",
                       0xD3 : "Si1003",
                       0xD4 : "Si1004",
                       0xD5 : "Si1005",
                       0xE0 : "Si1060",
                       0xE1 : "Si1061",
                       0xE2 : "Si1062",
                       0xE3 : "Si1063",
                       0xE4 : "Si1064",
                       0xE5 : "Si1065",
                     }

# EFM8BB1 Derivatives
MCU_EFM8BB1_DERIVS = { 0x01 : "EFM8BB10F8G",
                       0x02 : "EFM8BB10F8G",
                       0x03 : "EFM8BB10F8G",
                       0x04 : "EFM8BB10F4G",
                       0x05 : "EFM8BB10F4G",
                       0x06 : "EFM8BB10F4G",
                       0x07 : "EFM8BB10F2G",
                       0x08 : "EFM8BB10F2G",
                       0x09 : "EFM8BB10F2G",
                       0x11 : "EFM8BB10F8I",
                       0x12 : "EFM8BB10F8I",
                       0x13 : "EFM8BB10F8I",
                       0x14 : "EFM8BB10F4I",
                       0x15 : "EFM8BB10F4I",
                       0x16 : "EFM8BB10F4I",
                       0x17 : "EFM8BB10F2I",
                       0x18 : "EFM8BB10F2I",
                       0x19 : "EFM8BB10F2I",
                       0x21 : "EFM8BB10F8Y",
                       0x22 : "EFM8BB10F8Y",
                       0x23 : "EFM8BB10F8Y",
                       0x24 : "EFM8BB10F4Y",
                       0x25 : "EFM8BB10F4Y",
                       0x26 : "EFM8BB10F4Y",
                       0x27 : "EFM8BB10F2Y",
                       0x28 : "EFM8BB10F2Y",
                       0x29 : "EFM8BB10F2Y",
                       0x31 : "EFM8BB10F8A",
                       0x32 : "EFM8BB10F8A",
                       0x33 : "EFM8BB10F8A",
                       0x34 : "EFM8BB10F4A",
                       0x35 : "EFM8BB10F4A",
                       0x36 : "EFM8BB10F4A",
                       0x37 : "EFM8BB10F2A",
                       0x38 : "EFM8BB10F2A",
                       0x39 : "EFM8BB10F2A",
                       0xD0 : "C8051850-GU",
                       0xD1 : "C8051851-GU",
                       0xD2 : "C8051852-GU",
                       0xD3 : "C8051853-GU",
                       0xD4 : "C8051854-GU",
                       0xD5 : "C8051855-GU",
                       0xE0 : "C8051860-GS",
                       0xE1 : "C8051861-GS",
                       0xE2 : "C8051862-GS",
                       0xE3 : "C8051863-GS",
                       0xE4 : "C8051864-GS",
                       0xE5 : "C8051865-GS",
                       0xF0 : "C8051850-GM",
                       0xF1 : "C8051851-GM",
                       0xF2 : "C8051852-GM",
                       0xF3 : "C8051853-GM",
                       0xF4 : "C8051854-GM",
                       0xF5 : "C8051855-GM",
                     }

# EFM8LB1/BB3 Derivatives
MCU_EFM8LB1_BB3_DERIVS = { 0x01 : "EFM8BB31F64G",
                           0x02 : "EFM8BB31F64G",
                           0x03 : "EFM8BB31F64G",
                           0x04 : "EFM8BB31F64G",
                           0x05 : "EFM8BB31F32G",
                           0x06 : "EFM8BB31F32G",
                           0x07 : "EFM8BB31F32G",
                           0x08 : "EFM8BB31F32G",
                           0x09 : "EFM8BB31F16G",
                           0x0A : "EFM8BB31F16G",
                           0x0B : "EFM8BB31F16G",
                           0x0C : "EFM8BB31F16G",
                           0x11 : "EFM8BB31F64I",
                           0x12 : "EFM8BB31F64I",
                           0x13 : "EFM8BB31F64I",
                           0x14 : "EFM8BB31F64I",
                           0x15 : "EFM8BB31F32I",
                           0x16 : "EFM8BB31F32I",
                           0x17 : "EFM8BB31F32I",
                           0x18 : "EFM8BB31F32I",
                           0x19 : "EFM8BB31F16I",
                           0x1A : "EFM8BB31F16I",
                           0x1B : "EFM8BB31F16I",
                           0x1C : "EFM8BB31F16I",
                           0x21 : "EFM8BB31F64A",
                           0x22 : "EFM8BB31F64A",
                           0x23 : "EFM8BB31F64A",
                           0x24 : "EFM8BB31F64A",
                           0x25 : "EFM8BB31F32A",
                           0x26 : "EFM8BB31F32A",
                           0x27 : "EFM8BB31F32A",
                           0x28 : "EFM8BB31F32A",
                           0x29 : "EFM8BB31F16A",
                           0x2A : "EFM8BB31F16A",
                           0x2B : "EFM8BB31F16A",
                           0x2C : "EFM8BB31F16A",
                           0x41 : "EFM8LB12F64E",
                           0x42 : "EFM8LB12F64E",
                           0x43 : "EFM8LB12F64E",
                           0x44 : "EFM8LB12F64E",
                           0x45 : "EFM8LB12F32E",
                           0x46 : "EFM8LB12F32E",
                           0x47 : "EFM8LB12F32E",
                           0x48 : "EFM8LB12F32E",
                           0x49 : "EFM8LB11F32E",
                           0x4A : "EFM8LB11F32E",
                           0x4B : "EFM8LB11F32E",
                           0x4C : "EFM8LB11F32E",
                           0x4D : "EFM8LB11F16E",
                           0x4E : "EFM8LB11F16E",
                           0x4F : "EFM8LB11F16E",
                           0x50 : "EFM8LB11F16E",
                           0x51 : "EFM8LB10F16E",
                           0x52 : "EFM8LB10F16E",
                           0x53 : "EFM8LB10F16E",
                           0x54 : "EFM8LB10F16E",
                           
                           0x61 : "EFM8LB12F64E-S",
                           0x62 : "EFM8LB12F64E-S",
                           0x63 : "EFM8LB12F64E-S",
                           0x64 : "EFM8LB12F64E-S",
                           0x65 : "EFM8LB12F32E-S",
                           0x66 : "EFM8LB12F32E-S",
                           0x67 : "EFM8LB12F32E-S",
                           0x68 : "EFM8LB12F32E-S",
                           0x69 : "EFM8LB11F32E-S",
                           0x6A : "EFM8LB11F32E-S",
                           0x6B : "EFM8LB11F32E-S",
                           0x6C : "EFM8LB11F32E-S",
                           0x6D : "EFM8LB11F16E-S",
                           0x6E : "EFM8LB11F16E-S",
                           0x6F : "EFM8LB11F16E-S",
                           0x70 : "EFM8LB11F16E-S",
                           0x71 : "EFM8LB10F16E-S",
                           0x72 : "EFM8LB10F16E-S",
                           0x73 : "EFM8LB10F16E-S",
                           0x74 : "EFM8LB10F16E-S",
                         }
# EFM8 Derivatives Table
MCU_EFM8_DERIVS = { 0x16 : MCU_EFM8SB2_DERIVS,
                    0x25 : MCU_EFM8SB1_DERIVS,
                    0x28 : MCU_EFM8UB2_DERIVS,
                    0x30 : MCU_EFM8BB1_DERIVS,
                    0x32 : MCU_EFM8UB1_BB2_DERIVS,
                    0x34 : MCU_EFM8LB1_BB3_DERIVS,
                  }

# EFM8-Specific Constants
JLINK_EFM8_VIRTUAL_AREA_SIZE        = 0x1000000

# 64KB. First 32KB are fixed, the other 32KB are the current bank
JLINK_EFM8_START_ADDR_CODE          = 0x0000000

# 256 bytes
JLINK_EFM8_START_ADDR_IDATA         = JLINK_EFM8_START_ADDR_CODE + JLINK_EFM8_VIRTUAL_AREA_SIZE

# 256 bytes  00-7F is RAM, with register banks as usual. 80-FF is the sfr area 
# of the currently selected bank
# WARNING: Because of how the debugger (DSR) interface works, DDATA ranges 0x00 - 0x7f should be referenced as IDATA.
# See Jeff or Rich for details.
JLINK_EFM8_START_ADDR_DDATA         = JLINK_EFM8_START_ADDR_IDATA + JLINK_EFM8_VIRTUAL_AREA_SIZE
JLINK_EFM8_START_ADDR_XDATA         = JLINK_EFM8_START_ADDR_DDATA + JLINK_EFM8_VIRTUAL_AREA_SIZE

# Virtually 64 KB. Maps non-memory mapped DSR registers to virtual memory, 
# to allow easy access to them
JLINK_EFM8_START_ADDR_DSR           = JLINK_EFM8_START_ADDR_XDATA + JLINK_EFM8_VIRTUAL_AREA_SIZE

#
# Explicit access to different DDATA pages
#

# 256 bytes. Same as DDATA, only sfrs are page-0 sfrs (no matter what SFRPAGE 
# register currently selects)
JLINK_EFM8_START_ADDR_DDATA_PAGE0   = JLINK_EFM8_START_ADDR_DDATA + 0x00100

# 256 bytes. Same as DDATA, only sfrs are page-1 sfrs (no matter what SFRPAGE 
# register currently selects)
JLINK_EFM8_START_ADDR_DDATA_PAGE1   = JLINK_EFM8_START_ADDR_DDATA + 0x00200

# 256 bytes. Same as DDATA, only sfrs are page-2 sfrs (no matter what SFRPAGE 
# register currently selects)
JLINK_EFM8_START_ADDR_DDATA_PAGE2   = JLINK_EFM8_START_ADDR_DDATA + 0x00300

# [...] DDATA_PAGE2-xxx
#
# Explicit access to different flash areas
# Allows debugger to perform a continuous flash download via a single memory-write
#

# 32KB, Always visible at 0x30000. Also be visible at 0x38000 if PSBANK == 0x00
JLINK_EFM8_START_ADDR_CODE_BANK0    = JLINK_EFM8_START_ADDR_CODE + 0x10000

# 32KB, Also be visible at 0x38000 if PSBANK == 0x11
JLINK_EFM8_START_ADDR_CODE_BANK1    = JLINK_EFM8_START_ADDR_CODE + 0x18000

# // 32KB, Also visible at 0x38000 if PSBANK register == 0x22
JLINK_EFM8_START_ADDR_CODE_BANK2    = JLINK_EFM8_START_ADDR_CODE + 0x20000

# [...] CODE_BANK3-xxx

#
# Virtual offsets of non-memory mapped DSR registers, into DSR zone
#
JLINK_EFM8_OFF_REG_DSR_VERSION      = 0x00
JLINK_EFM8_OFF_REG_DSR_DERIVATIVE   = 0x01

# //
# // Flags for JLINKARM_BP_
# //
JLINKARM_BP_MODE0                   = (0 << 0)      # // Meaning depends on CPU type
JLINKARM_BP_MODE1                   = (1 << 0)      # // Meaning depends on CPU type
JLINKARM_BP_MODE2                   = (2 << 0)      # // Meaning depends on CPU type
JLINKARM_BP_MODE3                   = (3 << 0)      # // Meaning depends on CPU type
JLINKARM_BP_MODE_MASK               = (0x0000000F)

JLINKARM_BP_IMP_SW_RAM              = (1 << 4)
JLINKARM_BP_IMP_SW_FLASH            = (1 << 5)
JLINKARM_BP_IMP_SW                  = (0x000000F0)
JLINKARM_BP_IMP_HW                  = (0xFFFFFF00)
JLINKARM_BP_IMP_ANY                 = (JLINKARM_BP_IMP_HW | JLINKARM_BP_IMP_SW)
JLINKARM_BP_IMP_MASK                = (JLINKARM_BP_IMP_ANY)

JLINKARM_BP_HANDLE_ALL              = (0xFFFFFFFF)
JLINKARM_WP_HANDLE_ALL              = (0xFFFFFFFF)

JLINKARM_GO_FLAG_OVERSTEP_BP        = (1 << 0)    # // Overstep the current instruction if it is breakpointed

JLINKARM_GO_MAX_EMUL_INSTS_DEFAULT  = (-1)        # // Use the same settings as JLINKARM_Go()

# //
# // Do NEVER change the numeric value of the register description, as certain parts of the DLL rely on this
# //
JLINK_EFM8_REG = {
  # //
  # // R0-R7 of each bank
  # //
  'JLINK_EFM8_R0_B0'     :  0,     # // Index 0: R0, bank 0
  'JLINK_EFM8_R1_B0'     :  1,
  'JLINK_EFM8_R2_B0'     :  2,
  'JLINK_EFM8_R3_B0'     :  3,
  'JLINK_EFM8_R4_B0'     :  4,
  'JLINK_EFM8_R5_B0'     :  5,
  'JLINK_EFM8_R6_B0'     :  6,
  'JLINK_EFM8_R7_B0'     :  7,
  'JLINK_EFM8_R0_B1'     :  8,     # // Index 8: R0, bank 1
  'JLINK_EFM8_R1_B1'     :  9,
  'JLINK_EFM8_R2_B1'     : 10,
  'JLINK_EFM8_R3_B1'     : 11,
  'JLINK_EFM8_R4_B1'     : 12,
  'JLINK_EFM8_R5_B1'     : 13,
  'JLINK_EFM8_R6_B1'     : 14,
  'JLINK_EFM8_R7_B1'     : 15,
  'JLINK_EFM8_R0_B2'     : 16,     # // Index 16: R0, bank 2
  'JLINK_EFM8_R1_B2'     : 17,
  'JLINK_EFM8_R2_B2'     : 18,
  'JLINK_EFM8_R3_B2'     : 19,
  'JLINK_EFM8_R4_B2'     : 20,
  'JLINK_EFM8_R5_B2'     : 21,
  'JLINK_EFM8_R6_B2'     : 22,
  'JLINK_EFM8_R7_B2'     : 23,
  'JLINK_EFM8_R0_B3'     : 24,     # // Index 24: R0, bank 3
  'JLINK_EFM8_R1_B3'     : 25,
  'JLINK_EFM8_R2_B3'     : 26,
  'JLINK_EFM8_R3_B3'     : 27,
  'JLINK_EFM8_R4_B3'     : 28,
  'JLINK_EFM8_R5_B3'     : 29,
  'JLINK_EFM8_R6_B3'     : 30,
  'JLINK_EFM8_R7_B3'     : 31,
  # //
  # // Special registers like PC, stackpointer etc.
  # //
  'JLINK_EFM8_PC'        : 32,        # // Index 32: PC, 16-bit
  'JLINK_EFM8_A'         : 33,         # // Accumulator
  'JLINK_EFM8_B'         : 34,
  'JLINK_EFM8_DPTR'      : 35,      # // Data pointer register (16-bit)
  'JLINK_EFM8_SP'        : 36,
  'JLINK_EFM8_PSW'       : 37,
  # //
  # // Pseudo regs. Mapped to currenttly selected register bank
  # // Bank is selected via PSW
  # //
  'JLINK_EFM8_R0'        : 38,        # // Index 38: Current R0 (pseudo reg)
  'JLINK_EFM8_R1'        : 39,
  'JLINK_EFM8_R2'        : 40,
  'JLINK_EFM8_R3'        : 41,
  'JLINK_EFM8_R4'        : 42,
  'JLINK_EFM8_R5'        : 43,
  'JLINK_EFM8_R6'        : 44,
  'JLINK_EFM8_R7'        : 45,
  # //
  # // End of list
  # //
  'JLINK_EFM8_NUM_REGS'  : 46,
}

# Prefixes to use when generating EFM32 part numbers
EFM32_PART_PREFIX = { 16  : "EFR32MG1P",
                      17  : "EFR32MG1B",
                      18  : "EFR32MG1V",
                      19  : "EFR32BG1P",
                      20  : "EFR32BG1B",
                      21  : "EFR32BG1V",
                      25  : "EFR32FG1P",
                      26  : "EFR32FG1B",
                      27  : "EFR32FG1V",
                      28  : "EFR32MG12P",
                      29  : "EFR32MG12B",
                      30  : "EFR32MG12V",
                      31  : "EFR32BG12P",
                      32  : "EFR32BG12B",
                      37  : "EFR32FG12P",
                      38  : "EFR32FG12B",
                      39  : "EFR32FG12V",
                      40  : "EFR32MG13P",
                      41  : "EFR32MG13B",
                      42  : "EFR32MG13V",
                      43  : "EFR32BG13P",
                      44  : "EFR32BG13B",
                      45  : "EFR32BG13V",
                      49  : "EFR32FG13P",
                      50  : "EFR32FG13B",
                      51  : "EFR32FG13V",
                      52  : "EFR32MG14P",
                      53  : "EFR32MG14B",
                      54  : "EFR32MG14V",
                      55  : "EFR32BG14P",
                      56  : "EFR32BG14B",
                      57  : "EFR32BG14V",
                      61  : "EFR32FG14P",
                      62  : "EFR32FG14B",
                      63  : "EFR32FG14V",
                      71  : "EFM32G",
                      72  : "EFM32GG",
                      73  : "EFM32TG",
                      74  : "EFM32LG",
                      75  : "EFM32WG",
                      76  : "EFM32ZG",
                      77  : "EFM32HG",
                      81  : "EFM32PG1B",
                      83  : "EFM32JG1B",
                      85  : "EFM32PG12B",
                      87  : "EFM32JG12B",
                      89  : "EFM32PG13B",
                      91  : "EFM32JG13B",
                      100 : "EFM32GG11B",
                      103 : "EFM32TG11B",
                      120 : "EZR32LG",
                      121 : "EZR32WG",
                      122 : "EZR32HG",
                    }

JLINK_DLL_ERROR_CODES = {
    # (0xFFFFFF00) No connection to emulator / Connection to emulator lost
    -256 : "JLINK_ERR_EMU_NO_CONNECTION",
    # (0xFFFFFEFF) Emulator communication error
    # (host-interface module repORted error)
    -257 : "JLINK_ERR_EMU_COMM_ERROR",
    # (0xFFFFFEFE) DLL has not been opened but needs to be
    # (JLINKARM_Open() needs to be called first)
    -258 : "JLINK_ERR_DLL_NOT_OPEN",
    # (0xFFFFFEFD) Target system has no power (Measured VTref < 1V)
    -259 : "JLINK_ERR_VCC_FAILURE",
    # (0xFFFFFEFC) File handle / memory area handle needed for operation,
    # but given handle is not valid
    -260 : "JLINK_ERR_INVALID_HANDLE",
    # (0xFFFFFEFB) Could not find supported CPU
    -261 : "JLINK_ERR_NO_CPU_FOUND",
    # (0xFFFFFEFA) Emulator does not support the selected feature
    # (Usually returned by functions which need specific emulator capabilities)
    -262 : "JLINK_ERR_EMU_FEATURE_NOT_SUPPORTED",
    # (0xFFFFFEF9) Emulator does not have enough memory to perform
    # the requested operation
    -263 : "JLINK_ERR_EMU_NO_MEMORY",
    # (0xFFFFFEF8) Things such as "TCK is low but should be high"
    -264 : "JLINK_ERR_TIF_STATUS_ERROR",
    -265 : "JLINK_ERR_FLASH_PROG_COMPARE_FAILED",
    -266 : "JLINK_ERR_FLASH_PROG_PROGRAM_FAILED",
    -267 : "JLINK_ERR_FLASH_PROG_VERIFY_FAILED",
    -268 : "JLINK_ERR_OPEN_FILE_FAILED",
    -269 : "JLINK_ERR_UNKNOWN_FILE_FORMAT",
    -270 : "JLINK_ERR_WRITE_TARGET_MEMORY_FAILED",
}

JLINK_UNSECURE_DIALOG_CB_FUNC_TYPE = ct.WINFUNCTYPE(ct.c_int,     # Return
                                                    ct.c_char_p,  # sTitle
                                                    ct.c_char_p,  # sMsg
                                                    ct.c_uint32)  # Flags


class JLinkArmEmuConnectInfo_CStruct(ct.Structure):
    """ JLINKARM_EMU_CONNECT_INFO struct """
    _pack_ = 1
    _fields_ = [("SerialNumber", ct.c_uint32),
                ("Connection", ct.c_uint),
                ("USBAddr", ct.c_uint32),
                ("aIPAddr", ct.c_uint8 * 16),
                ("Time", ct.c_int),
                ("Time_us", ct.c_uint64),
                ("HWVersion", ct.c_uint32),
                ("abMACAddr", ct.c_uint8 * 6),
                ("acProduct", ct.c_char * 32),
                ("acNickName", ct.c_char * 32),
                ("acFWString", ct.c_char * 112),
                ("IsDHCPAssignedIP", ct.c_char),
                ("IsDHCPAssignedIPIsValid", ct.c_char),
                ("NumIPConnections", ct.c_char),
                ("NumIPConnectionsIsValid", ct.c_char),
                ("aPadding", ct.c_uint8 * 34)]


class JLinkJtagIdData_CStruct(ct.Structure):
    """ JLINKARM_EMU_CONNECT_INFO struct """
    _pack_ = 1
    _fields_ = [("NumDevices", ct.c_int),
                ("ScanLen", ct.c_uint16),
                ("aId", ct.c_uint32 * 3),
                ("aScanLen", ct.c_uint8 * 3),
                ("aIrRead", ct.c_uint8 * 3),
                ("aScanRead", ct.c_uint8 * 3)]


class JlinkArm_Speed_Info_CStruct(ct.Structure):
    """ JLINKARM_SPEED_INFO struct """
    _pack_ = 1
    _fields_ = [("SizeOfStruct", ct.c_uint32),
                ("BaseFreq", ct.c_uint32),
                ("MinDiv", ct.c_uint16),
                ("SupportAdaptive", ct.c_uint16)]
