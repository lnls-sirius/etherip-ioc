FROM lnls/epics-dist:base-3.15-debian-9 AS base
#FROM  lnlscon/epics-r3.15.8:v1.2 AS base

RUN echo "deb http://archive.debian.org/debian stretch main contrib non-free" > /etc/apt/sources.list
RUN set -ex; \
    apt-get update &&\
    apt-get install -y --fix-missing --no-install-recommends \
        procps \
        socat \
        tzdata \
        vim \
        wget \
        python-dev \
        python3-dev \
        python3-urllib3 \
        gettext-base \
        && rm -rf /var/lib/apt/lists/*  && \
    dpkg-reconfigure --frontend noninteractive tzdata
#        python3-urllib3=1.24.1-1 \

# Epics auto addr list
ENV EPICS_CA_AUTO_ADDR_LIST YES
ENV EPICS_IOC_CAPUTLOG_INET 0.0.0.0
ENV EPICS_IOC_CAPUTLOG_PORT 7012
ENV EPICS_IOC_LOG_INET 0.0.0.0
ENV EPICS_IOC_LOG_PORT 7011

ENV IOC_PROCSERV_SOCK /opt/etheripIOC/sockets/ioc.sock

# PyDevice
RUN cd /opt &&\
    git clone https://github.com/klemenv/PyDevice.git &&\
    cd PyDevice &&\
    git checkout 4b6afde9c8c70c223217ff439e9aa9d2927042b1 &&\
    echo "EPICS_BASE=/opt/epics/base" > configure/RELEASE.local &&\
    sed -i -e 's|^PYTHON_CONFIG=.*$|PYTHON_CONFIG=python3-config|' configure/CONFIG_SITE &&\
    make
#    sed -i -e 's|^PYTHON_CONFIG=.*$|PYTHON_CONFIG=python3-config|' configure/CONFIG_SITE

ENV PYDEVICE /opt/PyDevice

# EtherIP
RUN cd /opt &&\
    wget https://github.com/EPICSTools/ether_ip/archive/ether_ip-3-2.tar.gz &&\
    tar -zxvf ether_ip-3-2.tar.gz && rm -f ether_ip-3-2.tar.gz && cd ether_ip-ether_ip-3-2 &&\
    sed -i -e '1iEPICS_BASE='/opt/epics/base configure/RELEASE && make -j$(nproc)

ENV ETHER_IP /opt/ether_ip-ether_ip-3-2

COPY ./ioc /opt/etheripIOC

WORKDIR /opt/etheripIOC

ENV EPICS_BASE="/opt/epics/base"

#RUN cd /opt/etheripIOC/ && mkdir sockets && envsubst < configure/RELEASE.tmplt > configure/RELEASE &&\
#    make -j$(nproc)
RUN cd /opt/etheripIOC/ && mkdir sockets &&\
    make -j$(nproc)

COPY entrypoint.sh /opt/etheripIOC/entrypoint.sh
ENTRYPOINT [ "/bin/bash", "/opt/etheripIOC/entrypoint.sh" ]

#FROM base AS rf_bo
#COPY ./ioc/database /opt/etheripIOC/database
#COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
#ENV NAME RF-BO-Intlk
#ENV CMD RF-Booster.cmd
#ENV DEVIP 10.128.130.150

#FROM base AS rf_si
#COPY ./ioc/database /opt/etheripIOC/database
#COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
#ENV NAME RF-SI-Intlk
#ENV CMD RF-Ring1.cmd
#ENV DEVIP 10.128.130.60

#FROM base AS delta
#COPY ./ioc/database /opt/etheripIOC/database
#COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
#ENV NAME DELTA
#ENV CMD Delta.cmd
#ENV DEVIP 1.1.1.1

FROM base AS delta_v2
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME DELTA-V2
ENV CMD Delta_v2.cmd
ENV DEVIP 1.1.1.1
