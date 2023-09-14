import json
import logging
import os
import sys
import re
import typing
import copy
#import pandas

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
    acalcout_generic_template,
    wfm_template
)
from .consts import SCAN_VALUES
from .consts import json_info

logger = logging.getLogger()

# Global variables

list_tags_32bit_for_bool = []

#########################

class KeyNames:
    def __init__(
        self,
        gen_type,
        name,
        desc,
        tag,
        inout,
        dtype,
        egu,
        scan,
        prec,
        inp,
        out,
        args,
        cmd_high,
        conv,
        val,
        hsv,
        hhsv,
        lsv,
        llsv,
    ):
        self.gen_type = gen_type
        self.name = name
        self.desc = desc
        self.tag = tag
        self.inout = inout
        self.dtype = dtype
        self.egu = egu
        self.scan = scan
        self.prec = prec
        self.inp = inp
        self.out = out
        self.args = args
        self.cmd_high = cmd_high
        self.conv = conv
        self.val = val
        self.hsv = hsv
        self.hhsv = hhsv
        self.lsv = lsv
        self.llsv = llsv

class RowData:
    def __init__(self, row, keys: KeyNames):
        self.gen_type = row.get(keys.gen_type, "")
        self.name = row.get(keys.name, "")
        self.desc = row.get(keys.desc, "")
        self.tag = row.get(keys.tag, "")
        self.inout = row.get(keys.inout, "")
        self.dtype = row.get(keys.dtype, "")
        self.egu = row.get(keys.egu, "")
        self.scan = row.get(keys.scan, "")
        self.prec = row.get(keys.prec, "")
        self.inp = row.get(keys.inp, "")
        self.out = row.get(keys.out, "")
        self.args = row.get(keys.args, "")
        self.cmd_high = row.get(keys.cmd_high, "")
        self.conv = row.get(keys.conv, "")
        self.val = row.get(keys.val, "")
        self.hsv = row.get(keys.hsv, "NO_ALARM")
        self.hhsv = row.get(keys.hhsv, "NO_ALARM")
        self.lsv = row.get(keys.lsv, "NO_ALARM")
        self.llsv = row.get(keys.llsv, "NO_ALARM")

        # convert alarm severity string to upper case
        self.hsv = self.hsv.upper()
        self.hhsv = self.hhsv.upper()
        self.lsv = self.lsv.upper()
        self.llsv = self.llsv.upper()

        if type(self.prec) != str:
            self.prec = str(self.prec)

        if type(self.cmd_high) != str:
            self.cmd_high = str(self.cmd_high)

        self.conv = self.conv.replace(' ','').replace('\t','')
        self.conv = self.conv.replace('\n','').replace('\r','')
        self.conv = self.conv.replace('pv','A').replace('**','^')
        if self.conv == "":
            self.conv = "A"

        if not self.name or self.name.startswith("-"):
            raise ValueError("Wrong name format {} tag {}".format(self.name, self.tag))

        if len(self.desc) > 39:
            self.desc = self.desc[0:39]

        # remove left zeros from scan period
        self.scan = self.scan.lstrip('0')

        if (self.inout == json_info.inout.read
                and self.scan not in SCAN_VALUES):
            raise ValueError(
                'Invalid scan value "{}" defined for name "{}".'.format(
                    self.scan, self.name
                )
            )

        # Filter invalid EGU character
        self.egu = (
            "" if type(self.egu) == float else re.sub(r"[^A-Za-z0-9 ]+", "", self.egu)
        )

        if (self.gen_type == json_info.gen_type.tag
                and (not self.tag or type(self.tag) != str
                    or self.tag == "" or self.tag == "N/A")):
            raise ValueError("Invalid tag for record {}".format(self.name))

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

def generate_bi_record(data: RowData, file_handler):
    file_handler.write(
        bi_template.safe_substitute(
            desc=data.desc,
            name=data.name,
            onam="True",
            scan=data.scan,
            tag=data.tag,
            znam="False",
            val=data.val,
        )
    )

