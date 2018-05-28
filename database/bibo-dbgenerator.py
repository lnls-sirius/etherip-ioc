#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

tipo = str(sys.argv[1])
arquivo = str(sys.argv[2])
pv = str(sys.argv[3])
tag = str(sys.argv[4])

try:
    if tipo == "bi":
        file = open(arquivo,'r')
        conteudo = file.readlines()
        conteudo.append('\n' + 'record (bi, "{}")'.format(pv) + '\n' + '{' + '\n' \
                        + '    field (INP, "{}")'.format(tag) + '\n' + '}' + '\n')
        file = open(arquivo, 'w')
        file.writelines(conteudo)
        file.close()

    elif tipo == "bo":
        file = open(arquivo,'r')
        conteudo = file.readlines()
        conteudo.append('\n' + 'record (bo, "{}")'.format(pv) + '\n' + '{' + '\n' \
                        + '    field(SCAN, "Passive")'+ '\n' \
                        + '    field(DTYP, "EtherIP")'+ '\n' \
                        + '    field(OUT, "{}")'.format(tag) + '\n' \
                        + '    field(ZNAM, "False")' + '\n' \
                        + '    field(ONAM, "True")' + '\n' + '}' + '\n')
        file = open(arquivo, 'w')
        file.writelines(conteudo)
        file.close()

except Exception as e:
    print(e)
    pass