#!/bin/bash
./ioc.py \
    ../etc/Interlock_RF_EPICS_V2.xlsx \
    --plc-ip 10.0.28.135 \
    --plc-name plc1 \
    --plc-module 0 \
    --ioc-name RF-Booster \
    --sheet Booster \
    --arch linux-x86_64