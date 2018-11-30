#!/bin/bash

# Environment Variables export

export PATH=/opt/epics-R3.14.12.7/base/bin/linux-x86_64:$PATH
export EPICS_BASE=/opt/epics-R3.14.12.7/base
export EPICS_HOST_ARCH=linux-x86_64
export EPICAS_CAS_SERVER_PORT=5100

# Wait for 2 seconds

sleep 2s

procServ --chdir /root/etherip-ioc/iocBoot 20202 ./RF-Booster.cmd &
