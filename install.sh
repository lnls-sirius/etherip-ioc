#!/bin/sh

cd /opt/epics-R3.14.12.7/modules
wget https://github.com/EPICSTools/ether_ip/archive/ether_ip-2-27.tar.gz
tar -xvzf ether_ip-2-27.tar.gz
rm ether_ip-2-27.tar.gz
sed -i -e '11s/^/#/' -e '12iEPICS_BASE=/opt/epics-R3.14.12.7/base' ether_ip-ether_ip-2-27/configure/RELEASE
cd ether_ip-ether_ip-2-27
make
