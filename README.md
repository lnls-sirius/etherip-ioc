# etherip-ioc

This project is an EPICS IOC based on Ether_IP.

## Supported devices

Currently etherip-ioc provides EPICS interfaces for:

## IOC Generation and Docker images

There's a shell script for each application. Just run it (Always check if all parameters match the system configuration).

```command
cd scripts
make <target>
```

These IOCs are meant to run on Docker containers. In order to build a new image the compose file [`docker-compose.yml`](./docker-compose.yml) is used. For each subsystem a new target must be specified at the [`Dockerfile`](./Dockerfile) and referenced on the build section of the previously mentioned [`docker-compose.yml`](./docker-compose.yml).

```command
docker-compose build <service_name>
```

The build process will **not** execute the database generation scripts. This is a conscious choice that aims to keep the content of the Docker container in sync with this repository.

## Executing the IOC

Deploy the a Docker container with the correct settings e.g. Environment variables and network configuration.

The following environment variables are used to customize the deployment:

| Name                    | Default | Desc                         |
| ----------------------- | ------- | ---------------------------- |
| CMD                     |         | iocBoot cmd file             |
| DEVIP                   |         | PLC IP Address               |
| EPICS_IOC_CAPUTLOG_INET | 0.0.0.0 | EPICS Logging Inet (generic) |
| EPICS_IOC_CAPUTLOG_PORT | 7012    | EPICS Logging Port (generic) |
| EPICS_IOC_LOG_INET      | 0.0.0.0 | EPICS Logging Inet (caput)   |
| EPICS_IOC_LOG_PORT      | 7011    | EPICS Logging Port (caput)   |

## Update

Update the corresponding spreadsheet at `etc/<spreadsheet>`, `cd ./scripts` and run the corresponding `make <target>`.
