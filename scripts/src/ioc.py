import pandas
import logging
import os
import re
import typing
import copy

from .templates.interlock_rf import (
    cmd_template,
    ai_template,
    ao_template,
    bi_template,
    bo_template,
    calcout_template_field,
    ao_template_closed_loop,
    calcout_generic_template,
    bi_soft_channel_template,
    bo_soft_channel_template,
)
from .consts import SCAN_VALUES

logger = logging.getLogger()

# Global variables

list_tags_32bit_for_bool = []

#########################

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
        bo_high,
        main_conv,
        lower_conv,
        upper_conv,
    ):
        self.name = name
        self.desc = desc
        self.tag = tag
        self.inout = inout
        self.dtype = dtype
        self.egu = egu
        self.scan = scan
        self.prec = prec
        self.bo_high = bo_high
        self.main_conv = main_conv
        self.lower_conv = lower_conv
        self.upper_conv = upper_conv

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
        self.bo_high = row[cols.bo_high]
        self.main_conv = row[cols.main_conv]
        self.lower_conv = row[cols.lower_conv]
        self.upper_conv = row[cols.upper_conv]

        if type(self.prec) != str:
            self.prec = str(self.prec)

        if type(self.bo_high) != str:
            self.bo_high = str(self.bo_high)

        self.main_conv = self.main_conv.replace(' ','').replace('\t','')
        self.main_conv = self.main_conv.replace('\n','').replace('\r','')
        self.main_conv = self.main_conv.replace('pv','A').replace('**','^')
        if self.main_conv == "":
            self.main_conv = "A"

        self.lower_conv = self.lower_conv.replace(' ','').replace('\t','')
        self.lower_conv = self.lower_conv.replace('\n','').replace('\r','')
        self.lower_conv = self.lower_conv.replace('pv','A').replace('**','^')
        if self.lower_conv == "":
            self.lower_conv = "A"

        self.upper_conv = self.upper_conv.replace(' ','').replace('\t','')
        self.upper_conv = self.upper_conv.replace('\n','').replace('\r','')
        self.upper_conv = self.upper_conv.replace('pv','A').replace('**','^')
        if self.upper_conv == "":
            self.upper_conv = "A"

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
    filename = (
        os.path.join(base_path, "../ioc/iocBoot/iocetheripIOC/") + ioc_name + ".cmd"
    )
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
            high=data.bo_high,
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

def generate_ao_record(data: RowData, file):
    file.write(
        ao_template.safe_substitute(
            desc=data.desc,
            egu=data.egu,
            name=data.name,
            prec=data.prec,
            scan=data.scan,
            tag=data.tag,
        )
    )

def generate_bi_from_bit(input_pv, shift_str, data: RowData, file):
    aux_calc_name = data.name
    aux_calc_name = aux_calc_name.replace('-SP', '')
    aux_calc_name = aux_calc_name.replace('-Sel', '')
    aux_calc_name = aux_calc_name.replace('-RB', '')
    aux_calc_name = aux_calc_name.replace('-Sts', '')
    aux_calc_name = aux_calc_name.replace('-Cmd', '')
    aux_calc_name = aux_calc_name.replace('-Mon', '')
    aux_calc_name = aux_calc_name + 'Calc'
    calc_desc = "Aux calc for " + data.name
    file.write(
        calcout_generic_template.safe_substitute(
            name=aux_calc_name,
            desc=calc_desc[0:40],
            scan = data.scan + " second",
            inpa=input_pv + " NPP",
            calc="1 & (A >> " + shift_str + ")",
            out=data.name + " PP",
            inpb="",
            inpc="",
            inpd="",
            inpe="",
            inpf="",
            inpg="",
            inph="",
            inpi="",
            inpj="",
            inpk="",
            inpl="",
            flnk="",
            egu="",
            prec="",
        )
    )
    file.write(
        bi_soft_channel_template.safe_substitute(
            desc=data.desc,
            name=data.name,
            onam="True",
            scan="Passive",
            inp=aux_calc_name,
            inp_type="NPP",
            znam="False",
        )
    )

