#!/usr/bin/env python
import os
import json

from iocgen.templates import bi_template

default = {"onam": "Enable", "znam": "Disable", "desc": ""}

with open("sirius.json", "r") as f:
    data = json.load(f)

if __name__ == "__main__":
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../database/Sirius.db"
    )
    with open(path, "w+") as _f:
        for d in data:
            if d["type"] == "bi":
                _f.write(bi_template.safe_substitute(default, **d))