def generate_bo_record(data: RowData, file_handler):
    file_handler.write(
        bo_template.safe_substitute(
            desc=data.desc,
            name=data.name,
            onam="True",
            scan=data.scan,
            tag=data.tag,
            znam="False",
            high=data.cmd_high,
        )
    )

def generate_ai_record(data: RowData, file_handler):
    file_handler.write(
        ai_template.safe_substitute(
            desc=data.desc,
            egu=data.egu,
            name=data.name,
            prec=data.prec,
            scan=data.scan,
            tag=data.tag,
            val=data.val,
            hsv=data.hsv,
            hhsv=data.hhsv,
            lsv=data.lsv,
            llsv=data.llsv,
        )
    )
def generate_wfm_record(data: RowData, file_handler):
    elem_count = len(data.val.split(','))
    file_handler.write(
        wfm_template.safe_substitute(
            name=data.name,
            inp=data.val,
            desc=data.desc,
            ftvl='DOUBLE',
            nelm=elem_count,
            prec=data.prec,
            egu=data.egu,
        )
    )
def generate_ao_record(data: RowData, file_handler):
    file_handler.write(
        ao_template.safe_substitute(
            desc=data.desc,
            egu=data.egu,
            name=data.name,
            prec=data.prec,
            scan=data.scan,
            tag=data.tag,
        )
    )

