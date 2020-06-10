#!/usr/bin/env
from string import Template
bi_template = Template(
    """
record(bi, "${pv}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(ONAM, "${highname}")
    field(ZNAM, "${lowname}")
}
"""
)

data = [{
        "tag":"Program:IHM.EXT_BO_01D_MA_B.Alimentacao",
}]

if __name__ == "__main__":

