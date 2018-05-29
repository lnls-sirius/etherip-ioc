#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

arquivo = str(sys.argv[1])
pv = str(sys.argv[2])
tag = str(sys.argv[3])
scan = str(sys.argv[4])
prec = str(sys.argv[5])
egu = str(sys.argv[6]) #unit
eguf = str(sys.argv[7])
hopr = str(sys.argv[8])
lopr = str(sys.argv[9])
hihi = str(sys.argv[10])
high = str(sys.argv[11])
low = str(sys.argv[12])
lolo = str(sys.argv[13])
hhsv = str(sys.argv[14])
hsv = str(sys.argv[15])
lsv = str(sys.argv[16])
llsv = str(sys.argv[17])

try:
    file = open(arquivo,'r')
    conteudo = file.readlines()

    conteudo.append('\n' + 'record (ai, "$(IOC):{}")'.format(pv) + '\n' + '{' + '\n' \
                    + '    field(SCAN, "{}")'.format(scan)+ '\n' \
                    + '    field(DTYP, "EtherIP")' + '\n' \
                    + '    field(INP, "{}")'.format(tag) + '\n'
                    + '    field(EGUF, "{}")'.format(eguf) + '\n' \
                    + '    field(EGU, "{}")'.format(egu) + '\n' \
                    + '    field(HOPR, "{}")'.format(hopr) + '\n' \
                    + '    field(LOPR, "{}")'.format(lopr) + '\n' \
                    + '    field(HIHI, "{}")'.format(hihi) + '\n' \
                    + '    field(HIGH, "{}")'.format(high) + '\n' \
                    + '    field(LOW, "{}")'.format(low) + '\n' \
                    + '    field(LOLO, "{}")'.format(lolo) + '\n' \
                    + '    field(HHSV, "{}")'.format(hhsv) + '\n' \
                    + '    field(HSV, "{}")'.format(hsv) + '\n' \
                    + '    field(LSV, "{}")'.format(lsv) + '\n' \
                    + '    field(LLSV, "{}")'.format(llsv) + '\n' \
                    + '    field(PREC, "{}")'.format(prec) + '\n' \
                    + '}' + '\n')

    file = open(arquivo,'w')
    file.writelines(conteudo)
    file.close()

except Exception as e:
    print(e)
    pass