from string import Template

cmd_template = Template(
    """#!../../bin/linux-x86_64/etheripIOC
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

dbLoadRecords("database/${database}.db", "PLC=${plc}, P=$(NAME)")
iocInit()

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
"""
)

ai_template = Template(
    """
record(ai, "${name}"){
    field(DTYP, "EtherIP")
    field(INP,  "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(PREC, "${prec}")
    field(EGU,  "${egu}")
}
"""
)

ao_template = Template(
    """
record(ao, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT,  "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(PREC, "${prec}")
    field(EGU,  "${egu}")
}
"""
)

bo_template = Template(
    """
record(bo, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag} S .1")
    field(DESC, "${desc}")
    field(SCAN, "Passive")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
}
"""
)

bi_template = Template(
    """
record(bi, "${name}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
}
"""
)
