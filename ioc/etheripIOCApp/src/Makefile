TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build an IOC support library
LIBRARY_IOC += etheripIOCSupport

etheripIOCSupport_SRCS += myUtil.c

INC += myUtil.h

etheripIOCSupport_LIBS += $(EPICS_BASE_IOC_LIBS)
#=============================
# Build the IOC application

PROD_IOC = etheripIOC

# etheripIOC.dbd will be created and installed
DBD += etheripIOC.dbd

# For PyDevice module
SYS_PROD_LIBS += $(shell python-config --ldflags | sed 's/-[^l][^ ]*//g' | sed 's/-l//g')

# etheripIOC.dbd will be made up from these files:
etheripIOC_DBD += base.dbd
etheripIOC_DBD += ether_ip.dbd
etheripIOC_DBD += calcSupport.dbd
#etheripIOC_DBD += caPutLog.dbd
etheripIOC_DBD += asSupport.dbd
etheripIOC_DBD += pydev.dbd

# Add all the support libraries needed by this IOC
etheripIOC_LIBS += ether_ip
etheripIOC_LIBS += calc
#etheripIOC_LIBS += caPutLog
etheripIOC_LIBS += autosave
etheripIOC_LIBS += pydev
etheripIOC_LIBS += seq

# To build SNL programs, SNCSEQ must be defined
# in the <top>/configure/RELEASE file
ifneq ($(SNCSEQ),)
    # Build sncSabia into etheripIOCSupport
    #sncSabia_SNCFLAGS += +r
    sncSabia_SNCFLAGS += +W
    sncSabia_SNCFLAGS += +c
    sncSabia_SNCFLAGS += +s
    sncSabia_SNCFLAGS += -a
    etheripIOC_DBD += sncSabia.dbd
    etheripIOCSupport_SRCS += sncSabiaProgram.st
    etheripIOCSupport_LIBS += seq pv
    etheripIOC_LIBS += seq pv


endif

# Link in the code from our support library
etheripIOC_LIBS += etheripIOCSupport

# | Option | Description |
# | ------ | ----------- |
# | +a | Asynchronous pvGet: the program continues without waiting for completion of the pvGet operation. |
# | -a | Synchronous pvGet: the program waits for completion. This is the default if an option is not specified. |
# | +c | Wait for process variables to connect before allowing the program to begin execution. This is the default. |
# | -c | Allow the program to begin execution before connections are established to all channel. |
# | +d | Turn on run-time debug messages. |
# | -d | Turn off run-time debug messages. This is the default. |
# | +e | Use the new event flag mode. This is the default. |
# | -e | Use the old event flag mode (clear flags after executing a when statement). |
# | +i | Generate registrar procedure that registers shell commands and programs with an IOC shell. This is the default. |
# | -i | Do not generate registrar procedure. |
# | +l | Add line markers to the generated code, so that C compiler messages refer to the SNL source file. This is the default. |
# | -l | Do not produce line markers. |
# | +m | Include main procedure (seqMain.c) for a stand-alone program. |
# | -m | Do not include seqMain.c. This is the default. |
# | +r | Make the generated code reentrant, thus allowing more than one instance of the program to run on an IOC. |
# | -r | Generated code is not reentrant. This is the default. |
# | +s | Safe Mode: variables are local to state set and must be communicated explicitly. Implies +r. |
# | -s | Traditional (non-safe) mode. This is the default for compatibility. |
# | +w | Display warning messages. This is the default. |
# | -w | Suppress warnings. |
# | -o | To change the name of the generated C file. Requires an argument. |
# | +W | Display extra warnings for undefined objects. |
# | -W | Suppress extra warnings. This is the default. |

etheripIOC_SNCFLAGS += +W
etheripIOC_SNCFLAGS += +c
etheripIOC_SNCFLAGS += +s
etheripIOC_SNCFLAGS += -a


# etheripIOC_registerRecordDeviceDriver.cpp derives from etheripIOC.dbd
etheripIOC_SRCS += etheripIOC_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
etheripIOC_SRCS_DEFAULT += etheripIOCMain.cpp
etheripIOC_SRCS_vxWorks += -nil-

# Finally link to the EPICS Base libraries
etheripIOC_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

