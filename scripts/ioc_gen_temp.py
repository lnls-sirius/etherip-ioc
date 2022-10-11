#!/usr/bin/env python3

import argparse
import logging
import os

from src.consts import SCAN_VALUES
from src.sirius_temp_iocs import generate

logger = logging.getLogger()

def config_logger(logger):
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
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
        "--arch",
        choices=["linux-x86_64", "linux-arm"],
        default="linux-x86_64",
        help="System architecture.",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    config_logger(logger)
    base_path = os.path.dirname(os.path.abspath(__file__))
    generate(get_args(), base_path)