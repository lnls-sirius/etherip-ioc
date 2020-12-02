#!/usr/bin/env python3
import argparse
import pandas
import logging
import os
import re
from templates_delta import *

logger = logging.getLogger()

SCAN_VALUES = [".1", ".2", ".5", "1", "2", "5", "10", "I/O Intr", "Event", "Passive"]
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

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
}

def replace_prefix(pv, new_prefix, delimiters=':'):
    """ Replace a prefix or prefix macro from an EPICS PV name.
        The prefix is determined by a delimiter or list of possible
        delimiters. The last occurrence of all delimiters indicate
        the prefix end.
    """
    # if delimiters not a list, make it a list
    if type(delimiters) is not list:
        delimiters = [delimiters]
    # remove dummy prefix from pv
    pv_property = pv
    for delim in delimiters:
        substr = pv_property.rpartition(delim)[2]
        if substr != '':
            pv_property = substr
    # return pv with new prefix
    return new_prefix + pv_property

def config_logger(logger):
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-6s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def get_args():
    parser = argparse.ArgumentParser(
        description="""Generate Sirius Ether IP - IOC.\n
            SCAN_VALUES: {}""".format(
            SCAN_VALUES
        )
    )
    parser.add_argument("spreadsheet", help="Excel spreadsheet location.")
    parser.add_argument(
        "--plc-name",
        required=True,
        dest="plc_name",
        help="Name used to identify the PLC.",
    )
    parser.add_argument(
        "--plc-module",
        required=True,
        dest="plc_module",
        help="Slot of the variables to be archived in PLC.",
    )

    parser.add_argument("--col-desc", default="Description", help="EPICS desc column name.")
    parser.add_argument(
        "--col-dtype", default="Data Type", help="Data type column name."
    )
    parser.add_argument("--col-egu", default="EGU", help="EPICS egu column name.")
    parser.add_argument(
        "--col-inout", default="In/Out", help="Input/Output column name."
    )
    parser.add_argument("--col-prec", default="Prec", help="EPICS prec column name.")
    parser.add_argument("--col-pv", default="NAME", help="PV column name.")
    parser.add_argument("--col-scan", default="Scan", help="EPICS scan time column name.")
    parser.add_argument("--col-tag", default="TAG", help="PLC tag column name.")
    parser.add_argument("--ioc-name", required=True, help="IOC name.")
    parser.add_argument("--sheet", required=True, help="Sheet name.")

    parser.add_argument(
        "--arch",
        choices=["linux-x86_64", "linux-arm"],
        default="linux-x86_64",
        help="System architecture.",
    )

    parser.add_argument(
        "--col-znam",
        default="ZNAM",
        help="EPICS Binary Zero Name column name."
    )
    parser.add_argument(
        "--col-onam",
        default="ONAM",
        help="EPICS Binary One Name column name."
    )
    parser.add_argument(
        "--col-zsv",
        default="ZSV",
        help="EPICS Binary Zero Severity column name."
    )
    parser.add_argument(
        "--col-osv",
        default="OSV",
        help="EPICS Binary One Severity column name."
    )
    parser.add_argument(
        "--col-drvh",
        default="DRVH",
        help="EPICS Analog Out Driver High column name."
    )
    parser.add_argument(
        "--col-drvl",
        default="DRVL",
        help="EPICS Analog Out Driver Low column name."
    )
    parser.add_argument(
        "--col-hopr",
        default="HOPR",
        help="EPICS High Operating Range column name."
    )
    parser.add_argument(
        "--col-lopr",
        default="LOPR",
        help="EPICS Low Operating Range column name."
    )
    parser.add_argument(
        "--col-hihi",
        default="HIHI",
        help="EPICS High High Alarm Limit column name."
    )
    parser.add_argument(
        "--col-high",
        default="HIGH",
        help="EPICS High Alarm Limit column name."
    )
    parser.add_argument(
        "--col-low",
        default="LOW",
        help="EPICS Low Alarm Limit column name."
    )
    parser.add_argument(
        "--col-lolo",
        default="LOLO",
        help="EPICS Low Low Alarm Limit column name."
    )
    parser.add_argument(
        "--col-hhsv",
        default="HHSV",
        help="EPICS High High Alarm Severity column name."
    )
    parser.add_argument(
        "--col-hsv",
        default="HSV",
        help="EPICS High Alarm Severity column name."
    )
    parser.add_argument(
        "--col-lsv",
        default="LSV",
        help="EPICS Low Alarm Severity column name."
    )
    parser.add_argument(
        "--col-llsv",
        default="LLSV",
        help="EPICS Low Low Alarm Severity column name."
    )
    parser.add_argument(
        "--col-hyst",
        default="HYST",
        help="EPICS Alarm Deadband column name."
    )
    parser.add_argument(
        "--col-sizv",
        default="SIZV",
        help="EPICS Long String Size of Buffer column name."
    )
    parser.add_argument(
        "--bi",
        nargs='+',
        default="Binary Input",
        help="EPICS bi data type alias (can be more than one)."
    )
    parser.add_argument(
        "--bo",
        nargs='+',
        default="Binary Output",
        help="EPICS bo data type alias (can be more than one)."
    )
    parser.add_argument(
        "--ai",
        nargs='+',
        default="Analog Input",
        help="EPICS ai data type alias (can be more than one)."
    )
    parser.add_argument(
        "--ao",
        nargs='+',
        default="Analog Output",
        help="EPICS ao data type alias (can be more than one)."
    )
    # EPICS base 3.15 only
    parser.add_argument(
        "--lsi",
        nargs='+',
        default="Long String Input",
        help="EPICS lsi data type alias (can be more than one)."
    )
    # EPICS base 3.15 only
    parser.add_argument(
        "--lso",
        nargs='+',
        default="Long String Output",
        help="EPICS lso data type alias (can be more than one)."
    )
    parser.add_argument(
        "--multi-cmd",
        nargs=4,
        action='append',
        help="Create a startup script copy for each cmd name, IP address,"
             " module number, and associated DB file name."
    )
    parser.add_argument(
        "--multi-db",
        nargs=2,
        action='append',
        help="Create a database copy for each prefix and file name listed,"
             " replacing prefixes already provided by the spreadsheet,"
             " i.e. any substring ending in ':' or ')'."
    )

    args = parser.parse_args()
    return args

