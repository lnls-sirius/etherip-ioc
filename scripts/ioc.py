#!/usr/bin/env python3
import argparse
import pandas
import logging
import os
import re
from templates import cmd_template, ai_template, bi_template, bo_template

logger = logging.getLogger()

SCAN_VALUES = [".1", ".2", ".5", "1", "2", "5", "10", "I/O Intr", "Event", "Passive"]
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


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
    parser.add_argument("--plc-ip", required=True, dest="plc_ip", help="PLC IP.")
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
        help="Modulus of the variables to be archived in PLC.",
    )

    parser.add_argument("--col-desc", default="Description", help="Desc column name.")
    parser.add_argument(
        "--col-dtype", default="Data Type", help="Data type column name."
    )
    parser.add_argument("--col-egu", default="EGU", help="EPICS egu column name.")
    parser.add_argument(
        "--col-inout", default="In/Out", help="Input/Output column name."
    )
    parser.add_argument("--col-prec", default="Prec", help="EPICS scan time.")
    parser.add_argument("--col-pv", default="NAME", help="PV column name.")
    parser.add_argument("--col-scan", default="Scan", help="EPICS scan time.")
    parser.add_argument("--col-tag", default="TAG", help="Desc column name.")
    parser.add_argument("--ioc-name", required=True, help="IOC name.")
    parser.add_argument("--sheet", required=True, help="Sheet name.")

    parser.add_argument(
        "--epics-ca-server-port",
        default=5064,
        help="EPICS_CA_SERVER_PORT value.",
        type=int,
    )
    parser.add_argument(
        "--epics-cas-intf-addr-list",
        default="127.0.0.1",
        help="EPICS_CAS_INTF_ADDR_LIST ip.",
    )
    parser.add_argument(
        "--arch",
        choices=["linux-x86_64", "linux-arm"],
        default="linux-x86_64",
        help="System architecture.",
    )

    args = parser.parse_args()
    return args


def generate(args):
    sheet_name = args.sheet.split(",")
    logger.info("Args, {}.".format(vars(args)))

    IOC_CMD_PATH = (
        os.path.join(BASE_PATH, "../iocBoot/iocetheripIOC/") + args.ioc_name + ".cmd"
    )
    IOC_DATABASE_PATH = os.path.join(BASE_PATH, "../database/") + args.ioc_name + ".db"

    logger.info('Generating "{}.cmd" file at "{}".'.format(args.ioc_name, IOC_CMD_PATH))

    with open(IOC_CMD_PATH, "w+") as f:
        f.write(
            cmd_template.safe_substitute(
                arch=args.arch,
                database=args.ioc_name,
                epics_ca_server_port=args.epics_ca_server_port,
                epics_cas_intf_addr_list=args.epics_cas_intf_addr_list,
                ip=args.plc_ip,
                module=args.plc_module,
                plc=args.plc_name,
            )
        )
    tags = {}
    logger.info(
        'Generating "{}.db" file at "{}".'.format(args.ioc_name, IOC_DATABASE_PATH)
    )
    with open(IOC_DATABASE_PATH, "w+") as f:
        for s_name in sheet_name:
            sheet = pandas.read_excel(args.spreadsheet, sheet_name=s_name, dtype=str)
            replace_info = {"\n": ""}
            sheet.replace(replace_info, inplace=True, regex=True)
            sheet.fillna("", inplace=True)
            for n, row in sheet.iterrows():
                name = row[args.col_pv]
                desc = row[args.col_desc]
                tag = row[args.col_tag]
                inout = row[args.col_inout]
                dtype = row[args.col_dtype]
                egu = row[args.col_egu]
                scan = row[args.col_scan]
                prec = row[args.col_prec]

                if not name or name.startswith("-"):
                    continue

                if len(desc) > 28:
                    desc = desc[0:28]

                # Filter invalid EGU character
                egu = "" if type(egu) == float else re.sub(r"[^A-Za-z0-9 ]+", "", egu)

                if scan not in SCAN_VALUES:
                    logger.error(
                        'Invalid scan value "{}" defined for name "{}".'.format(
                            scan, name
                        )
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

                if dtype == "Digital":
                    if inout == "Input" or inout == "Output":
                        f.write(
                            bi_template.safe_substitute(
                                desc=desc,
                                name=name,
                                onam="True",
                                scan=scan,
                                tag=tag,
                                znam="False",
                            )
                        )
                    elif inout == "Control":
                        f.write(
                            bo_template.safe_substitute(
                                desc=desc,
                                name=name,
                                onam="True",
                                scan=scan,
                                tag=tag,
                                znam="False",
                            )
                        )
                    else:
                        logger.warning('Invalid Type "{}".'.format(inout + "  " + name))

                elif dtype == "Analog":
                    if inout == "Input":
                        f.write(
                            ai_template.safe_substitute(
                                desc=desc,
                                egu=egu,
                                name=name,
                                prec=str(prec),
                                scan=scan,
                                tag=tag,
                            )
                        )
                    else:
                        logger.warning(
                            "Type Analog Out Not - Supported {}.".format(name)
                        )

            for tag, vals in tags.items():
                if len(vals) > 1:
                    logger.error('Tag "{}" already exists {}.'.format(tag, tags[tag]))


if __name__ == "__main__":
    config_logger(logger)
    args = get_args()
    generate(args)
