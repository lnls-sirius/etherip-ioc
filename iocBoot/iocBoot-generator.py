#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

arquivo = str(sys.argv[1])
plc = str(sys.argv[2])
ip = str(sys.argv[3])
module = str(sys.argv[4])
database = str(sys.argv[5])
nameplc = str(sys.argv[6])
prefx = str(sys.argv[7])


try:
    file = open(arquivo, 'a')
    file = open(arquivo, 'w')

    file.writelines('#! ../../bin/linux-arm/eipIoc\n' 
                    '# 3.14 example startup file for a Host - * - shell-script - * -\n'  
                    '# Load dbd, register the drvEtherIP .. commands\n' 
                    'dbLoadDatabase ("../../../ether_ip-ether_ip-2-27/dbd/eipIoc.dbd)\n' 
                    'eipIoc_registerRecordDeviceDriver (pdbbase)\n' 
                    'epicsEnvSet ("EPICS_IOC_LOG_INET", "127.0.0.1")\n' 
                    'epicsEnvSet ("EPICS_IOC_LOG_PORT", "6505")\n' 
                    '#iocLogInit\n' 
                    '# Initialize EtherIP driver, define PLCs\n' 
                    'EIP_buffer_limit (450)\n' 
                    'drvEtherIP_init ()\n' 
                    'EIP_verbosity (7)\n' 
                    'drvEtherIP_define_PLC ("{}", "{}", {})'.format(plc, ip, module) + '\n' 
                    'dbLoadRecords ("../database/{}", "{},{}")'.format(database, nameplc, prefx) + '\n' 
                    'iocInit () \n'
                    )

    file.close()

except Exception as e:
    print(e)
    pass
