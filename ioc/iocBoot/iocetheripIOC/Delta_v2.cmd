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
drvEtherIP_define_PLC("plc1", "$(DEVIP)", 0)

dbLoadRecords("database/Delta_Global.db", "PREFIX_GLOBAL=${PREFIX_GLOBAL}, PLC=plc1")
dbLoadRecords("database/Delta_Mod01.db", "PREFIX_MOD01=${PREFIX_MOD01}, PLC=plc1")
#dbLoadRecords("database/Delta_Mod02.db", "PREFIX_MOD02=${PREFIX_MOD02}, PLC=plc1")
#dbLoadRecords("database/Delta_Mod02.db", "PREFIX_MOD03=${PREFIX_MOD03}, PLC=plc1")
dbLoadRecords("database/Delta_Sabia.db", "P=${PREFIX_MOD01}, R=")
iocInit()

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
