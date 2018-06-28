#! ../ether_ip/bin/linux-x86_64/eipIoc
# 3.14 example startup file for a Host - * - shell-script - * -
# Load dbd, register the drvEtherIP .. commands
dbLoadDatabase ("../../dbd/eipIoc.dbd")
eipIoc_registerRecordDeviceDriver (pdbbase)
epicsEnvSet ("EPICS_IOC_LOG_INET", "127.0.0.1")
epicsEnvSet ("EPICS_IOC_LOG_PORT", "6505")
#iocLogInit
# Initialize EtherIP driver, define PLCs
EIP_buffer_limit (450)
drvEtherIP_init ()
EIP_verbosity (7)
drvEtherIP_define_PLC ("NAME OF PLC", "IP OF PLC", "MODULE OF PLC")
dbLoadRecords ("../../db/YOUR DATABASE", "PLC = YOUR PLC NAME, IOC = YOUR PV")
iocInit ()
