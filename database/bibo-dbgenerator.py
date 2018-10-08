#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

tipo = str(sys.argv[1])
arquivo = str(sys.argv[2])
pv = str(sys.argv[3])
tag = str(sys.argv[4])
scan = str(sys.argv[5])
highname = str(sys.argv[6])
lowname = str(sys.argv[7])

try:
    file = open(arquivo, 'r')
    conteudo = file.readlines()

    if tipo == "bi":
        conteudo.append('\n' + 'record (bi, "{}")'.format(pv) + '\n' + '{' + '\n' \
                        + '    field(INP, "@$(PLC) {}")'.format(tag) + '\n' \
                        + '    field(SCAN, "{}")'.format(scan) + '\n' \
                        + '    field(ZNAM, "{}")'.format(lowname) + '\n' \
                        + '    field(ONAM, "{}")'.format(highname) + '\n' \
                        + '    field(DTYP, "EtherIP")' + '\n' \
                        + '}' + '\n')

    elif tipo == "bo":
        conteudo.append('\n' + 'record (bo, "{}")'.format(pv) + '\n' + '{' + '\n' \
                        + '    field(INP, "@$(PLC) {}")'.format(tag) + '\n' \
                        + '    field(SCAN, "{}")'.format(scan) + '\n' \
                        + '    field(ZNAM, "{}")'.format(lowname) + '\n' \
                        + '    field(ONAM, "{}")'.format(highname) + '\n' \
                        + '    field(DTYP, "EtherIP")' + '\n' \
                        + '}' + '\n')

    file = open(arquivo, 'w')
    file.writelines(conteudo)
    file.close()

except Exception as e:
    print(e)
    pass
