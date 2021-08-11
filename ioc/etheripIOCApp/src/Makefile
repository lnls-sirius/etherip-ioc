TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = etheripIOC

# etheripIOC.dbd will be created and installed
DBD += etheripIOC.dbd

# etheripIOC.dbd will be made up from these files:
etheripIOC_DBD += base.dbd
etheripIOC_DBD += ether_ip.dbd
etheripIOC_DBD += calcSupport.dbd
etheripIOC_DBD += caPutLog.dbd
etheripIOC_DBD += asSupport.dbd


# Add all the support libraries needed by this IOC
etheripIOC_LIBS += ether_ip
etheripIOC_LIBS += calc
etheripIOC_LIBS += caPutLog
etheripIOC_LIBS += autosave

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