def generate_bi_from_bit(input_pv, shift_str, data: RowData, file_handler):
    aux_calc_name = data.name
    aux_calc_name = aux_calc_name.replace('-SP', '')
    aux_calc_name = aux_calc_name.replace('-Sel', '')
    aux_calc_name = aux_calc_name.replace('-RB', '')
    aux_calc_name = aux_calc_name.replace('-Sts', '')
    aux_calc_name = aux_calc_name.replace('-Cmd', '')
    aux_calc_name = aux_calc_name.replace('-Mon', '')
    aux_calc_name = aux_calc_name + 'InCalc'
    calc_desc = "Aux calc for " + data.name
    file_handler.write(
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
    file_handler.write(
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

def generate_bo_from_bit(output_pv, shift_str, data: RowData, file_handler):
    aux_calc_name = data.name
    aux_calc_name = aux_calc_name.replace('-SP', '')
    aux_calc_name = aux_calc_name.replace('-Sel', '')
    aux_calc_name = aux_calc_name.replace('-RB', '')
    aux_calc_name = aux_calc_name.replace('-Sts', '')
    aux_calc_name = aux_calc_name.replace('-Cmd', '')
    aux_calc_name = aux_calc_name.replace('-Mon', '')
    aux_calc_name = aux_calc_name + 'OutCalc'
    file_handler.write(
        bo_soft_channel_template.safe_substitute(
            desc=data.desc,
            name=data.name,
            onam="True",
            scan="Passive",
            out=aux_calc_name + ".PROC",
            out_type="PP",
            znam="False",
            high=data.cmd_high,
        )
    )
    calc_desc = "Aux calc for " + data.name
    file_handler.write(
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

def generate_var_type_record(data: RowData, file_handler):
    if data.dtype == json_info.dtype.bool:
        generate_bi_record(data, file_handler)
    elif (data.dtype == json_info.dtype.float
            or data.dtype == json_info.dtype.int):
        generate_ai_record(data, file_handler)
    elif data.dtype == json_info.dtype.array:
        generate_wfm_record(data, file_handler)

def generate_calc_type_record(data: RowData, file_handler):
    generate_conv_calc(
            file_handler, name=data.name, inp=data.inp,
            calc=data.conv, prec=data.prec,
            egu=data.egu, out=data.out, desc=data.desc)
    return

def generate_conv_type_record(data: RowData, file_handler):
    generate_polyn_calc(
            file_handler, name=data.name, inp=data.inp,
            prec=data.prec, egu=data.egu, nelm=20,
            out=data.out, desc=data.desc, args=data.args)
    return

def generate_tag_type_record(data: RowData, file_handler):
    if data.dtype == json_info.dtype.bool:
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
                generate_ao_record(data_32bit_tag, file_handler)
            if data.inout == json_info.inout.read:
                generate_bi_from_bit(
                    data_32bit_tag.name, shift_str, data, file_handler
                )
            elif data.inout == json_info.inout.write:
                generate_bo_from_bit(
                    data_32bit_tag.name, shift_str, data, file_handler
                )
        # other cases
        elif data.inout == json_info.inout.read:
            generate_bi_record(data, file_handler)
        elif data.inout == json_info.inout.write:
            generate_bo_record(data, file_handler)
        else:
            raise ValueError('Invalid Type "{}".'.format(data.inout + "  " + data.name))

    elif data.dtype == json_info.dtype.float:
        if data.inout == json_info.inout.read:
            if data.conv == "A":
                generate_ai_record(data, file_handler)
            else:
                data_copy = copy.copy(data)
                data_copy.name = remove_pv_suffix(data.name) + 'Raw'
                data_copy.desc = "Raw " + data.desc
                data_copy.desc = data.desc[0:40]
                generate_ai_record(data_copy, file_handler)
                generate_conv_calc(
                    file_handler, name=data.name, inp=data_copy.name,
                    calc=data.conv, prec=data.prec,
                    egu=data.egu, desc=data.desc
                )
        else:
            raise ValueError("Type Analog Out Not - Supported {}.".format(data.name))
    else:
        raise ValueError("Unknown data type {} at {}".format(data.dtype, data.name))


#def dict_from_sheets_generator(spreadsheet_path, sheet_names):
#    for sheet_name in sheet_names:
#        sheet = pandas.read_excel(spreadsheet_path, sheet_name=sheet_name, dtype=str, engine="openpyxl")
#        replace_info = {"\n": ""}
#        sheet.replace(replace_info, inplace=True, regex=True)
#        sheet.fillna("", inplace=True)
#        row_dict_list = sheet.to_dict(orient='records')
#        with open("../etc/"+sheet_name, 'w+') as f:
#            for line in row_dict_list:
#                f.write("%s\n" % line)
#        for d in row_dict_list:
#            yield d, sheet_name

#def json_from_sheets_generator(spreadsheet_path, sheet_names):
#    for sheet_name in sheet_names:
#        sheet = pandas.read_excel(spreadsheet_path, sheet_name=sheet_name, dtype=str, engine="openpyxl")
#        replace_info = {"\n": ""}
#        sheet.replace(replace_info, inplace=True, regex=True)
#        sheet.fillna("", inplace=True)
#        row_dict_list = sheet.to_dict(orient='records')
#        with open("../etc/"+sheet_name, 'w+') as f:
#            for line in row_dict_list:
#                f.write("%s\n" % line)

def parse_json_generator(json_paths):
    for json_path in json_paths:
        with open(json_path, 'r') as f:
            data_list = json.load(f)
        for data_dict in data_list:
            yield data_dict, json_path

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

def generate_polyn_calc(f, name, inp, prec, egu, nelm, out="", desc="", args=""):
    f.write(
        acalcout_generic_template.safe_substitute(
            name=name,
            desc=desc,
            scan="Passive",
            inpa=inp+" CP",
            inpb=args+".NELM",
            inaa=args,
            calc="L:=0;C:=0;D:=UNTIL(C:=C+A*AA[L,L]^L;L:=L+1;L>=B);C",
            egu=egu,
            prec=prec,
            out=out,
            nelm=nelm,
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
            inbb="",
            incc="",
            indd="",
            inee="",
            inff="",
            ingg="",
            inhh="",
            inii="",
            injj="",
            inkk="",
            inll="",
            flnk="",
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

def generate_records_from_row(
    row, json_name, file_handler, key_names: KeyNames, tags):
    try:
        data = RowData(row, key_names)
        if data.gen_type == json_info.gen_type.tag:
            if data.tag not in tags:
                tags[data.tag] = [data.name]
            else:
                tags[data.tag].append(data.name)
            generate_tag_type_record(data, file_handler)
        elif data.gen_type == json_info.gen_type.conv:
            generate_conv_type_record(data, file_handler)
        elif data.gen_type == json_info.gen_type.calc:
            generate_calc_type_record(data, file_handler)
        elif data.gen_type == json_info.gen_type.var:
            generate_var_type_record(data, file_handler)
    except ValueError as e:
        logger.error("Record Generation [{}]: {}".format(json_name, e))
    for tag, vals in tags.items():
        if len(vals) > 1:
            logger.error('Tag "{}" already exists {}.'.format(tag, tags[tag]))

def write_to_autosave_file(
    row, json_name, file_handler, key_names: KeyNames):
    try:
        data = RowData(row, key_names)
        if data.gen_type == json_info.gen_type.var:
            file_handler.write(data.name + "\n")
    except ValueError as e:
        logger.error("Autosave req file generation [{}]: {}".format(json_name, e))

def get_database_path(base_path, name):
    return os.path.join(base_path, "../ioc/database/") + name + ".db"

def get_autosave_path(base_path, name):
    return os.path.join(base_path, "../ioc/autosave/") + name + ".req"

def generate_db_file(
    base_path, json_paths, ioc_name, key_names: KeyNames
):
    ioc_database_path = get_database_path(base_path, ioc_name)
    tags = {}
    logger.info('Generating "{}.db" file at "{}".'.format(ioc_name, ioc_database_path))
    with open(ioc_database_path, "w+") as f:
        for row, json_name in parse_json_generator(json_paths=json_paths):
            generate_records_from_row(
                row=row,
                json_name=json_name,
                key_names=key_names,
                file_handler=f,
                tags=tags,
            )

def generate_autosave_file(
    base_path, json_paths, ioc_name, key_names: KeyNames
):
    ioc_autosave_path = get_autosave_path(base_path, ioc_name)
    logger.info('Generating "{}.req" file at "{}".'.format(ioc_name, ioc_autosave_path))
    with open(ioc_autosave_path, "w+") as f:
        for row, json_name in parse_json_generator(json_paths=json_paths):
            write_to_autosave_file(
                row=row,
                json_name=json_name,
                key_names=key_names,
                file_handler=f,
            )

def generate(args, base_path):
    logger.info("Args, {}.".format(vars(args)))

    arch = args.arch
    base_path = base_path
    ioc_name = args.ioc_name
    plc_module = args.plc_module
    plc_name = args.plc_name
    sheet_names = args.sheet.split(",")
    spreadsheet_path = args.spreadsheet
    json_paths = args.json.split(",")

    if spreadsheet_path != "" and json_paths != "":
        logger.error("Cannot generated IOC from both JSON and spreadsheet: specify only one option.")
        sys.exit(1)
    elif spreadsheet_path != "" and  len(sheet_names) > 0:
        # create json files and return paths
        #json_paths = json_from_sheets_generator(spreadsheet_path, sheet_names)
        logger.error("Spreadsheet option is currently not support: specify json file instead.")

    generate_cmd_file(
        base_path=base_path,
        arch=arch,
        ioc_name=ioc_name,
        plc_module=plc_module,
        plc_name=plc_name,
    )

    key_names = KeyNames(
        gen_type=json_info.keys.gen_type,
        name=json_info.keys.name,
        desc=json_info.keys.desc,
        tag=json_info.keys.tag,
        inout=json_info.keys.inout,
        dtype=json_info.keys.dtype,
        egu=json_info.keys.egu,
        scan=json_info.keys.scan,
        prec=json_info.keys.prec,
        inp=json_info.keys.inp,
        out=json_info.keys.out,
        args=json_info.keys.args,
        cmd_high=json_info.keys.cmd_high,
        conv=json_info.keys.conv,
        val=json_info.keys.val,
        hsv=json_info.keys.hsv,
        hhsv=json_info.keys.hhsv,
        lsv=json_info.keys.lsv,
        llsv=json_info.keys.llsv,
    )

    generate_db_file(
        base_path=base_path,
        json_paths=json_paths,
        ioc_name=ioc_name,
        key_names=key_names,
    )

    generate_autosave_file(
        base_path=base_path,
        json_paths=json_paths,
        ioc_name=ioc_name,
        key_names=key_names,
    )
