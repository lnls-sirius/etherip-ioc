#!/usr/bin/python3
from string import Template

cmd_template = Template(
    """#!../../bin/linux-x86_64/etheripIOC
< envPaths
< logEnv

cd "${TOP}"

# Load dbd, register the drvEtherIP .. commands
dbLoadDatabase("dbd/etheripIOC.dbd")
eipIoc_registerRecordDeviceDriver(pdbbase)

asSetFilename("${TOP}/db/Security.as")

#epicsEnvSet("EPICS_CA_SERVER_PORT", "${epics_ca_server_port}")
epicsEnvSet("EPICS_CAS_INTF_ADDR_LIST", "${epics_cas_intf_addr_list}")

iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("${plc}", "${ip}", ${module})

dbLoadRecords("../database/${database}", "PLC=${plc}")
iocInit()

"""
)

ao_template = Template(
    """
record(ao, "${pv}"){
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
record(ai, "${pv}"){
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
record(bo, "${pv}"){
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
record(bi, "${pv}"){
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
