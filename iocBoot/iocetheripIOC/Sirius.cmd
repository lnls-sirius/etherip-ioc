#!../../bin/linux-x86_64/etheripIOC
< envPaths

cd "${TOP}"

# Load dbd, register the drvEtherIP .. commands
dbLoadDatabase("dbd/etheripIOC.dbd")
etheripIOC_registerRecordDeviceDriver(pdbbase)

asSetFilename("${TOP}/db/Security.as")

epicsEnvSet("EPICS_IOC_LOG_INET", "0.0.0.0")
epicsEnvSet("EPICS_IOC_LOG_PORT", "7011")

# epicsEnvSet("EPICS_CA_SERVER_PORT", "5064")
# epicsEnvSet("EPICS_CAS_INTF_ADDR_LIST", "10.128.124.140")

iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("plc1", "10.0.38.199", 1)

dbLoadRecords("database/Sirius.db", "PLC=plc1")
iocInit()

caPutLogInit "0.0.0.0:5065" 2