def generate_all(args):
    if args.multi_db is not None:
        generate_multi_db(args)
    if args.multi_cmd is not None:
        generate_multi_cmd(args)
    if (args.multi_db is None
        and args.multi_cmd is None):
        generate_single(args)

def generate_single(args):
    generate(args, db=True, db_name=args.ioc_name,
                   cmd=True, cmd_name=args.ioc_name)

def generate_multi_db(args):
    if args.multi_db is None:
        logger.error(
            'Multi DB option specified, but no DB name '
            'or prefix was provided.'
        )
        return -1
    
    for prefix_and_name in args.multi_db:
        prefix = prefix_and_name[0]
        db_name = prefix_and_name[1]
        generate(args, db=True, db_name=db_name,
                       cmd=False, new_prefix=prefix)

def generate_multi_cmd(args):
    if args.multi_cmd is None:
        logger.error(
            'Multi CMD option specified, but no IOC name, '
            'IP and associated DB file name were provided.'
        )
        return -1
    
    for cmd_name, ip, module, db_name in args.multi_cmd:
        generate(args, db=False, db_name=db_name,
                       cmd=True, cmd_name=cmd_name,
                       ip=ip, module=module)

def generate(args, db=True, db_name='example',
                   cmd=True, cmd_name='example',
                   ip='', module='', new_prefix=''):
    sheet_name = args.sheet.split(",")
    logger.info("Args, {}.".format(vars(args)))

    IOC_CMD_PATH = os.path.join(BASE_PATH, "../iocBoot/iocetheripIOC/") + cmd_name + ".cmd"

    IOC_DATABASE_PATH = os.path.join(BASE_PATH, "../database/") + db_name + ".db"

    if ip == '':
        PLC_IP = args.plc_ip
    else:
        PLC_IP = ip

    if module == '':
        PLC_MODULE = args.plc_module
    else:
        PLC_MODULE = str(module)

    logger.info('Generating "{}.cmd" file at "{}".'.format(cmd_name, IOC_CMD_PATH))

    # generate CMD file
    if cmd == True:
        with open(IOC_CMD_PATH, "w+") as f:
            f.write(
                cmd_template.safe_substitute(
                    arch=args.arch,
                    database=db_name+".db",
                    module=PLC_MODULE,
                    plc=args.plc_name,
                )
            )
    tags = {}
    logger.info(
        'Generating "{}.db" file at "{}".'.format(args.ioc_name, IOC_DATABASE_PATH)
    )

    # generate DB file
    if db == True:
        with open(IOC_DATABASE_PATH, "w+") as f:
            for s_name in sheet_name:
                sheet = pandas.read_excel(args.spreadsheet, sheet_name=s_name, dtype=str)
                replace_info = {"\n": ""}
                sheet.replace(replace_info, inplace=True, regex=True)
                sheet.fillna("", inplace=True)
                # check required columns
                if args.col_pv not in sheet.columns:
                    logger.error(
                        'Could not find required {} column in {} sheet.'
                        .format(args.col_pv, s_name)
                    )
                    continue
                if args.col_tag not in sheet.columns:
                    logger.error(
                        'Could not find required {} column in {} sheet.'
                        .format(args.col_tag, s_name)
                    )
                    continue
                if args.col_dtype not in sheet.columns:
                    logger.error(
                        'Could not find required {} column in {} sheet.'
                        .format(args.col_dtype, s_name)
                    )
                    continue
                for n, row in sheet.iterrows():
                    # main columnn
                    name = row[args.col_pv]
                    tag = row[args.col_tag]
                    dtype = row[args.col_dtype]
                    # optional columns
                    inout = row.get(args.col_inout, '')
                    desc = row.get(args.col_desc, defaults['desc'])
                    egu = row.get(args.col_egu, defaults['egu'])
                    scan = row.get(args.col_scan, defaults['scan'])
                    prec = row.get(args.col_prec, defaults['prec'])
                    znam = row.get(args.col_znam, defaults['znam'])
                    onam = row.get(args.col_onam, defaults['onam'])
                    zsv = row.get(args.col_zsv, defaults['zsv'])
                    osv = row.get(args.col_osv, defaults['osv'])
                    drvh = row.get(args.col_drvh, defaults['drvh'])
                    drvl = row.get(args.col_drvl, defaults['drvl'])
                    hopr = row.get(args.col_hopr, defaults['hopr'])
                    lopr = row.get(args.col_lopr, defaults['lopr'])
                    hihi = row.get(args.col_hihi, defaults['hihi'])
                    high = row.get(args.col_high, defaults['high'])
                    low = row.get(args.col_low, defaults['low'])
                    lolo = row.get(args.col_lolo, defaults['lolo'])
                    hhsv = row.get(args.col_hhsv, defaults['hhsv'])
                    hsv = row.get(args.col_hsv, defaults['hsv'])
                    lsv = row.get(args.col_lsv, defaults['lsv'])
                    llsv = row.get(args.col_llsv, defaults['llsv'])
                    hyst = row.get(args.col_hyst, defaults['hyst'])
                    sizv = row.get(args.col_sizv, defaults['sizv'])
    
                    if not name or name.startswith("-"):
                        continue
    
                    # if new prefix specified, replace current prefix
                    if new_prefix != '':
                        name = replace_prefix(name, new_prefix, delimiters=[':', ')'])
    
                    if len(desc) > 28:
                        desc = desc[0:28]
    
                    if type(egu) == float:
                        egu = ""
                    else:
                        egu = re.sub(r"[^A-Za-z0-9/% ]+", "", egu)
    
                    if scan not in SCAN_VALUES:
                        logger.error(
                            'Invalid scan value "{}" defined for pv "{}".'.format(scan, name)
                        )
                        continue
    
                    if not tag or type(tag) != str or tag == "" or tag == "N/A":
                        logger.warning(
                            "Tag not set! {}. EPICS record won't be generated.".format(name)
                        )
                        continue
    
                    if tag not in tags:
                        tags[tag] = [name]
                    else:
                        tags[tag].append(name)
    
                    # Concatenate dtype and inout information.
                    #     Ex: dype='Analog', inout='Ouput' =>
                    #         full_type = 'Analog Output'
                    #     If inout has no value, full_type = dtype
                    full_type = dtype
                    if inout != '' and not inout.startswith("-") and inout.lower != 'n/a':
                        full_type = dtype + ' ' + inout
    
                    if full_type in args.bi:
                        f.write(
                            bi_template.safe_substitute(
                                name=name,
                                tag=tag,
                                desc=desc,
                                scan=scan,
                                onam=onam,
                                znam=znam,
                                zsv=zsv,
                                osv=osv,
                            )
                        )
                    elif full_type in args.bo:
                        f.write(
                            bo_template.safe_substitute(
                                name=name,
                                tag=tag,
                                desc=desc,
                                scan=scan,
                                onam=onam,
                                znam=znam,
                                zsv=zsv,
                                osv=osv,
                            )
                        )
                    elif full_type in args.ai:
                        f.write(
                            ai_template.safe_substitute(
                                name=name,
                                tag=tag,
                                desc=desc,
                                scan=scan,
                                prec=str(prec),
                                egu=egu,
                                hopr=hopr,
                                lopr=lopr,
                                hihi=hihi,
                                high=high,
                                low=low,
                                lolo=lolo,
                                hhsv=hhsv,
                                hsv=hsv,
                                lsv=lsv,
                                llsv=llsv,
                                hyst=hyst,
                            )
                        )
                    elif full_type in args.ao:
                        f.write(
                            ao_template.safe_substitute(
                                name=name,
                                tag=tag,
                                desc=desc,
                                scan=scan,
                                prec=str(prec),
                                egu=egu,
                                drvh=drvh,
                                drvl=drvl,
                                hopr=hopr,
                                lopr=lopr,
                                hihi=hihi,
                                high=high,
                                low=low,
                                lolo=lolo,
                                hhsv=hhsv,
                                hsv=hsv,
                                lsv=lsv,
                                llsv=llsv,
                                hyst=hyst,
                            )
                        )
                    elif full_type in args.lsi:
                        f.write(
                            lsi_template.safe_substitute(
                                name=name,
                                tag=tag,
                                desc=desc,
                                scan=scan,
                                sizv=sizv,
                            )
                        )
                    elif full_type in args.lso:
                        f.write(
                            lso_template.safe_substitute(
                                name=name,
                                tag=tag,
                                desc=desc,
                                scan=scan,
                                sizv=sizv,
                            )
                        )
                    else:
                        logger.warning('Invalid Type "{}".'.format(full_type + " for " + name))
    
                for tag, vals in tags.items():
                    if len(vals) > 1:
                        logger.warning('Tag "{}" already exists {}.'.format(tag, tags[tag]))


if __name__ == "__main__":
    config_logger(logger)
    args = get_args()
    status = generate_all(args)
