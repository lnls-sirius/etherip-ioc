#!/usr/bin/env python3
import argparse
import pandas
import logging
import os
import re
import typing

from .templates import (
    cmd_template,
    ai_template,
    bi_template,
    bo_template,
    calcout_template_field,
)
from .consts import SCAN_VALUES

logger = logging.getLogger()


class ColumnNames:
    def __init__(
        self,
        name,
        desc,
        tag,
        inout,
        dtype,
        egu,
        scan,
        prec,
    ):
        self.name = name
        self.desc = desc
        self.tag = tag
        self.inout = inout
        self.dtype = dtype
        self.egu = egu
        self.scan = scan
        self.prec = prec

        self.upperLimitTag = "Upper Limit"
        self.lowerLimitTag = "Lower Limit"
        self.upperLimitPV = "UPPER LIMIT PV NAME"
        self.lowerLimitPV = "LOWER LIMIT PV NAME"


class RowData:
    def __init__(self, row, cols: ColumnNames):
        self.name = row[cols.name]
        self.desc = row[cols.desc]
        self.tag = row[cols.tag]
        self.inout = row[cols.inout]
        self.dtype = row[cols.dtype]
        self.egu = row[cols.egu]
        self.scan = row[cols.scan]
        self.prec = row[cols.prec]

        if type(self.prec) != str:
            self.prec = str(self.prec)

        if not self.name or self.name.startswith("-"):
            raise ValueError("Wrong name format {} tag {}".format(self.name, self.tag))

        if len(self.desc) > 28:
            self.desc = self.desc[0:28]

        if self.scan not in SCAN_VALUES:
            raise ValueError(
                'Invalid scan value "{}" defined for name "{}".'.format(
                    self.scan, self.name
                )
            )

        # Filter invalid EGU character
        self.egu = (
            "" if type(self.egu) == float else re.sub(r"[^A-Za-z0-9 ]+", "", self.egu)
        )

        if not self.tag or type(self.tag) != str or self.tag == "" or self.tag == "N/A":
            raise ValueError("Invalid tag for record {}".format(self.name))

        self.lower_lim_tag = row[cols.lowerLimitTag]
        self.upper_lim_tag = row[cols.upperLimitTag]

        self.lower_lim_pv = row[cols.lowerLimitPV]
        self.upper_lim_pv = row[cols.upperLimitPV]


class Limits:
    def __init__(self):
        self.lower_tags = {}
        self.upper_tags = {}

    def add_row(self, row: RowData):
        count = 0
        if row.upper_lim_tag != "":
            if row.upper_lim_tag not in self.upper_tags:
                self.upper_tags[row.upper_lim_tag] = []
            self.upper_tags[row.upper_lim_tag].append(row)
            count += 1

        if row.lower_lim_tag != "":
            if row.lower_lim_tag not in self.lower_tags:
                self.lower_tags[row.lower_lim_tag] = []
            self.lower_tags[row.lower_lim_tag].append(row)
            count += 1

        return count

    def upper_tags_items(
        self,
    ) -> typing.Generator[typing.Tuple[int, RowData], None, None]:
        for k, v in self.upper_tags.items():
            for i in v:
                yield k, i

    def lower_tags_items(
        self,
    ) -> typing.Generator[typing.Tuple[int, RowData], None, None]:
        for k, v in self.lower_tags.items():
            for i in v:
                yield k, i


def generate_cmd_file(base_path, arch, ioc_name, plc_module, plc_name):
    filename = os.path.join(base_path, "../iocBoot/iocetheripIOC/") + ioc_name + ".cmd"
    logger.info('Generating "{}.cmd" file at "{}".'.format(ioc_name, filename))
    with open(filename, "w+") as f:
        f.write(
            cmd_template.safe_substitute(
                arch=arch,
                database=ioc_name,
                module=plc_module,
                plc=plc_name,
            )
        )


def generate_bi_record(data: RowData, file):
    file.write(
        bi_template.safe_substitute(
            desc=data.desc,
            name=data.name,
            onam="True",
            scan=data.scan,
            tag=data.tag,
            znam="False",
        )
    )


def generate_bo_record(data: RowData, file):
    file.write(
        bo_template.safe_substitute(
            desc=data.desc,
            name=data.name,
            onam="True",
            scan=data.scan,
            tag=data.tag,
            znam="False",
        )
    )


def generate_ai_record(data: RowData, file):
    file.write(
        ai_template.safe_substitute(
            desc=data.desc,
            egu=data.egu,
            name=data.name,
            prec=data.prec,
            scan=data.scan,
            tag=data.tag,
        )
    )


