#!../../bin/linux-x86_64/etheripIOC
< envPaths
< logEnv

cd "${TOP}"

# PYTHONPATH points to folders where Python modules are.
epicsEnvSet("PYTHONPATH","$(TOP)/etheripIOCApp/src/python")

# maximum conversion table length
epicsEnvSet("MAX_TABLE_LENGTH", 1001)

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
dbLoadRecords("database/Delta_Mod02.db", "PREFIX_MOD02=${PREFIX_MOD02}, PLC=plc1")
dbLoadRecords("database/Delta_Mod03.db", "PREFIX_MOD03=${PREFIX_MOD03}, PLC=plc1")
dbLoadRecords("database/Delta_Sabia.db", "P=${PREFIX_MOD01}, R=, MAX_TABLE_LENGTH=${MAX_TABLE_LENGTH}, XLVMM2K=${XLVMM2K}, XLHMM2K=${XLHMM2K}, XCRMM2K=${XCRMM2K}, XCLMM2K=${XCLMM2K}, YLVMM2K=${YLVMM2K}, YLHMM2K=${YLHMM2K}, YCRMM2K=${YCRMM2K}, YCLMM2K=${YCLMM2K}, UPDATESTS=${UPDATESTS}")

# PyDevice code init for http requests
pydev("from deltaUtil import UnitConverter")
pydev("tables = UnitConverter('${URL_LV}', '${XLVMM2K}', '${YLVMM2K}', '${URL_LH}', '${XLHMM2K}', '${YLHMM2K}', '${URL_CR}', '${XCRMM2K}', '${YCRMM2K}', '${URL_CL}', '${XCLMM2K}', '${YCLMM2K}', '${UPDATESTS}')")

iocInit()

## Start any sequence programs
seq sncSabia, "P_MOD01=$(PREFIX_MOD01), P_GLOBAL=$(PREFIX_GLOBAL)"

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
