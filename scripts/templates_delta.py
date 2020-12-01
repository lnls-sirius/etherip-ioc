#!/usr/bin/python3
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

iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("${plc}", "$(DEVIP)", ${module})

dbLoadRecords("database/${database}.db", "PLC=${plc}")
iocInit()

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
"""
)

ao_template = Template(
    """
record(ao, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(PREC, "${prec}")
    field(EGU,  "${egu}")
    field(DRVH, "${drvh}")
    field(DRVL, "${drvl}")
    field(HOPR, "${hopr}")
    field(LOPR, "${lopr}")
    field(HIHI, "${hihi}")
    field(HIGH, "${high}")
    field(LOW, "${low}")
    field(LOLO, "${lolo}")
    field(HHSV, "${hhsv}")
    field(HSV, "${hsv}")
    field(LSV, "${lsv}")
    field(LLSV, "${llsv}")
    field(HYST, "${hyst}")
}
"""
)

ai_template = Template(
    """
record(ai, "${name}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(PREC, "${prec}")
    field(EGU,  "${egu}")
    field(HOPR, "${hopr}")
    field(LOPR, "${lopr}")
    field(HIHI, "${hihi}")
    field(HIGH, "${high}")
    field(LOW, "${low}")
    field(LOLO, "${lolo}")
    field(HHSV, "${hhsv}")
    field(HSV, "${hsv}")
    field(LSV, "${lsv}")
    field(LLSV, "${llsv}")
    field(HYST, "${hyst}")
}
"""
)

bo_template = Template(
    """
record(bo, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
    field(ZSV, "${zsv}")
    field(OSV, "${osv}")
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
    field(ZSV, "${zsv}")
    field(OSV, "${osv}")
}
"""
)

lsi_template = Template(
    """
record(lsi, "${name}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(SIZV,  "${sizv}")
}
"""
)

lso_template = Template(
    """
record(lso, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(SIZV,  "${sizv}")
}
"""
)
