#!/usr/bin/env python
import os
from string import Template

bi_template = Template(
    """
record(bi, "${name}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
}
"""
)
default = {"onam": "Enable", "znam": "Disable", "desc": ""}
data = [
    {
        "tag": "Program:IHM.EXT_BO_01D_MA_B.Input_Temperatura",
        "scan": ".1",
        "template": bi_template,
        "name": "IHM:EXT_BO_01D_MA_B:Input_Temperatura",
    },
    {
        "tag": "Program:IHM.EXT_BO_01D_MA_B.Input_Protecao",
        "scan": ".1",
        "template": bi_template,
        "name": "IHM:EXT_BO_01D_MA_B:Input_Protecao",
    },
    {
        "tag": "Program:IHM.EXT_BO_01D_MA_B.Alimentacao",
        "scan": ".1",
        "template": bi_template,
        "name": "IHM:EXT_BO_01D_MA_B:Alimentacao",
    },
    {
        "tag": "Program:IHM.EXT_BO_01D_MA_B.Falha_Temperatura",
        "scan": ".1",
        "template": bi_template,
        "name": "IHM:EXT_BO_01D_MA_B:Falha_Temperatura",
    },
    {
        "tag": "Program:IHM.EXT_BO_01D_MA_B.Falha_Protecao",
        "scan": ".1",
        "template": bi_template,
        "name": "IHM:EXT_BO_01D_MA_B:Falha_Protecao",
    },
    {
        "tag": "Program:IHM.EXT_BO_01D_MA_B.Falha_Geral",
        "scan": ".1",
        "template": bi_template,
        "name": "IHM:EXT_BO_01D_MA_B:Falha_Geral",
    },
]

if __name__ == "__main__":
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../database/Sirius.db"
    )
    with open(path, "w+") as _f:
        for d in data:
            _f.write(d["template"].safe_substitute(default, **d))
