#!/bin/bash

# Generate Sirius RF Booster IOC
./ioc.py \
    --epics-ca-server-port  5064\
    --epics-cas-intf-addr-list 10.128.124.140 \
    ../etc/BOIlk \
    --sheet 'SSAmp Tower,Interlock,Petra 5,LLRF,Transmission Line' \
    --plc-ip 10.128.130.150 \
    --plc-name plc1 \
    --plc-module 0 \
    --ioc-name RF-Booster \
    --arch linux-x86_64
sed -i -e  's/\n")/")/g' ../database/RF-Booster.db
