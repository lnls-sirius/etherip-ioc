# Author: Cláudio Ferreira Carneiro
# LNLS - Brazilian Synchrotron Light Source Laboratory

FROM  lnlscon/epics-r3.15.8:v1.2
LABEL maintainer="Claudio Carneiro <claudio.carneiro@lnls.br>"

# VIM
RUN apt-get -y update && apt-get -y install procps vim

# Epics auto addr list
ENV EPICS_CA_AUTO_ADDR_LIST YES

# Base procServ port
ENV EPICS_IOC_CAPUTLOG_INET 0.0.0.0
ENV EPICS_IOC_CAPUTLOG_PORT 7012

ENV EPICS_IOC_LOG_INET 0.0.0.0
ENV EPICS_IOC_LOG_PORT 7011

# EtherIP
RUN cd ${EPICS_MODULES} &&\
    wget https://github.com/EPICSTools/ether_ip/archive/ether_ip-3-2.tar.gz &&\
    tar -zxvf ether_ip-3-2.tar.gz && rm -f ether_ip-3-2.tar.gz && cd ether_ip-ether_ip-3-2 &&\
    sed -i -e '1iEPICS_BASE='${EPICS_BASE} configure/RELEASE && make

ENV ETHER_IP ${EPICS_MODULES}/ether_ip-ether_ip-3-2

RUN mkdir -p /opt/etheripIOC
WORKDIR /opt/etheripIOC

COPY ./etheripIOCApp    /opt/etheripIOC/etheripIOCApp
COPY ./Makefile         /opt/etheripIOC/Makefile
COPY ./configure        /opt/etheripIOC/configure
COPY ./iocBoot          /opt/etheripIOC/iocBoot
COPY ./database         /opt/etheripIOC/database

RUN envsubst < configure/RELEASE.tmplt > configure/RELEASE && make && make distclean

ENV PROCSERVPORT 27001

CMD make clean && make distclean && make && procServ --allow -f -L - --chdir /opt/etheripIOC/iocBoot/iocetheripIOC ${PROCSERVPORT} /opt/etheripIOC/iocBoot/iocetheripIOC/Sirius.cmd
