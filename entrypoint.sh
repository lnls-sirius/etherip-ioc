#!/bin/sh
set -eu

if [ -z "$1" ]; then
    echo "##########################################################################"
    echo "# ${NAME} - Port ${IOC_PROCSERV_SOCK}"
    echo "##########################################################################"
    /usr/local/bin/procServ \
        --logfile - \
        --chdir "$(pwd)/iocBoot/iocetheripIOC/" \
        --foreground \
        --ignore ^D^C \
        --name "${NAME}-IOC" \
        unix:${IOC_PROCSERV_SOCK} ./${CMD}
else
    exec "$@"
fi
