etherip-ioc
===========
This project is an EPICS IOC based on Ether_IP. All etherip-ioc-based EPICS interfaces created by LNLS Controls Group for Sirius control system will be contained in this application.

Wiki-Sirius DOC - https://wiki-sirius.lnls.br/mediawiki/index.php/CON:EPICS_clients_on_Allen_Bradley_PLC

Supported devices
-----------------
Currently etherip-ioc provides EPICS interfaces for:

* ControlLogix 5000 - Rockwell Allen Bradley PLCs

Directory structure
-------------------
Here is a brief explanation of the directory structure (by default, this repository is located at `/opt/etherip-ioc`):

* **database** - Contains files with record definitions for all devices this application supports.
* **iocBoot** - Directory where the IOC initialization scripts reside. These files must be properly configured, as described at the "Executing the IOC" section. In the future, definition of control system nodes structure will lead to many specific initialization scripts.
* **etc** - Spreasheets with records definitions.
* **scripts** - IOC generation scripts.
* **services** - systemd services.

IOC Generation
--------------
There's a shell script for each application. Just run it (Always check if all parameters match the system configuration).
```
cd scripts
./<script>
```

Executing the IOC
-----------------
Start the corresponding systemd service.

Update
------
In order to update the IOC, replace the spreadsheet at `etc/<spreadsheet>`, execute the corresponding shell script at `scripts/<script>` and restart the IOC.
