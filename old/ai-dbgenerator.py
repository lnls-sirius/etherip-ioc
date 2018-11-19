#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

arquivo = str(sys.argv[1])
scan = str(sys.argv[2])
prec = str(sys.argv[3])
egu = str(sys.argv[4])
pv = str(sys.argv[5])
tag = str(sys.argv[6])

try:
    file = open(arquivo,'r')
    conteudo = file.readlines()

    conteudo.append('\n' + 'record (ai, "$(IOC):{}")'.format(pv) + '\n' + '{' + '\n' \
                    + '    field(SCAN, "{}")'.format(scan)+ '\n' \
                    + '    field(DTYP, "EtherIP")' + '\n' \
                    + '    field(INP, "@$(PLC) {}")'.format(tag) + '\n'
                    + '    field(EGU, "{}")'.format(egu) + '\n' \
                    + '    field(PREC, "{}")'.format(prec) + '\n' \
                    + '}' + '\n')

    file = open(arquivo,'w')
    file.writelines(conteudo)
    file.close()

except Exception as e:
    print(e)
    pass