def generate_by_record_type(data: RowData, file):
    if data.dtype == "Digital":
        if data.inout == "Input" or data.inout == "Output":
            generate_bi_record(data, file)
        elif data.inout == "Control":
            generate_bo_record(data, file)
        else:
            raise ValueError('Invalid Type "{}".'.format(data.inout + "  " + data.name))

    elif data.dtype == "Analog":
        if data.inout == "Input":
            generate_ai_record(data, file)
        else:
            raise ValueError("Type Analog Out Not - Supported {}.".format(data.name))
    else:
        raise ValueError("Unknown data type {} at {}".format(data.dtype, data.name))


def rows_from_sheets_generator(spreadsheet_path, sheet_names):
    for sheet_name in sheet_names:
        sheet = pandas.read_excel(spreadsheet_path, sheet_name=sheet_name, dtype=str)
        replace_info = {"\n": ""}
        sheet.replace(replace_info, inplace=True, regex=True)
        sheet.fillna("", inplace=True)
        for _, row in sheet.iterrows():
            yield row, sheet_name


def generate_limit_records(limit_tags: Limits, f):

    for _, row in limit_tags.upper_tags_items():
        from_clp_record = ai_template.safe_substitute(
            name=row.upper_lim_pv,
            tag=row.upper_lim_tag,
            desc="Upper limits from PLC",
            egu=row.egu,
            prec=row.prec,
            scan="1",
        )
        f.write(from_clp_record)
        f.write(
            calcout_template_field.safe_substitute(
                name=row.upper_lim_pv + "_hihi",
                name_clp=row.upper_lim_pv,
                name_target=row.name,
                offset="-0.5",
                field="HIHI",
            )
        )
        f.write(
            calcout_template_field.safe_substitute(
                name=row.upper_lim_pv + "_high",
                name_clp=row.upper_lim_pv,
                name_target=row.name,
                offset="-1.0",
                field="HIGH",
            )
        )

    for _, row in limit_tags.lower_tags_items():
        from_clp_record = ai_template.safe_substitute(
            name=row.lower_lim_pv,
            tag=row.lower_lim_tag,
            desc="Upper limits from PLC",
            egu=row.egu,
            prec=row.prec,
            scan="1",
        )
        f.write(from_clp_record)
        f.write(
            calcout_template_field.safe_substitute(
                name=row.lower_lim_pv + "_low",
                name_clp=row.lower_lim_pv,
                name_target=row.name,
                offset="+0.5",
                field="LOW",
            )
        )
        f.write(
            calcout_template_field.safe_substitute(
                name=row.lower_lim_pv + "_lolo",
                name_clp=row.lower_lim_pv,
                name_target=row.name,
                offset="+1.0",
                field="LOLO",
            )
        )


def generate_records_from_row(
    row, sheet_name, file, column_names: ColumnNames, tags, limit_tags: Limits
):
    try:
        data = RowData(row, column_names)

        if data.tag not in tags:
            tags[data.tag] = [data.name]
        else:
            tags[data.tag].append(data.name)

        generate_by_record_type(data, file)

        limit_tags.add_row(data)

    except ValueError as e:
        logger.error("Record Generation [{}]: {}".format(sheet_name, e))

    for tag, vals in tags.items():
        if len(vals) > 1:
            logger.error('Tag "{}" already exists {}.'.format(tag, tags[tag]))


def generate_db_file(
    base_path, spreadsheet_path, ioc_name, sheet_names, column_names: ColumnNames
):
    IOC_DATABASE_PATH = os.path.join(base_path, "../database/") + ioc_name + ".db"
    tags = {}
    logger.info('Generating "{}.db" file at "{}".'.format(ioc_name, IOC_DATABASE_PATH))

    limits = Limits()

    with open(IOC_DATABASE_PATH, "w+") as f:
        for row, sheet_name in rows_from_sheets_generator(
            spreadsheet_path=spreadsheet_path, sheet_names=sheet_names
        ):
            generate_records_from_row(
                row=row,
                sheet_name=sheet_name,
                column_names=column_names,
                file=f,
                tags=tags,
                limit_tags=limits,
            )
        generate_limit_records(limits, f)


def generate(args, base_path):
    logger.info("Args, {}.".format(vars(args)))

    arch = args.arch
    base_path = base_path
    ioc_name = args.ioc_name
    plc_module = args.plc_module
    plc_name = args.plc_name
    sheet_names = args.sheet.split(",")
    spreadsheet_path = args.spreadsheet

    generate_cmd_file(
        base_path=base_path,
        arch=arch,
        ioc_name=ioc_name,
        plc_module=plc_module,
        plc_name=plc_name,
    )

    column_names = ColumnNames(
        name=args.col_pv,
        desc=args.col_desc,
        tag=args.col_tag,
        inout=args.col_inout,
        dtype=args.col_dtype,
        egu=args.col_egu,
        scan=args.col_scan,
        prec=args.col_prec,
    )

    generate_db_file(
        base_path=base_path,
        spreadsheet_path=spreadsheet_path,
        ioc_name=ioc_name,
        sheet_names=sheet_names,
        column_names=column_names,
    )
