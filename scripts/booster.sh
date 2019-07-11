#!/bin/bash

# Generate Sirius RF Booster IOC
./ioc.py \
    ../etc/BOIlk \
    --sheet 'SSAmp Tower,Interlock,Petra 5,LLRF,Transmission Line' \
    --plc-ip 10.128.124.150 \
    --plc-name plc1 \
    --plc-module 0 \
    --ioc-name RF-Booster \
    --epics-ca-server-port  5064\
    --epics-cas-intf-addr-list 10.128.124.204 \
    --arch linux-x86_64
