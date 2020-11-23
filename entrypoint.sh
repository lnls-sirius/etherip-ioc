#!/bin/bash

echo "##########################################################################"
echo "# ProcServControl - unix:"${PCTRL_SOCK}
echo "#     In order to connect: \"socat - UNIX-CLIENT:${PCTRL_SOCK}"
echo "##########################################################################"
echo ""
/usr/local/bin/procServ \
    -L -\
    -f \
    -c "$(pwd)/procCtrl/iocBoot/iocprocCtrl" \
    -n "${NAME}-PCTRL-IOC" \
    -i ^D^C \
    'unix:'${PCTRL_SOCK} ./st.cmd &

sleep 4

echo ""
echo ""
echo "##########################################################################"
echo "# ${NAME} - Port ${IOC_PROCSERV_ADDR}"
echo "##########################################################################"
echo ""
/usr/local/bin/procServ \
    -L - \
    -f \
    -c "$(pwd)/iocBoot/iocetheripIOC/" \
    -n "${NAME}-IOC" \
    -i ^D^C \
    unix:${IOC_PROCSERV_SOCK} ./${CMD}
