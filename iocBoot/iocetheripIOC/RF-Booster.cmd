#!/opt/epics-R3.15.6/modules/ether_ip-ether_ip-3-1/bin/linux-x86_64/eipIoc

# Load dbd, register the drvEtherIP .. commands
dbLoadDatabase("/opt/epics-R3.15.6/modules/ether_ip-ether_ip-3-1/dbd/eipIoc.dbd")
eipIoc_registerRecordDeviceDriver(pdbbase)

# epicsEnvSet("EPICS_IOC_LOG_INET", "127.0.0.1")
# epicsEnvSet("EPICS_IOC_LOG_PORT", "6505")

#epicsEnvSet("EPICS_CA_SERVER_PORT", "5064")
epicsEnvSet("EPICS_CAS_INTF_ADDR_LIST", "10.128.124.140")
iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("plc1", "10.128.130.150", 0)

dbLoadRecords("../database/RF-Booster.db", "PLC=plc1")
dbLoadRecords("../database/RF-Booster-Calc.db", "PLC=plc1")
iocInit()

