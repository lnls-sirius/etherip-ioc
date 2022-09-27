#!/bin/sh
set -eu

echo "##########################################################################"
echo "# ${NAME} - Port ${IOC_PROCSERV_SOCK}"
echo "##########################################################################"
chmod +x /opt/etheripIOC/iocBoot/iocetheripIOC/*
/usr/local/bin/procServ \
    --logfile - \
    --chdir "$(pwd)/iocBoot/iocetheripIOC/" \
    --foreground \
    --ignore ^D^C \
    --name "${NAME}-IOC" \
    unix:${IOC_PROCSERV_SOCK} ./${CMD}