def generate_bo_from_bit(output_pv, shift_str, data: RowData, file):
    aux_calc_name = data.name
    aux_calc_name = aux_calc_name.replace('-SP', '')
    aux_calc_name = aux_calc_name.replace('-Sel', '')
    aux_calc_name = aux_calc_name.replace('-RB', '')
    aux_calc_name = aux_calc_name.replace('-Sts', '')
    aux_calc_name = aux_calc_name.replace('-Cmd', '')
    aux_calc_name = aux_calc_name.replace('-Mon', '')
    aux_calc_name = aux_calc_name + 'Calc'
    file.write(
        bo_soft_channel_template.safe_substitute(
            desc=data.desc,
            name=data.name,
            onam="True",
            scan="Passive",
            out=aux_calc_name + ".PROC",
            out_type="PP",
            znam="False",
            high=data.bo_high,
        )
    )
    calc_desc = "Aux calc for " + data.name
    file.write(
        calcout_generic_template.safe_substitute(
            name=aux_calc_name,
            desc=calc_desc[0:40],
            scan="Passive",
            inpa=data.name + " NPP",
            inpb=output_pv + " NPP",
            calc="C:=1<<"+shift_str+";((~(B&C))&B)+(A<<"+shift_str+")",
            out=output_pv + " PP",
            inpc="",
            inpd="",
            inpe="",
            inpf="",
            inpg="",
            inph="",
            inpi="",
            inpj="",
            inpk="",
            inpl="",
            flnk="",
            egu="",
            prec="",
        )
    )

def has_bit_notation(tag_name):
    dot_idx = tag_name.rfind('.')
    return (dot_idx > -1 and dot_idx < len(tag_name)-1
            and tag_name[dot_idx+1:].isdecimal()
            )

def split_bit_notation(tag_name):
    dot_idx = tag_name.rfind('.')
    return (tag_name[:dot_idx], tag_name[dot_idx+1:])

def generate_by_record_type(data: RowData, file):
    if data.dtype == "Digital":
        # treat the case when bit from tag is specified
        if has_bit_notation(data.tag):
            tag_str, shift_str = split_bit_notation(data.tag)
            data_32bit_tag = copy.copy(data)
            data_32bit_tag_name = tag_str
            data_32bit_tag_name = (
                    data_32bit_tag_name.replace(
                        '[','_'
                        ).replace(
                        ']','_'
                        ).replace(
                        '.',''
                        ).replace(
                        ':',''
                        ) + '_32bit'
                )
            data_32bit_tag.name = data_32bit_tag_name
            data_32bit_tag.tag = tag_str
            data_32bit_tag.scan = ".1"
            data_32bit_tag.desc = '32bit PV for tag ' + tag_str
            if not data_32bit_tag.tag in list_tags_32bit_for_bool:
                list_tags_32bit_for_bool.append(data_32bit_tag.tag)
                generate_ao_record(data_32bit_tag, file)
            if data.inout == "Input" or data.inout == "Output":
                generate_bi_from_bit(
                    data_32bit_tag.name, shift_str, data, file
                )
            elif data.inout == "Control":
                generate_bo_from_bit(
                    data_32bit_tag.name, shift_str, data, file
                )
        # other cases
        elif data.inout == "Input" or data.inout == "Output":
            generate_bi_record(data, file)
        elif data.inout == "Control":
            generate_bo_record(data, file)
        else:
            raise ValueError('Invalid Type "{}".'.format(data.inout + "  " + data.name))

    elif data.dtype == "Analog":
        if data.inout == "Input":
            if data.main_conv == "A":
                generate_ai_record(data, file)
            else:
                data_copy = copy.copy(data)
                data_copy.name = remove_pv_suffix(data.name) + 'Raw'
                data_copy.desc = "Raw " + data.desc
                data_copy.desc = data.desc[0:40]
                generate_ai_record(data_copy, file)
                generate_conv_calc(
                    file, name=data.name, inp=data_copy.name,
                    calc=data.main_conv, prec=data.prec,
                    egu=data.egu, desc=data.desc
                )
        else:
            raise ValueError("Type Analog Out Not - Supported {}.".format(data.name))
    else:
        raise ValueError("Unknown data type {} at {}".format(data.dtype, data.name))


def rows_from_sheets_generator(spreadsheet_path, sheet_names):
    for sheet_name in sheet_names:
        sheet = pandas.read_excel(spreadsheet_path, sheet_name=sheet_name, dtype=str, engine="openpyxl")
        replace_info = {"\n": ""}
        sheet.replace(replace_info, inplace=True, regex=True)
        sheet.fillna("", inplace=True)
        for _, row in sheet.iterrows():
            yield row, sheet_name


def make_pv_from_tag(tag):
    return "$(P):{}".format(re.sub(r"[^A-Za-z0-9]+", "_", tag))


def generate_tag_record(f, tag_pv, tag):
    f.write(
        ai_template.safe_substitute(
            name=tag_pv,
            tag=tag,
            desc=tag,
            egu="",
            prec="4",
            scan="5",
        )
    )

