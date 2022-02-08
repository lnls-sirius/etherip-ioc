ARG DOCKER_IMAGE_BASE
FROM ${DOCKER_IMAGE_BASE} as epics-deps

# set correct timezone
ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN set -ex; \
    apt update -y && \
    apt install -y --fix-missing --no-install-recommends \
        build-essential \
        ca-certificates \
        gettext-base \
        git \
        libpcre3-dev \
        libreadline-dev \
        procps \
        python3-dev \
        python3-urllib3 \
        re2c \
        socat \
        tzdata \
        vim \
        wget \
      && rm -rf /var/lib/apt/lists/*  && \
    dpkg-reconfigure --frontend noninteractive tzdata

# --- procServ ---
RUN set -exu; \
    wget https://github.com/ralphlange/procServ/releases/download/v2.8.0/procServ-2.8.0.tar.gz; \
    tar -zxvf procServ-2.8.0.tar.gz; \
    cd procServ-2.8.0; \
    ./configure --enable-access-from-anywhere; \
    make install; \
    cd ..; \
    rm -rf procServ-2.8.0.tar.gz procServ-2.8.0

ENV PATH /opt/procServ:${PATH}

FROM epics-deps as epics-base
# --- EPICS BASE ---

ENV EPICS_VERSION R3.15.8
ENV EPICS_HOST_ARCH linux-x86_64
ENV EPICS_BASE /opt/epics-${EPICS_VERSION}/base
ENV EPICS_MODULES /opt/epics-${EPICS_VERSION}/modules
ENV PATH ${EPICS_BASE}/bin/${EPICS_HOST_ARCH}:${PATH}

ENV EPICS_CA_AUTO_ADDR_LIST YES


ARG EPICS_BASE_URL=https://github.com/epics-base/epics-base/archive/${EPICS_VERSION}.tar.gz
LABEL br.cnpem.epics-base=${EPICS_BASE_URL}
RUN set -x; \
    set -e; \
    mkdir -p ${EPICS_MODULES}; \
    wget -O /opt/epics-R3.15.8/base-3.15.8.tar.gz ${EPICS_BASE_URL}; \
    cd /opt/epics-${EPICS_VERSION}; \
    tar -zxf base-3.15.8.tar.gz; \
    rm base-3.15.8.tar.gz; \
    mv epics-base-R3.15.8 base; \
    cd base; \
    make -j$(nproc)

WORKDIR /opt/epics-${EPICS_VERSION}


FROM epics-base as epics-modules
# --- EPICS MODULES ---

# sscan-R2-11-3
ARG SSCAN_VERSION=R2-11-4
ARG SSCAN_URL=https://github.com/epics-modules/sscan/archive/${SSCAN_VERSION}.tar.gz
LABEL br.cnpem.sscan=${SSCAN_URL}
ENV SSCAN ${EPICS_MODULES}/sscan-${SSCAN_VERSION}
RUN set -x; \
    set -e; \
    cd ${EPICS_MODULES}; \
    wget -O ${SSCAN}.tar.gz ${SSCAN_URL}; \
    tar -xvzf ${SSCAN}.tar.gz; \
    rm ${SSCAN}.tar.gz; \
    cd ${SSCAN}; \
    sed -i \
        -e '7s/^/#/' \
        -e '10s/^/#/' \
        -e '14cEPICS_BASE='${EPICS_BASE}  \
        configure/RELEASE; \
    make -j$(nproc)

# synApps Calc Module
ARG CALC_VERSION=R3-7-4
ARG CALC_URL=https://github.com/epics-modules/calc/archive/${CALC_VERSION}.tar.gz
LABEL br.cnpem.calc=${CALC_URL}
ENV CALC ${EPICS_MODULES}/synApps/calc-${CALC_VERSION}
RUN set -exu; \
    cd ${EPICS_MODULES}; \
    mkdir synApps; \
    cd synApps; \
    wget -O ${CALC}.tar.gz ${CALC_URL}; \
    tar -xvzf ${CALC}.tar.gz; \
    rm ${CALC}.tar.gz; \
    cd ${CALC}; \
    sed -i  \
        -e '5s/^/#/' \
        -e '7,8s/^/#/' \
        -e '13cSSCAN='${SSCAN} \
        -e '20cEPICS_BASE='${EPICS_BASE}  \
        configure/RELEASE; \
    make -j$(nproc)

# asynDriver
ARG ASYN_VERSION=R4-41
ARG ASYN_URL=https://github.com/epics-modules/asyn/archive/${ASYN_VERSION}.tar.gz
ENV ASYN ${EPICS_MODULES}/asyn-${ASYN_VERSION}
LABEL br.cnpem.asyn=${ASYN_URL}
RUN set -x; \
    set -e; \
    cd ${EPICS_MODULES}; \
    wget ${ASYN_URL} -O ${ASYN}.tar.gz; \
    tar -xvzf ${ASYN}.tar.gz; \
    rm -f ${ASYN}.tar.gz; \
    cd ${ASYN}; \
    sed -i  \
        -e '3,4s/^/#/' \
        -e '7s/^/#/' \
        -e '10s/^/#/' \
        -e '19cEPICS_BASE='${EPICS_BASE}  \
        -e '15iCALC='${CALC} \
        -e '16iSSCAN='${SSCAN} \
        ${ASYN}/configure/RELEASE; \
    make -j$(nproc)

# Autosave
ARG AUTOSAVE_VERSION=R5-10-2
ARG AUTOSAVE_URL=https://github.com/epics-modules/autosave/archive/${AUTOSAVE_VERSION}.tar.gz
ENV AUTOSAVE ${EPICS_MODULES}/asyn-${AUTOSAVE_VERSION}
LABEL br.cnpem.autosave=${AUTOSAVE_URL}
ENV AUTOSAVE ${EPICS_MODULES}/autosave-${AUTOSAVE_VERSION}
RUN set -x; \
    set -e; \
    cd ${EPICS_MODULES}; \
    wget -O ${AUTOSAVE}.tar.gz ${AUTOSAVE_URL}; \
    tar -zxvf ${AUTOSAVE}.tar.gz; \
    rm -f ${AUTOSAVE}.tar.gz; \
    cd ${AUTOSAVE}; \
    sed -i  \
        -e '7s/^/#/' \
        -e '10cEPICS_BASE='${EPICS_BASE} \
        configure/RELEASE; \
    make -j$(nproc)

# Caput Log
ARG CAPUTLOG_VERSION=R3.7
ARG CAPUTLOG_URL=https://github.com/epics-modules/caPutLog/archive/${CAPUTLOG_VERSION}.tar.gz
ENV CAPUTLOG ${EPICS_MODULES}/asyn-${CAPUTLOG_VERSION}
LABEL br.cnpem.caputlog=${CAPUTLOG_URL}
ENV CAPUTLOG /opt/epics-R3.15.8/modules/caPutLog-${CAPUTLOG_VERSION}
RUN set -exu; \
    cd ${EPICS_MODULES}; \
    wget -O ${CAPUTLOG}.tar.gz ${CAPUTLOG_URL}; \
    tar -zxvf ${CAPUTLOG}.tar.gz; \
    rm -f ${CAPUTLOG}.tar.gz; \
    cd ${CAPUTLOG}; \
    sed -i -e '22cEPICS_BASE='${EPICS_BASE} configure/RELEASE; \
    make -j$(nproc)

# Busy
ARG BUSY_VERSION=R1-7-3
ARG BUSY_URL=https://github.com/epics-modules/busy/archive/${BUSY_VERSION}.tar.gz
LABEL br.cnpem.busy=${BUSY_URL}
ENV BUSY ${EPICS_MODULES}/busy-${BUSY_VERSION}
RUN set -x; \
    set -e; \
    cd ${EPICS_MODULES}; \
    wget -O ${BUSY}.tar.gz ${BUSY_URL}; \
    tar -zxf ${BUSY}.tar.gz; \
    rm -f ${BUSY}.tar.gz; \
    cd ${BUSY}; \
    sed -i \
        -e '7,8s/^/#/'                      \
        -e '10cASYN='${ASYN}                \
        -e '13cAUTOSAVE='${AUTOSAVE}        \
        -e '16cBUSY='${BUSY}                \
        -e '19cEPICS_BASE='${EPICS_BASE}    \
        configure/RELEASE; \
    make -j$(nproc)

# Sequencer
ARG SNCSEQ_URL=https://github.com/ISISComputingGroup/EPICS-seq/archive/vendor_2_2_8.tar.gz
LABEL br.cnpem.seq=${SNCSEQ_URL}
ENV SNCSEQ ${EPICS_MODULES}/seq-2.2.8
RUN set -x; \
    set -e; \
    cd ${EPICS_MODULES}; \
    wget -O ${SNCSEQ}.tar.gz ${SNCSEQ_URL}; \
    tar -xvzf ${SNCSEQ}.tar.gz; \
    rm -f ${SNCSEQ}.tar.gz; \
    mv *seq* ${SNCSEQ}; \
    cd ${SNCSEQ}; \
    sed -i -e '6cEPICS_BASE='${EPICS_BASE} configure/RELEASE; \
    make

# PyDevice
ARG PYDEVICE_COMMIT=4b6afde9c8c70c223217ff439e9aa9d2927042b1
ARG PYDEVICE_URL=https://github.com/klemenv/PyDevice
LABEL br.cnpem.pydevice=${PYDEVICE_URL}/commit/${PYDEVICE_COMMIT}

RUN cd ${EPICS_MODULES} && \
    git clone ${PYDEVICE_URL} && \
    cd PyDevice && \
    git checkout ${PYDEVICE_COMMIT} && \
    sed -i -e "s|EPICS_BASE=.*$|EPICS_BASE=${EPICS_BASE}|" configure/RELEASE && \
    sed -i -e 's|^.*PYTHON_CONFIG=.*$|PYTHON_CONFIG=python3-config|' configure/CONFIG && \
    make

ENV PYDEVICE ${EPICS_MODULES}/PyDevice

# EtherIP
ARG ETHERIP_URL=https://github.com/EPICSTools/ether_ip/archive/ether_ip-3-2.tar.gz
LABEL br.cnpem.etherip=${ETHERIP_URL}
ENV ETHER_IP ${EPICS_MODULES}/ether_ip-ether_ip-3-2
RUN cd ${EPICS_MODULES} && \
    wget ${ETHERIP_URL} && \
    tar -zxvf ether_ip-3-2.tar.gz && \
    rm -f ether_ip-3-2.tar.gz && \
    cd ether_ip-ether_ip-3-2 && \
    sed -i -e '1iEPICS_BASE='${EPICS_BASE} configure/RELEASE && \
    make -j$(nproc)

FROM epics-modules as base

# Epics auto addr list
ENV EPICS_CA_AUTO_ADDR_LIST YES
ENV EPICS_IOC_CAPUTLOG_INET 0.0.0.0
ENV EPICS_IOC_CAPUTLOG_PORT 7012
ENV EPICS_IOC_LOG_INET 0.0.0.0
ENV EPICS_IOC_LOG_PORT 7011

ENV IOC_PROCSERV_SOCK /opt/etheripIOC/sockets/ioc.sock

COPY ./ioc /opt/etheripIOC

WORKDIR /opt/etheripIOC

RUN cd /opt/etheripIOC/ && \
    mkdir sockets && \
    envsubst < configure/RELEASE.tmplt > configure/RELEASE && \
    cat configure/RELEASE && \
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

FROM base AS fcplc01
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME FCPLC01
ENV CMD FCPLC01.cmd
ENV DEVIP 10.20.35.211

FROM base AS fcplc02
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME FCPLC02
ENV CMD FCPLC02.cmd
ENV DEVIP 10.20.35.221

FROM base AS fcplc03
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME FCPLC03
ENV CMD FCPLC03.cmd
ENV DEVIP 10.20.35.231

FROM base AS linac
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME linac
ENV CMD SKID_LINAC.cmd
ENV DEVIP 10.0.38.250

FROM base AS petraV
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME petraV
ENV CMD SKID_PetraV.cmd
ENV DEVIP 10.0.38.246

FROM base AS petraVII
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME petraV
ENV CMD SKID_PetraVII.cmd
ENV DEVIP 10.0.38.249

FROM base AS delta_v2
COPY ./ioc/database /opt/etheripIOC/database
COPY ./ioc/iocBoot /opt/etheripIOC/iocBoot
ENV NAME DELTA-V2
ENV CMD Delta_v2.cmd
ENV DEVIP 1.1.1.1
