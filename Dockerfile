# Author: Cláudio Ferreira Carneiro
# LNLS - Brazilian Synchrotron Light Source Laboratory

FROM  lnlscon/epics-r3.15.8:v1.0
LABEL maintainer="Claudio Carneiro <claudio.carneiro@lnls.br>"

# Python3
RUN pip3 install pandas==0.23.4 xlrd==1.2.0

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
    tar -zxvf ether_ip-3-2.tar.gz && rm -f ether_ip-3-2.tar.gz && cd ether_ip-3-2 &&\
    sed -i -e '1iEPICS_BASE='${EPICS_BASE} configure/RELEASE && make
ENV ETHER_IP ${EPICS_MODULES}/ether_ip-3-2

RUN mkdir /opt/etheriopIOC
WORKDIR /opt/etheriopIOC

ADD etheriopIOC        etheriopIOC 
ADD Makefile           Makefile
ADD configure          configure
ADD iocBoot            iocBoot

CMD sleep infinity
