#!/bin/bash

echo "##########################################################################"
echo "# ProcServControl - unix:"${PCTRL_SOCK}
echo "#     In order to connect: \"socat - UNIX-CLIENT:${PCTRL_SOCK}"
echo "##########################################################################"
echo ""
/usr/local/bin/procServ \
    --holdoff 2 \
    --logfile - \
    --chdir "$(pwd)/procCtrl/iocBoot/iocprocCtrl" \
    --foreground \
    --ignore ^D^C \
    --name "${NAME}-PCTRL-IOC" \
    'unix:'${PCTRL_SOCK} ./st.cmd &

sleep 4

echo ""
echo ""
echo "##########################################################################"
echo "# ${NAME} - Port ${IOC_PROCSERV_SOCK}"
echo "##########################################################################"
echo ""

set -e
set -x
while true; do
/usr/local/bin/procServ \
    --holdoff 2 \
    --logfile - \
    --chdir "$(pwd)/iocBoot/iocetheripIOC/" \
    --foreground \
    --ignore ^D^C \
    --name "${NAME}-IOC" \
    unix:${IOC_PROCSERV_SOCK} ./${CMD}
sleep 2
done;
