# etherip-ioc

This project is an EPICS IOC based on Ether_IP. All etherip-ioc-based EPICS interfaces created by LNLS Controls Group for Sirius control system will be contained in this application.

Wiki-Sirius DOC - https://wiki-sirius.lnls.br/mediawiki/index.php/CON:EPICS_clients_on_Allen_Bradley_PLC

## System requirements

In order to get this software running, you should have installed in your system EPICS base (version 3.14.12.7 recommended). etherip-ioc is intended to run in a Linux environment.

## Supported devices

Currently etherip-ioc provides EPICS interfaces for:

* ControlLogix 5000 - Rockwell Allen Bradley PLCs

## Directory structure

The repository should be cloned with the `--recursive` option:

```
$ git clone --recursive https://github.com/lnls-sirius/etherip-ioc.git
```

This way the user will also obtain the ether_ip source code from GitHub.com. Ether_ip is a Git submodule of etherip-ioc repository.

Here is a brief explanation of the directory structure:

* **database** - Contains files with record definitions for all devices this application supports.

* **iocBoot** - Directory where the IOC initialization scripts reside. These files must be properly configured, as described at the "Executing the IOC" section. In the future, definition of control system nodes structure will lead to many specific initialization scripts. 

## Compiling

This software is distributed in the form of source code. In order to compile it, first define at the `ether_ip/configure/RELEASE` file the system paths to EPICS base and asynDriver. By default, these configurations are:

```
EPICS_VER=master
EPICS_BASE_RELEASE=/opt/base-3.14.12.7/

```

After editing `ether_ip/configure/RELEASE`, run these commands at the top directory:

```
$ cd ..
$ make

```

## Executing the IOC

To run this application, execute one of the scripts located at iocBoot directory.

The first line of script file must be the correct path to the application executable. If the system CPU is an ARM core, the first line must be:

```
#!../bin/linux-arm/eipIoc
```

Instead, if we are working in a 64-bit computer:

```
#!../bin/linux-x86_64/eipIoc
```

In the script file, four environment variables must be correctly defined:

* **EPICS_BASE** - Path to the system directory where EPICS base is installed.

* **ARCH** - System architecture ("linux-arm" for an ARM environment or "linux-x86_64" for a 64-bit Linux architecture, for example).

## Uninstalling

To remove this software from a computer, just delete its parent directory.
