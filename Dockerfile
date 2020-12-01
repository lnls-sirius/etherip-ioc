# Author: Cláudio Ferreira Carneiro
# LNLS - Brazilian Synchrotron Light Source Laboratory

FROM  lnlscon/epics-r3.15.8:v1.2 AS base
LABEL maintainer="Claudio Carneiro <claudio.carneiro@lnls.br>"

# VIM
RUN apt-get -y update && apt-get -y install procps socat vim

# Epics auto addr list
ENV EPICS_CA_AUTO_ADDR_LIST YES

# Base procServ port
ENV EPICS_IOC_CAPUTLOG_INET 0.0.0.0
ENV EPICS_IOC_CAPUTLOG_PORT 7012
ENV EPICS_IOC_LOG_INET 0.0.0.0
ENV EPICS_IOC_LOG_PORT 7011

ENV IOC_PROCSERV_SOCK /opt/etheripIOC/sockets/ioc.sock
ENV PCTRL_SOCK /opt/etheripIOC/procCtrl/sockets/pCtrl.sock

# EtherIP
RUN cd ${EPICS_MODULES} &&\
    wget https://github.com/EPICSTools/ether_ip/archive/ether_ip-3-2.tar.gz &&\
    tar -zxvf ether_ip-3-2.tar.gz && rm -f ether_ip-3-2.tar.gz && cd ether_ip-ether_ip-3-2 &&\
    sed -i -e '1iEPICS_BASE='${EPICS_BASE} configure/RELEASE && make

ENV ETHER_IP ${EPICS_MODULES}/ether_ip-ether_ip-3-2

RUN mkdir -p /opt/etheripIOC/autosave/save

WORKDIR /opt/etheripIOC

COPY . /opt/etheripIOC

RUN cd /opt/etheripIOC/procCtrl && envsubst < configure/RELEASE.tmplt > configure/RELEASE &&\
    cat configure/RELEASE && make distclean && make clean && make -j$(nproc) && mkdir sockets &&\
    \
    cd /opt/etheripIOC/ && mkdir sockets && envsubst < configure/RELEASE.tmplt > configure/RELEASE &&\
    make -j$(nproc)

CMD [ "/bin/bash", "/opt/etheripIOC/entrypoint.sh" ]

FROM base AS sirius
ENV NAME SIRIUS-INTLK
ENV CMD Sirius.cmd
ENV IOC_PROCSERV_PREFIX PCtrl:${NAME}
ENV DEVIP localhost

FROM base AS rf_bo
ENV NAME RF-BO-INTLK
ENV CMD RF-Booster.cmd
ENV DEVIP 10.128.130.150
ENV IOC_PROCSERV_PREFIX PCtrl:${NAME}

FROM base AS rf_si
ENV NAME RF-SI-INTLK
ENV CMD RF-Ring1.cmd
ENV DEVIP 10.128.130.60
ENV IOC_PROCSERV_PREFIX PCtrl:${NAME}
