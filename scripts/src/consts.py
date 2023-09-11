SCAN_VALUES = [".1", ".2", ".5", "1", "2", "5", "10", "I/O Intr", "Event", "Passive"]
# default record field values
defaults = {
    "scan": ".1",
    "egu": "",
    "desc": "",
    "onam": "True",
    "znam": "False",
    "zsv": "",
    "osv": "",
    "prec": "3",
    "drvh": "",
    "drvl": "",
    "hopr": "",
    "lopr": "",
    "hihi": "",
    "high": "",
    "low": "",
    "lolo": "",
    "hhsv": "",
    "hsv": "",
    "lsv": "",
    "llsv": "",
    "hyst": "",
    "sizv": "41",
    "omsl": "supervisory",
    "dol": "",
    "shft": "",
    "ivoa": "Continue normally",
    "ivov": "",
    "unsv": "NO_ALARM",
    "cosv": "NO_ALARM",
    "zrvl": "0",
    "zrst": "",
    "zrsv": "",
    "onvl": "1",
    "onst": "",
    "onsv": "",
    "twvl": "2",
    "twst": "",
    "twsv": "",
    "thvl": "3",
    "thst": "",
    "thsv": "",
    "frvl": "4",
    "frst": "",
    "frsv": "",
    "fvvl": "5",
    "fvst": "",
    "fvsv": "",
    "sxvl": "6",
    "sxst": "",
    "sxsv": "",
    "svvl": "7",
    "svst": "",
    "svsv": "",
    "eivl": "8",
    "eist": "",
    "eisv": "",
    "nivl": "9",
    "nist": "",
    "nisv": "",
    "tevl": "10",
    "test": "",
    "tesv": "",
    "elvl": "11",
    "elst": "",
    "elsv": "",
    "tvvl": "12",
    "tvst": "",
    "tvsv": "",
    "ttvl": "13",
    "ttst": "",
    "ttsv": "",
    "ftvl": "14",
    "ftst": "",
    "ftsv": "",
    "ffvl": "15",
    "ffst": "",
    "ffsv": "",
}
class json_info:
    class keys:
        gen_type='type'
        name='name'
        desc='desc'
        tag='tag'
        inout='inout'
        dtype='dtype'
        egu='egu'
        scan='scan'
        prec='prec'
        inp='inp'
        out='out'
        args='args'
        cmd_high='cmdtime'
        conv='conv'
    class gen_type:
        tag = 'tag'
        conv = 'conv'
        calc = 'calc'
        var = 'var'
    class inout:
        read = 'read'
        write = 'write'
    class dtype:
        bool = 'bool'
        float = 'float'
        int = 'int'
        array = 'array'

