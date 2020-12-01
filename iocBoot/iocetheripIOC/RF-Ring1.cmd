#!../../bin/linux-x86_64/etheripIOC
< envPaths
< logEnv

# epicsEnvSet("EPICS_CAS_INTF_ADDR_LIST", "10.128.124.141")

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
drvEtherIP_define_PLC("plc1", "10.128.130.60", 0)

dbLoadRecords("database/RF-Ring1.db", "PLC=plc1")
dbLoadRecords("database/RF-Ring1-Calc.db", "PLC=plc1")
iocInit()

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
