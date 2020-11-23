#!/bin/bash

echo "##########################################################################"
echo "# ProcServControl - unix:"${PCTRL_SOCK}
echo "#     In order to connect: \"socat - UNIX-CLIENT:${PCTRL_SOCK}"
echo "##########################################################################"
echo ""
/usr/local/bin/procServ \
    -L -\
    -c "$(pwd)/procCtrl/iocBoot/iocprocCtrl" \
    -f \
    -i ^D^C \
    -n "${NAME}-PCTRL-IOC" \
    'unix:'${PCTRL_SOCK} ./st.cmd &

sleep 4

echo ""
echo ""
echo "##########################################################################"
echo "# ${NAME} - Port ${IOC_PROCSERV_SOCK}"
echo "##########################################################################"
echo ""
/usr/local/bin/procServ \
    -L - \
    -c "$(pwd)/iocBoot/iocetheripIOC/" \
    -f \
    -i ^D^C \
    -n "${NAME}-IOC" \
    unix:${IOC_PROCSERV_SOCK} ./${CMD}
