#!/bin/bash

# Generate Sirius RF Booster IOC
./ioc.py \
    ../etc/Interlock_RF_EPICS_V2.xlsx \
    --plc-ip 10.0.28.135 \
    --plc-name plc1 \
    --plc-module 0 \
    --ioc-name RF-Booster \
    --sheet Booster \
    --epics-ca-server-port 5100 \
    --epics-cas-intf-addr-list 10.0.6.57 \
    --arch linux-x86_64