from string import Template

tag_dict_template = Template(
    """
  {
    "type": "tag",
    "desc": "${desc}",
    "name": "${name}",
    "dtype": "${data_type}",
    "inout": "${inout}",
    "cmdtime": "${cmdtime}",
    "tag": "${tag}",
    "egu": "${egu}",
    "scan": "${scan}",
    "prec": "${prec}",
    "hsv": "${hsv}",
    "hhsv": "${hhsv}",
    "lsv": "${lsv}",
    "llsv": "${llsv}"
  },
"""
)

calc_dict_template = Template(
"""
  {
    "type": "calc",
    "desc": "${desc}",
    "name": "${name}",
    "inp": "${inp}",
    "out": "${out}",
    "egu": "${egu}",
    "prec": "${prec}",
    "conv": "${conv}"
  },
"""
)

conv_dict_template = Template(
"""
  {
    "type": "conv",
    "desc": "${desc}",
    "name": "${name}",
    "inp": "${inp}",
    "egu": "${egu}",
    "prec": "${prec}",
    "args": "${args}"
  },
"""
)

var_dict_template = Template(
"""
  {
    "type": "var",
    "desc": "${desc}",
    "name": "${name}",
    "dtype": "${data_type}",
    "egu": "${egu}",
    "prec": "${prec}",
    "val": "${val}"
  },
"""
)

