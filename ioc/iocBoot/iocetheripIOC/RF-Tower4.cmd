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

set_pass0_restoreFile("RF-Tower4.sav")
set_pass1_restoreFile("RF-Tower4.sav")

iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("plc1", "$(DEVIP)", 0)

dbLoadRecords("database/RF-Tower4.db", "PLC=plc1")
iocInit()

# Save things every 5 seconds
create_monitor_set("autosave/RF-Tower4.req", 5, "")

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
