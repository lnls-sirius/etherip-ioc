#!/usr/bin/env python3

import argparse
import logging
import os

from src.consts import SCAN_VALUES
from src.ioc_new import generate

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
    parser.add_argument("--json", required=True, help="JSON files with specification.")
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
    parser.add_argument("--ioc-name", required=True, help="IOC name.")
    parser.add_argument("--spreadsheet", required=False, default="", help="Excel spreadsheet location.")
    parser.add_argument("--sheet", required=False, default="", help="Sheet name.")
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
