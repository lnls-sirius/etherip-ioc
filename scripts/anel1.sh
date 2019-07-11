#!/bin/bash

# Generate Sirius RF Storage Ring 1 IOC
./ioc.py \
    ../etc/SR1 \
    --sheet 'SSAmp Tower 02,Interlock,Petra 7,LLRF,Transmission Line' \
    --plc-ip 10.128.124.151 \
    --plc-name plc1 \
    --plc-module 0 \
    --ioc-name RF-Ring1 \
    --epics-ca-server-port  5068\
    --epics-cas-intf-addr-list 10.128.124.204 \
    --arch linux-x86_64
