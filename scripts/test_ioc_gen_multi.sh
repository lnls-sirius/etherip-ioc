#!/usr/bin/env bash

usage() {
    echo "Usage:"
    echo "      $0 AUTO_GEN_SCRIPT WORKBOOK"
}

if [ $# -lt 2 ]
then 
    printf "Not enough arguments - %d\n" $#
    usage
    exit 0
fi

AUTO_GEN_SCRIPT=$1
WORKBOOK=$2

DB_IOC_1="Delta1"
CMD_IOC_1="delta1"
PREFIX_IOC_1="SI-Glob:Test-Undulator-1:"
IP_IOC_1="1.1.1.1"
MODULE_IOC_1=0

DB_IOC_2="Delta2"
CMD_IOC_2="delta2"
PREFIX_IOC_2="SI-Glob:Test-Undulator-2:"
IP_IOC_2="1.1.1.2"
MODULE_IOC_2=0

DB_IOC_3="Delta3"
CMD_IOC_3="delta3"
PREFIX_IOC_3="SI-Glob:Test-Undulator-3:"
IP_IOC_3="1.1.1.3"
MODULE_IOC_3=0

python3 $AUTO_GEN_SCRIPT \
--multi-db $PREFIX_IOC_1 \
           $DB_IOC_1 \
--multi-cmd $CMD_IOC_1 \
            $IP_IOC_1 \
            $MODULE_IOC_1 \
            $DB_IOC_1 \
--multi-db $PREFIX_IOC_2 \
           $DB_IOC_2 \
--multi-cmd $CMD_IOC_2 \
            $IP_IOC_2 \
            $MODULE_IOC_2 \
            $DB_IOC_2 \
--multi-db $PREFIX_IOC_3 \
           $DB_IOC_3 \
--multi-cmd $CMD_IOC_3 \
            $IP_IOC_3 \
            $MODULE_IOC_3 \
            $DB_IOC_3 \
--plc-ip "192.168.0.14" \
--plc-name MyPLC \
--plc-module 0 \
--col-desc Description \
--col-dtype "Data Type" \
--col-egu EGU \
--col-inout "In/Out" \
--bi "Digital Input" "Digital Output" \
--bo "Digital Control" \
--ai "Analog Input" \
--ao "Analog Output" \
--lsi "String Input" \
--lso "String Output" \
--col-prec "Prec" \
--col-pv NAME \
--col-scan Scan \
--col-tag TAG \
--ioc-name TestDeltaIOC \
--sheet Sheet1 \
--epics-ca-server-port 5068 \
--epics-cas-intf-addr-list 10.128.124.141 \
--arch linux-x86_64 \
$WORKBOOK
