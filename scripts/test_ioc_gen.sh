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

python3 $AUTO_GEN_SCRIPT \
--plc-ip "1.1.1.1" \
--plc-name MyPLC \
--plc-module 0 \
--col-dtype "Data Type" \
--bi "Digital Input" \
     "Digital Output" \
--bo "Digital Control" \
--ai "Analog Input" \
--ao "Analog Output" \
--col-desc Description \
--col-inout "In/Out" \
--col-egu EGU \
--col-prec "Prec" \
--col-pv NAME \
--col-scan Scan \
--col-tag TAG \
--ioc-name TestDeltaIOC \
--sheet Sheet1 \
--epics-ca-server-port 5068 \
--epics-cas-intf-addr-list 10.128.124.141 \
--arch linux-x86_64 \
--col-drvh DRVH \
--col-drvl DRVL_TEST \
--col-hopr HOPR_TEST \
--col-lopr LOPR_TEST \
--col-hihi HIHI_TEST \
--col-high HIGH_TEST \
--col-low LOW_TEST \
--col-lolo LOLO_TEST \
--col-hhsv HHSV_TEST \
--col-hsv HSV_TEST \
--col-lsv LSV_TEST \
--col-llsv LLSV_TEST \
--col-hyst HYST_TEST \
$WORKBOOK
