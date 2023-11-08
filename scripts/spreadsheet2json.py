import argparse
import pandas
import logging
import os
import re
import typing
import copy

from src.templates.json_dicts import (
    tag_dict_template,
    calc_dict_template,
    conv_dict_template,
    var_dict_template,
)

logger = logging.getLogger()

#########################

def config_logger(logger):
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def get_args():
    parser = argparse.ArgumentParser(
        description="""Generate JSON specification file from spreadsheet.\n"""
    )
    parser.add_argument("--filename", required=True, help="JSON file name.")
    parser.add_argument("--spreadsheet", required=True, help="Excel spreadsheet location.")
    parser.add_argument("--sheet", required=True, help="Sheet names.")
    parser.add_argument("--col-main-pv", required=True, help="Main PV column name.")
    parser.add_argument("--col-desc", required=True, help="Desc column name.")
    parser.add_argument("--col-data-type", required=True, help="Data type column name.")
    parser.add_argument("--col-egu", required=True, help="EPICS egu column name.")
    parser.add_argument("--col-inout", required=True, help="Input/Output column name.")
    parser.add_argument("--col-prec", required=True, help="EPICS scan time.")
    parser.add_argument("--col-scan", required=True, help="EPICS scan time.")
    parser.add_argument("--col-tag", required=True, help="Desc column name.")
    parser.add_argument("--col-cmd-time", required=True, help="Time before the boolean returns to zero.")
    parser.add_argument("--col-lo-conv", required=True, help="Conversion calc to apply to tag low limit value.")
    parser.add_argument("--col-hi-conv", required=True, help="Conversion calc to apply to tag high limit value.")
    parser.add_argument("--col-lolo-conv", required=True, help="Conversion calc to apply to tag low low limit value.")
    parser.add_argument("--col-hihi-conv", required=True, help="Conversion calc to apply to tag high high limit value.")
    parser.add_argument("--col-upper-limit-tag", required=True, help="Tag for upper limit.")
    parser.add_argument("--col-lower-limit-tag", required=True, help="Tag for lower limit.")
    parser.add_argument("--col-upper-limit-pv", required=True, help="PV for upper limit.")
    parser.add_argument("--col-lower-limit-pv", required=True, help="PV for lower limit.")
    parser.add_argument("--col-val", required=True, help="PV initial value.")
    args = parser.parse_args()
    return args

class ColumnNames:
    def __init__(
        self,
        main_pv,
        desc,
        tag,
        inout,
        data_type,
        egu,
        scan,
        prec,
        cmd_time,
        lo_conv,
        hi_conv,
        lolo_conv,
        hihi_conv,
        upper_limit_tag,
        lower_limit_tag,
        upper_limit_pv,
        lower_limit_pv,
        val,
    ):
        self.main_pv = main_pv
        self.desc = desc
        self.tag = tag
        self.inout = inout
        self.data_type = data_type
        self.egu = egu
        self.scan = scan
        self.prec = prec
        self.cmd_time = cmd_time
        self.lo_conv = lo_conv
        self.hi_conv = hi_conv
        self.lolo_conv = lolo_conv
        self.hihi_conv = hihi_conv
        self.upper_limit_tag = upper_limit_tag
        self.lower_limit_tag = lower_limit_tag
        self.upper_limit_pv = upper_limit_pv
        self.lower_limit_pv = lower_limit_pv
        self.val = val


