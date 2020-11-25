# etherip-ioc

This project is an EPICS IOC based on Ether_IP. All etherip-ioc-based EPICS interfaces created by LNLS Controls Group for Sirius control system will be contained in this application.

Wiki-Sirius DOC - https://wiki-sirius.lnls.br/mediawiki/index.php/CON:EPICS_clients_on_Allen_Bradley_PLC

## Supported devices

Currently etherip-ioc provides EPICS interfaces for:

- ControlLogix 5000 - Rockwell Allen Bradley PLCs

## Directory structure

Here is a brief explanation of the directory structure (by default, this repository is located at `/opt/etherip-ioc`):

- **database** - Contains files with record definitions for all devices this application supports.
- **iocBoot** - Directory where the IOC initialization scripts reside. These files must be properly configured, as described at the "Executing the IOC" section. In the future, definition of control system nodes structure will lead to many specific initialization scripts.
- **etc** - Spreasheets with records definitions.
- **scripts** - IOC generation scripts.

## IOC Generation and Docker images

There's a shell script for each application. Just run it (Always check if all parameters match the system configuration).

```command
cd scripts
./<script>
```

These IOCs are meant to run on Docker containers. In order to build a new image the compose file [`docker-compose.yml`](./docker-compose.yml) is used. For each subsystem a new target must be specified at the [`Dockerfile`](./Dockerfile) and referenced on the build section of the previously mentioned [`docker-compose.yml`](./docker-compose.yml).

```command
docker-compose build <service_name>
```

The build process will **not** execute the database generation scripts. This is a conscious choice and that aims to keep the content of the Docker container in sync with this repository.

## Executing the IOC

Deploy the a Docker container with the correct settings e.g. Environment variables and network configuration.

The following environment variables are used to customize the deployment:

| Name  | Default | Desc |
|------ |---------|------|
| CMD   |         | iocBoot cmd file |
| DEVIP |         |PLC IP Address |
| IOC_PROCSERV_PREFIX || procServControl Prefix |
|EPICS_IOC_CAPUTLOG_INET|0.0.0.0|EPICS Logging Inet (generic)|
|EPICS_IOC_CAPUTLOG_PORT|7012|EPICS Logging Port (generic)|
|EPICS_IOC_LOG_INET|0.0.0.0|EPICS Logging Inet (caput)|
|EPICS_IOC_LOG_PORT|7011|EPICS Logging Port (caput)|

## Update

Update the corresponding spreadsheet at `etc/<spreadsheet>`, `cd ./scripts` and run the corresponding `make <target>`.
