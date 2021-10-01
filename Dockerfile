FROM  lnlscon/epics-r3.15.8:v1.2 AS base

RUN set -ex; \
    apt-get update &&\
    apt-get install -y --fix-missing --no-install-recommends \
        procps \
        socat \
        tzdata \
        vim \
        wget \
        && rm -rf /var/lib/apt/lists/*  && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Epics auto addr list
ENV EPICS_CA_AUTO_ADDR_LIST YES
ENV EPICS_IOC_CAPUTLOG_INET 0.0.0.0
ENV EPICS_IOC_CAPUTLOG_PORT 7012
ENV EPICS_IOC_LOG_INET 0.0.0.0
ENV EPICS_IOC_LOG_PORT 7011

ENV IOC_PROCSERV_SOCK /opt/etheripIOC/sockets/ioc.sock

# EtherIP
RUN cd ${EPICS_MODULES} &&\
    wget https://github.com/EPICSTools/ether_ip/archive/ether_ip-3-2.tar.gz &&\
    tar -zxvf ether_ip-3-2.tar.gz && rm -f ether_ip-3-2.tar.gz && cd ether_ip-ether_ip-3-2 &&\
    sed -i -e '1iEPICS_BASE='${EPICS_BASE} configure/RELEASE && make -j$(nproc)

ENV ETHER_IP ${EPICS_MODULES}/ether_ip-ether_ip-3-2

COPY ./ioc /opt/etheripIOC

WORKDIR /opt/etheripIOC

RUN cd /opt/etheripIOC/ && mkdir sockets && envsubst < configure/RELEASE.tmplt > configure/RELEASE &&\
    make -j$(nproc)

COPY entrypoint.sh /opt/etheripIOC/entrypoint.sh
ENTRYPOINT [ "/bin/bash", "/opt/etheripIOC/entrypoint.sh" ]

FROM base AS rf_bo
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME RF-BO-Intlk
ENV CMD RF-Booster.cmd
ENV DEVIP 10.128.172.150

FROM base AS rf_si
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME RF-SI-Intlk
ENV CMD RF-Ring1.cmd
ENV DEVIP 10.128.173.60

FROM base AS delta
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME DELTA
ENV CMD Delta.cmd
ENV DEVIP 1.1.1.1
