# etherip-ioc

This project is an EPICS IOC based on the [Ether_IP](https://github.com/EPICSTools/ether_ip) module.

Python scripts are used to generate EPICS database files and iocBoot cmds. The data sources for generation are JSON files following the specification detailed below.

## IOC specification with JSON file

The data source files used to generate the IOC must define a list of dictionaries.

[ <dictionary 1>, <dictionary 2>, ..., <dictionary N>]

The dictionary values should always be written as strings, using double quotes (").

As an example, we could define an IOC to read the tag "tagexample" with the PV "example:pv:name"
and to provide two other PVs with the tag value multiplied by 10 and 100, respectively:

```sh
[
  {
    "type": "tag",
    "desc": "example description",
    "name": "example:pv:name",
    "dtype": "float",
    "inout": "read",
    "tag": "tagexample",
    "scan": "1",
  },
  {
    "type": "calc",
    "desc": "example calculation 1",
    "name": "example:pv:calc1",
    "inp": "example:pv:name",
    "conv": "pv * 10"
  },
  {
    "type": "calc",
    "desc": "example calculation 2",
    "name": "example:pv:calc2",
    "inp": "example:pv:name",
    "conv": "pv * 100"
  }
]
```

Whitespaces and line breaks are optional.

## Dictionary templates

Each dictionary in the JSON file must follow one of the templates supported by the IOC, as presented below.
The text enclosed in < > provide a description of the data field in the template and should be
replaced by the appropriate PV data in the JSON file.

### Dictionary type: tag

This dictionary specifies a PV that directly maps a PLC tag.

```sh
  {
    "type": "tag",
    "desc": "<optional: description>",
    "name": "<required: pv name>",
    "dtype": "<required: data type; options: bool | float>",
    "inout": "<required: data direction; options: read | write>",
    "tag": "<required: PLC tag>",
    "egu": "<optional: engineering units>",
    "scan": "<required for read type: scan rate, options: 0.1 | 0.2 | 0.5 | 1 | 2 | 5 | 10 >",
    "prec": "<optional: number of decimal places>",
    "hsv": "<optional: high alarm severity, options: no_alarm | minor | major | invalid>",
    "hhsv": "<optional: high high alarm severity, options: no_alarm | minor | major | invalid>",
    "lsv": "<optional: low alarm severity, options: no_alarm | minor | major | invalid>",
    "llsv": "<optional: low low alarm severity, options: no_alarm | minor | major | invalid>"
  }
```
### Dictionary type: calc

This dictionary specifies a PV that takes the value of another PV, performs
a calculation and, optionally, sends it to another record.

```sh
  {
    "type": "calc",
    "desc": "<optional: description>",
    "name": "<required: pv name>",
    "inp": "<optional: input pv name>",
    "out": "<optional: output pv name>",
    "egu": "<optional: engineering units>",
    "prec": "<optional: number of decimal places>",
    "conv": "<calculation string; input value must be referenced as pv>"
  }
```
### Dictionary type: conv

This dictionary specifies a PV that takes the value of another PV and calculates
a polynomial with the coefficients provided by a waveform PV (array).
The coefficients must be ordered from the smaller to the largest corresponding exponent.

```sh
  {
    "type": "conv",
    "desc": "<optional: description>",
    "name": "<required: pv name>",
    "inp": "<optional: input pv name>",
    "egu": "<optional: engineering units>",
    "prec": "<optional: number of decimal places>",
    "args": "<optional: name of 1D array PV containing coefficients>"
  }
```
### Dictionary type: var

This dictionary specifies a PV that does not read/write from device support.

```sh
  {
    "type": "var",
    "desc": "<optional: description>",
    "name": "<required: pv name>",
    "dtype": "<required: data type; options: bool | float | array>",
    "egu": "<optional: engineering units>",
    "prec": "<optional: number of decimal places>",
    "val": "<optional: initial value, e.g., [1, 2, 3, 4]>"
  }
```

## Bulding a Docker image

In order to build the image, verify the settings at `./scripts/config.sh` then use `docker-compose build`.
The config file will update the `.env` file used by docker-compose.

```sh
sh ./scripts/config.sh
docker-compose build <service_name>
```

## IOC Generation and Docker images

Before building the docker image the user should generate the IOC (protocol, database and iocBoot cmds).
This is by design so we can monitor changes via git.
There's a shell script for each application. Just run it (Always check if all parameters match the system configuration).

```command
cd scripts
make <target>
```

These IOCs are meant to run on Docker containers.
In order to build a new image the compose file [`docker-compose.yml`](./docker-compose.yml) is used.
For each subsystem a new target must be specified at the [`Dockerfile`](./Dockerfile) and referenced on the build section of the previously mentioned [`docker-compose.yml`](./docker-compose.yml).

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

Update the corresponding JSON file at `etc/<json>`, `cd ./scripts` and run the corresponding `make <target>`.