class RowData:
    def __init__(self, row, cols: ColumnNames):
        self.main_pv = str(row.get(cols.main_pv, "")).strip()
        self.desc = str(row.get(cols.desc, "")).strip()
        self.tag = str(row.get(cols.tag, "")).strip()
        self.inout = str(row.get(cols.inout, "")).strip()
        self.data_type = str(row.get(cols.data_type, "")).strip()
        self.egu = str(row.get(cols.egu, "")).strip()
        self.scan = str(row.get(cols.scan, "")).strip()
        self.prec = str(row.get(cols.prec, "")).strip()
        self.cmd_time = str(row.get(cols.cmd_time, "")).strip()
        self.lo_conv = str(row.get(cols.lo_conv, "")).strip()
        self.hi_conv = str(row.get(cols.hi_conv, "")).strip()
        self.lolo_conv = str(row.get(cols.lolo_conv, "")).strip()
        self.hihi_conv = str(row.get(cols.hihi_conv, "")).strip()
        self.upper_limit_tag = str(row.get(cols.upper_limit_tag, "")).strip()
        self.lower_limit_tag = str(row.get(cols.lower_limit_tag, "")).strip()
        self.upper_limit_pv = str(row.get(cols.upper_limit_pv, "")).strip()
        self.lower_limit_pv = str(row.get(cols.lower_limit_pv, "")).strip()
        self.val = str(row.get(cols.val, "")).strip()
        self.hsv = ""
        self.hhsv = ""
        self.lsv = ""
        self.llsv = ""

        # post process tag name
        if self.tag == "N/A":
            self.tag = ""

        # post process upper limit pv name
        if self.upper_limit_pv == "N/A":
            self.upper_limit_pv = ""

        # post process lower limit pv name
        if self.lower_limit_pv == "N/A":
            self.lower_limit_pv = ""

        # assign high severity and high high severity for limits
        if self.upper_limit_pv != "":
            self.hsv = "minor"
            self.hhsv = "major"

        # assign low severity and low low severity for limits
        if self.lower_limit_pv != "":
            self.lsv = "minor"
            self.llsv = "major"


def remove_pv_suffix(pv_name):
    pv_name = pv_name.replace('-SP','')
    pv_name = pv_name.replace('-RB','')
    pv_name = pv_name.replace('-Sel','')
    pv_name = pv_name.replace('-Sts','')
    pv_name = pv_name.replace('-Cmd','')
    pv_name = pv_name.replace('-Mon','')
    pv_name = pv_name.replace('-Cte','')
    return pv_name


def rows_from_sheets_generator(spreadsheet_path, sheet_names):
    for sheet_name in sheet_names:
        sheet = pandas.read_excel(spreadsheet_path, sheet_name=sheet_name, dtype=str, engine="openpyxl")
        replace_info = {"\n": ""}
        sheet.replace(replace_info, inplace=True, regex=True)
        sheet.fillna("", inplace=True)
        for _, row in sheet.iterrows():
            yield row, sheet_name


