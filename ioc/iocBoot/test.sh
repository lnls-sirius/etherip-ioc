#!/bin/bash
set -x
function getTag {
/opt/epics-R3.15.8/modules/ether_ip-ether_ip-3-2/bin/linux-x86_64/ether_ip_test -i 10.0.38.199 -s $1 $2
#sleep 1
echo ""
}
#getTag 0 EXT_BO_01D_MA_B.Input_Temperatura
getTag 1 EXT_BO_01D_MA_B.Input_Temperatura
getTag 1 Program:IHM.EXT_BO_01D_MA_B.Input_Temperatura
#getTag 2 EXT_BO_01D_MA_B.Input_Temperatura
#getTag 4 EXT_BO_01D_MA_B.Input_Temperatura
#getTag 5 EXT_BO_01D_MA_B.Input_Temperatura
#getTag 6 EXT_BO_01D_MA_B.Input_Temperatura
#getTag 7 EXT_BO_01D_MA_B.Input_Temperatura
#getTag 8 EXT_BO_01D_MA_B.Input_Temperatura
##########getTag 9 EXT_BO_01D_MA_B.Input_Temperatura
