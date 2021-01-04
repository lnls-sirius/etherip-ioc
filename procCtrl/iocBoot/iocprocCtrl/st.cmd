#!../../bin/linux-x86_64/procCtrl

< envPaths

cd "${TOP}"

epicsEnvSet("EPICS_IOC_LOG_INET", "$(EPICS_IOC_LOG_INET)")
epicsEnvSet("EPICS_IOC_LOG_PORT", "$(EPICS_IOC_LOG_PORT)")

dbLoadDatabase "dbd/procCtrl.dbd"
procCtrl_registerRecordDeviceDriver pdbbase

asSetFilename("$(TOP)/db/Security.as")

dbLoadRecords("$(TOP)/db/procServControl.template", "P=$(IOC_PROCSERV_PREFIX),PORT=port1,SHOWOUT=1, MANUALSTART=,name=$(IOC_PROCSERV_PREFIX)")
drvAsynIPPortConfigure("port1", "unix://$(IOC_PROCSERV_SOCK)")


cd "${TOP}/iocBoot/${IOC}"
iocInit
iocLogInit
caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2

seq(procServControl,"P=$(IOC_PROCSERV_PREFIX)")
date
dbl

#                       ProcServ Control Init Complete
###########################################################################
