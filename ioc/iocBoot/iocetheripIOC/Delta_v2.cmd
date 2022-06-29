#!../../bin/linux-x86_64/etheripIOC
< envPaths
< logEnv

cd "${TOP}"

# PYTHONPATH points to folders where Python modules are.
epicsEnvSet("PYTHONPATH","$(TOP)/etheripIOCApp/src/python")

# maximum array size the IOC can send through CA
epicsEnvSet("EPICS_CA_MAX_ARRAY_BYTES", 100000)

# maximum conversion table length
epicsEnvSet("MAX_TABLE_LENGTH", 1001)

# maximum profile length
epicsEnvSet("PROFILE_BUFF_SIZE", 10000)

# conversion table urls
epicsEnvSet("LOC", "$(TABLE_URL_COMMON)")
epicsEnvSet("URL_LV", "${LOC}/$(FILE_LV)")
epicsEnvSet("URL_LH", "${LOC}/$(FILE_LH)")
epicsEnvSet("URL_CR", "${LOC}/$(FILE_CR)")
epicsEnvSet("URL_CL", "${LOC}/$(FILE_CL)")

# variables used by PyDevice to update PVs
epicsEnvSet("XLVMM2K", "xLVmm2k")
epicsEnvSet("XLHMM2K", "xLHmm2k")
epicsEnvSet("XCRMM2K", "xCRmm2k")
epicsEnvSet("XCLMM2K", "xCLmm2k")
epicsEnvSet("YLVMM2K", "yLVmm2k")
epicsEnvSet("YLHMM2K", "yLHmm2k")
epicsEnvSet("YCRMM2K", "yCRmm2k")
epicsEnvSet("YCLMM2K", "yCLmm2k")
epicsEnvSet("UPDATESTS", "updateSts")
epicsEnvSet("UPDATEFLG", "updateFlg")

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

set_pass0_restoreFile("Delta_Sabia.sav")
set_pass1_restoreFile("Delta_Sabia.sav")

iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("plc1", "$(DEVIP)", 0)

dbLoadRecords("database/Delta_Global.db", "PREFIX_GLOBAL=${PREFIX_GLOBAL}, PLC=plc1")
dbLoadRecords("database/Delta_Mod01.db", "PREFIX_MOD01=${PREFIX_MOD01}, PLC=plc1")
dbLoadRecords("database/Delta_Mod02.db", "PREFIX_MOD02=${PREFIX_MOD02}, PLC=plc1")
dbLoadRecords("database/Delta_Mod03.db", "PREFIX_MOD03=${PREFIX_MOD03}, PLC=plc1")
dbLoadRecords("database/Delta_Sabia.db", "P=${PREFIX_MOD01}, R=, P_AXIS=${PREFIX_MOD01}, P_GLOB=${PREFIX_GLOBAL}, MAX_TABLE_LENGTH=${MAX_TABLE_LENGTH}, XLVMM2K=${XLVMM2K}, XLHMM2K=${XLHMM2K}, XCRMM2K=${XCRMM2K}, XCLMM2K=${XCLMM2K}, YLVMM2K=${YLVMM2K}, YLHMM2K=${YLHMM2K}, YCRMM2K=${YCRMM2K}, YCLMM2K=${YCLMM2K}, UPDATESTS=${UPDATESTS}, UPDATEFLG=${UPDATEFLG}")

# PyDevice code init for http requests
pydev("from deltaUtil import UnitConverter")
pydev("tables = UnitConverter('${URL_LV}', '${XLVMM2K}', '${YLVMM2K}', '${URL_LH}', '${XLHMM2K}', '${YLHMM2K}', '${URL_CR}', '${XCRMM2K}', '${YCRMM2K}', '${URL_CL}', '${XCLMM2K}', '${YCLMM2K}', '${UPDATESTS}', '${UPDATEFLG}')")

iocInit()

## Start any sequence programs
seq sncSabia, "P_MOD01=$(PREFIX_MOD01), P_GLOBAL=$(PREFIX_GLOBAL)"

# Save record values every 5 seconds
create_monitor_set("Delta_Sabia.req", 5, "PREFIX=${PREFIX_MOD01}")

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
