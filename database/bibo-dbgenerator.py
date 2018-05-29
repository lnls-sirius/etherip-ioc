#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

tipo = str(sys.argv[1])
arquivo = str(sys.argv[2])
pv = str(sys.argv[3])
tag = str(sys.argv[4])
scan = str(sys.argv[5])

try:
    file = open(arquivo, 'r')
    conteudo = file.readlines()

    if tipo == "bi":
        conteudo.append('\n' + 'record (bi, "$(IOC):{}")'.format(pv) + '\n' + '{' + '\n' \
                        + '    field(INP, "@$(PLC) {}")'.format(tag) + '\n' \
                        + '    field(SCAN, "{} second")'.format(scan) + '\n' \
                        + '    field(ZNAM, "False")' + '\n' \
                        + '    field(ONAM, "True")' + '\n' \
                        + '    field(DTYP, "EtherIP")' + '\n' \
                        + '}' + '\n')

    elif tipo == "bo":
        conteudo.append('\n' + 'record (bo, "$(IOC):{}")'.format(pv) + '\n' + '{' + '\n' \
                        + '    field(SCAN, "Passive")'+ '\n' \
                        + '    field(DTYP, "EtherIP")'+ '\n' \
                        + '    field(OUT, "@$(PLC) {}")'.format(tag) + '\n' \
                        + '    field(ZNAM, "False")' + '\n' \
                        + '    field(ONAM, "True")' + '\n' \
                        + '    field(SCAN, "{} second")'.format(scan) + '\n' \
                        + '}' + '\n')

    file = open(arquivo, 'w')
    file.writelines(conteudo)
    file.close()

except Exception as e:
    print(e)
    pass