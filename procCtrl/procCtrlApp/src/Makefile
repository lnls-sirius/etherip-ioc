TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = procCtrl
# procCtrl.dbd will be created and installed
DBD += procCtrl.dbd

# procCtrl.dbd will be made up from these files:
procCtrl_DBD += base.dbd
procCtrl_DBD += asyn.dbd
procCtrl_DBD += drvAsynIPPort.dbd
procCtrl_DBD += busySupport.dbd
procCtrl_DBD += procServControl.dbd
procCtrl_DBD += caPutLog.dbd

# Add all the support libraries needed by this IOC
procCtrl_LIBS += procServControl
procCtrl_LIBS += busy
procCtrl_LIBS += seq
procCtrl_LIBS += pv
procCtrl_LIBS += asyn
procCtrl_LIBS += caPutLog

# procCtrl_registerRecordDeviceDriver.cpp derives from procCtrl.dbd
procCtrl_SRCS += procCtrl_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
procCtrl_SRCS_DEFAULT += procCtrlMain.cpp
procCtrl_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#procCtrl_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
procCtrl_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