def generate_conv_calc(f, name, inp, calc, prec, egu, out="", desc=""):
    f.write(
        calcout_generic_template.safe_substitute(
            name=name,
            desc=desc,
            scan="Passive",
            inpa=inp+" CP",
            calc=calc,
            egu=egu,
            prec=prec,
            out=out,
            inpb="",
            inpc="",
            inpd="",
            inpe="",
            inpf="",
            inpg="",
            inph="",
            inpi="",
            inpj="",
            inpk="",
            inpl="",
            flnk="",
        )
    )

def generate_tag_intermediate_record(f, name, tag_pv, prec, egu):
    f.write(
        ao_template_closed_loop.safe_substitute(
            name=name,
            name_in=tag_pv,
            desc="Upper limits from PLC",
            egu=egu,
            prec=prec,
        )
    )


def generate_tag_field_record(
    f,
    target_name,
    target_field,
    name_in,
    offset,
):
    f.write(
        calcout_template_field.safe_substitute(
            name=target_name + "_" + target_field,
            name_clp=name_in,
            name_target=target_name,
            offset=offset,
            field=target_field,
        )
    )

def remove_pv_suffix(pv_name):
    pv_name = pv_name.replace('-SP','')
    pv_name = pv_name.replace('-RB','')
    pv_name = pv_name.replace('-Sel','')
    pv_name = pv_name.replace('-Sts','')
    pv_name = pv_name.replace('-Cmd','')
    pv_name = pv_name.replace('-Mon','')
    pv_name = pv_name.replace('-Cte','')
    return pv_name

def generate_tag_set(
    generated_tags,
    f,
    tag,
    name,
    calc,
    prec,
    egu,
    lim_pv,
    major_name,
    major_offset,
    minor_name,
    minor_offset,
):
    tag_pv = make_pv_from_tag(tag)
    if tag not in generated_tags:
        generate_tag_record(f, tag_pv, tag)
        generated_tags.add(tag)

    generate_conv_calc(
            f, name=lim_pv, inp=tag_pv, calc=calc,
            prec=prec, egu=egu, desc="Upper limits from PLC"
            )

    #intermediate_pv = remove_pv_suffix(lim_pv)+'Calc'
    #generate_tag_intermediate_record(
    #        f, name=intermediate_pv,
    #        tag_pv=lim_pv, prec=prec, egu=egu
    #        )
    generate_tag_field_record(
        f,
        target_name=name,
        target_field=major_name,
        name_in=lim_pv,
        offset=major_offset,
    )
    generate_tag_field_record(
        f,
        target_name=name,
        target_field=minor_name,
        name_in=lim_pv,
        offset=minor_offset,
    )


def generate_limit_records(limit_tags: Limits, f):
    generated_tags = set()
    for tag, row in limit_tags.upper_tags_items():
        generate_tag_set(
            generated_tags,
            f,
            tag,
            name=row.name,
            calc=row.upper_conv,
            prec=row.prec,
            egu=row.egu,
            lim_pv=row.upper_lim_pv,
            major_name="HIHI",
            major_offset="-0.5",
            minor_name="HIGH",
            minor_offset="-1.0",
        )
    for tag, row in limit_tags.lower_tags_items():
        generate_tag_set(
            generated_tags,
            f=f,
            tag=tag,
            name=row.name,
            calc=row.lower_conv,
            prec=row.prec,
            egu=row.egu,
            lim_pv=row.lower_lim_pv,
            major_name="LOLO",
            major_offset="+0.5",
            minor_name="LOW",
            minor_offset="+1.0",
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


def get_database_path(base_path, name):
    return os.path.join(base_path, "../ioc/database/") + name + ".db"


def generate_db_file(
    base_path, spreadsheet_path, ioc_name, sheet_names, column_names: ColumnNames
):

    IOC_DATABASE_PATH = get_database_path(base_path, ioc_name)
    IOC_LIMITS_DATABASE_PATH = get_database_path(base_path, ioc_name + "-Limits")

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

    logger.info('Generating "{}" file.'.format(IOC_LIMITS_DATABASE_PATH))
    with open(IOC_LIMITS_DATABASE_PATH, "w+") as f:
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
        bo_high=args.col_bo_high,
        main_conv=args.col_main_conv,
        lower_conv=args.col_lower_conv,
        upper_conv=args.col_upper_conv,
    )

    generate_db_file(
        base_path=base_path,
        spreadsheet_path=spreadsheet_path,
        ioc_name=ioc_name,
        sheet_names=sheet_names,
        column_names=column_names,
    )
