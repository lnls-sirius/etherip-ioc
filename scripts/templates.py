#!/usr/bin/python3
from string import Template

cmd_template = Template(
"""#!/opt/epics-R3.14.12.7/modules/ether_ip-ether_ip-2-27/bin/${arch}/eipIoc
# 3.14 example startup file for a Host - * - shell-script - * -
# Load dbd, register the drvEtherIP .. commands
dbLoadDatabase("../ether_ip/dbd/eipIoc.dbd") 
eipIoc_registerRecordDeviceDriver(pdbbase)

epicsEnvSet("EPICS_IOC_LOG_INET", "127.0.0.1")
epicsEnvSet("EPICS_IOC_LOG_PORT", "6505")
epicsEnvSet("EPICS_CA_SERVER_PORT", "${epics_ca_server_port}")
iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("${plc}", "${ip}", ${module})

dbLoadRecords("../database/${database}.db", "PLC=${plc}")
iocInit()

""")

ai_template = Template("""
record(ai, "${pv}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan}")
    field(PREC, "${prec}")
    field(EGU, "${egu}")
}
""")

bo_template = Template("""
record(bo, "${pv}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan}")
    field(ONAM, "${highname}")
    field(ZNAM, "${lowname}")
}
""")

bi_template = Template("""
record(bi, "${pv}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan}")
    field(ONAM, "${highname}")
    field(ZNAM, "${lowname}")
}
""")
