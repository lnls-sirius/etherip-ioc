#!../../bin/linux-x86_64/etheripIOC
< envPaths
< logEnv

cd "${TOP}"

# Load dbd, register the drvEtherIP .. commands
dbLoadDatabase("dbd/etheripIOC.dbd")
etheripIOC_registerRecordDeviceDriver(pdbbase)

asSetFilename("${TOP}/db/Security.as")

# Autosave settings
set_requestfile_path("$(TOP)", "autosave")
set_savefile_path("$(TOP)/autosave/save")

save_restoreSet_DatedBackupFiles(1)
save_restoreSet_NumSeqFiles(2)
save_restoreSet_SeqPeriodInSeconds(600)

iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("plc3", "$(DEVIP)", 0)

dbLoadRecords("database/sirius-amb-temp-ioc-3.db", "PLC=plc3, P=$(NAME)")
dbLoadRecords("database/sirius-amb-temp-ioc-3-calc.db", "PLC=plc3")
iocInit()

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