def generate_dicts_from_row(
    row, sheet_name, file_handler, column_names: ColumnNames):
    try:
        data = RowData(row, column_names)
        if data.tag == "":
            file_handler.write(
                var_dict_template.safe_substitute(
                    desc=data.desc,
                    name=data.main_pv,
                    data_type=data.data_type,
                    egu=data.egu,
                    prec=data.prec,
                    val=data.val,
                    )
                )
        if data.tag != "":
            file_handler.write(
                tag_dict_template.safe_substitute(
                    desc=data.desc,
                    name=data.main_pv,
                    data_type=data.data_type,
                    inout=data.inout,
                    cmdtime=data.cmd_time,
                    tag=data.tag,
                    egu=data.egu,
                    scan=data.scan,
                    prec=data.prec,
                    hsv=data.hsv,
                    hhsv=data.hhsv,
                    lsv=data.lsv,
                    llsv=data.llsv,
                    )
                )
        if data.upper_limit_pv != "":
            file_handler.write(
                tag_dict_template.safe_substitute(
                    desc=data.desc,
                    name=data.upper_limit_pv,
                    data_type=data.data_type,
                    inout="read",
                    cmdtime="",
                    tag=data.upper_limit_tag,
                    egu=data.egu,
                    scan="5",
                    prec=data.prec,
                    hsv="",
                    hhsv="",
                    lsv="",
                    llsv="",
                    )
                )
            file_handler.write(
                calc_dict_template.safe_substitute(
                    desc=data.desc,
                    name=remove_pv_suffix(data.upper_limit_pv)+'HIGH-Cte',
                    inp=data.upper_limit_pv,
                    out=data.main_pv+'.HIGH',
                    egu=data.egu,
                    prec=data.prec,
                    conv=data.hi_conv,
                    )
                )
            file_handler.write(
                calc_dict_template.safe_substitute(
                    desc=data.desc,
                    name=remove_pv_suffix(data.upper_limit_pv)+'HIHI-Cte',
                    inp=data.upper_limit_pv,
                    out=data.main_pv+'.HIHI',
                    egu=data.egu,
                    prec=data.prec,
                    conv=data.hihi_conv,
                    )
                )
        if data.lower_limit_pv != "":
            file_handler.write(
                tag_dict_template.safe_substitute(
                    desc=data.desc,
                    name=data.lower_limit_pv,
                    data_type=data.data_type,
                    inout="read",
                    cmdtime="",
                    tag=data.lower_limit_tag,
                    egu=data.egu,
                    scan="5",
                    prec=data.prec,
                    hsv="",
                    hhsv="",
                    lsv="",
                    llsv="",
                    )
                )
            file_handler.write(
                calc_dict_template.safe_substitute(
                    desc=data.desc,
                    name=remove_pv_suffix(data.lower_limit_pv)+'LOW-Cte',
                    inp=data.lower_limit_pv,
                    out=data.main_pv+'.LOW',
                    egu=data.egu,
                    prec=data.prec,
                    conv=data.lo_conv,
                    )
                )
            file_handler.write(
                calc_dict_template.safe_substitute(
                    desc=data.desc,
                    name=remove_pv_suffix(data.lower_limit_pv)+'LOLO-Cte',
                    inp=data.lower_limit_pv,
                    out=data.main_pv+'.LOLO',
                    egu=data.egu,
                    prec=data.prec,
                    conv=data.lolo_conv,
                    )
                )
    except Exception as e:
        logger.error("JSON Generation [{}]: {}".format(sheet_name, e))


def generate_json_file(
    filename, spreadsheet_path, sheet_names, column_names: ColumnNames):

    file_path = filename

    logger.info('Generating "{}"'.format(file_path))

    with open(file_path, "w+") as f:
        f.write("[\n")
    with open(file_path, "a") as f:
        for row, sheet_name in rows_from_sheets_generator(
            spreadsheet_path=spreadsheet_path, sheet_names=sheet_names
        ):
            generate_dicts_from_row(
                row=row,
                sheet_name=sheet_name,
                file_handler=f,
                column_names=column_names,
            )
    with open(file_path, "a") as f:
        f.write("\n]")

def generate(args):
    logger.info("Args, {}.".format(vars(args)))

    filename = args.filename
    sheet_names = args.sheet.split(",")
    spreadsheet_path = args.spreadsheet

    column_names = ColumnNames(
        main_pv=args.col_main_pv,
        desc=args.col_desc,
        tag=args.col_tag,
        inout=args.col_inout,
        data_type=args.col_data_type,
        egu=args.col_egu,
        scan=args.col_scan,
        prec=args.col_prec,
        cmd_time=args.col_cmd_time,
        lo_conv=args.col_lo_conv,
        lolo_conv=args.col_lolo_conv,
        hi_conv=args.col_hi_conv,
        hihi_conv=args.col_hihi_conv,
        upper_limit_tag=args.col_upper_limit_tag,
        lower_limit_tag=args.col_lower_limit_tag,
        upper_limit_pv=args.col_upper_limit_pv,
        lower_limit_pv=args.col_lower_limit_pv,
        val=args.col_val,
    )

    generate_json_file(
        filename=filename,
        spreadsheet_path=spreadsheet_path,
        sheet_names=sheet_names,
        column_names=column_names,
    )

if __name__ == "__main__":
    config_logger(logger)
    generate(get_args())

