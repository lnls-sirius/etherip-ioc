#!/usr/bin/env python3
import argparse
import pandas
import logging
import re


from src import FileManager, config_logger
from src.consts import SCAN_VALUES, defaults
from src.templates.delta import (
    ai_template,
    ao_template,
    bi_template,
    bo_cmd_template,
    bo_template,
    cmd_template,
    lsi_template,
    lso_template,
    mbbi_template,
    mbbo_template,
)

logger = logging.getLogger()


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

    parser.add_argument(
        "--col-desc", default="Description", help="EPICS desc column name."
    )
    parser.add_argument(
        "--col-dtype", default="Data Type", help="Data type column name."
    )
    parser.add_argument("--col-egu", default="EGU", help="EPICS egu column name.")
    parser.add_argument(
        "--col-inout", default="In/Out", help="Input/Output column name."
    )
    parser.add_argument("--col-prec", default="Prec", help="EPICS prec column name.")
    parser.add_argument("--col-pv", default="NAME", help="PV column name.")
    parser.add_argument(
        "--col-scan", default="Scan", help="EPICS scan time column name."
    )
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
        "--col-znam", default="ZNAM", help="EPICS Binary Zero Name column name."
    )
    parser.add_argument(
        "--col-onam", default="ONAM", help="EPICS Binary One Name column name."
    )
    parser.add_argument(
        "--col-zsv", default="ZSV", help="EPICS Binary Zero Severity column name."
    )
    parser.add_argument(
        "--col-osv", default="OSV", help="EPICS Binary One Severity column name."
    )
    parser.add_argument(
        "--col-drvh", default="DRVH", help="EPICS Analog Out Driver High column name."
    )
    parser.add_argument(
        "--col-drvl", default="DRVL", help="EPICS Analog Out Driver Low column name."
    )
    parser.add_argument(
        "--col-hopr", default="HOPR", help="EPICS High Operating Range column name."
    )
    parser.add_argument(
        "--col-lopr", default="LOPR", help="EPICS Low Operating Range column name."
    )
    parser.add_argument(
        "--col-hihi", default="HIHI", help="EPICS High High Alarm Limit column name."
    )
    parser.add_argument(
        "--col-high", default="HIGH", help="EPICS High Alarm Limit column name."
    )
    parser.add_argument(
        "--col-low", default="LOW", help="EPICS Low Alarm Limit column name."
    )
    parser.add_argument(
        "--col-lolo", default="LOLO", help="EPICS Low Low Alarm Limit column name."
    )
    parser.add_argument(
        "--col-hhsv", default="HHSV", help="EPICS High High Alarm Severity column name."
    )
    parser.add_argument(
        "--col-hsv", default="HSV", help="EPICS High Alarm Severity column name."
    )
    parser.add_argument(
        "--col-lsv", default="LSV", help="EPICS Low Alarm Severity column name."
    )
    parser.add_argument(
        "--col-llsv", default="LLSV", help="EPICS Low Low Alarm Severity column name."
    )
    parser.add_argument(
        "--col-hyst", default="HYST", help="EPICS Alarm Deadband column name."
    )
    parser.add_argument(
        "--col-sizv",
        default="SIZV",
        help="EPICS Long String Size of Buffer column name.",
    )
    parser.add_argument(
        "--col-omsl",
        default="OMSL",
        help="EPICS Output Mode Select column name.",
    )
    parser.add_argument(
        "--col-dol",
        default="DOL",
        help="EPICS Desired Output Location column name.",
    )
    parser.add_argument(
        "--col-shft",
        default="SHFT",
        help="EPICS Shift column name.",
    )
    parser.add_argument(
        "--col-ivoa",
        default="IVOA",
        help="EPICS INVALID output action column name.",
    )
    parser.add_argument(
        "--col-ivov",
        default="IVOV",
        help="EPICS INVALID output value column name.",
    )
    parser.add_argument(
        "--col-unsv",
        default="UNSV",
        help="EPICS Unknown State Severity column name.",
    )
    parser.add_argument(
        "--col-cosv",
        default="COSV",
        help="EPICS Change Of State Severity column name.",
    )
    parser.add_argument(
        "--col-zrvl",
        default="ZRVL",
        help="EPICS Zero Value column name.",
    )
    parser.add_argument(
        "--col-zrst",
        default="ZRST",
        help="EPICS Zero String column name.",
    )
    parser.add_argument(
        "--col-zrsv",
        default="ZRSV",
        help="EPICS State Zero Severity column name.",
    )
    parser.add_argument(
        "--col-onvl",
        default="ONVL",
        help="EPICS One Value column name.",
    )
    parser.add_argument(
        "--col-onst",
        default="ONST",
        help="EPICS One String column name.",
    )
    parser.add_argument(
        "--col-onsv",
        default="ONSV",
        help="EPICS State One Severity column name.",
    )
    parser.add_argument(
        "--col-twvl",
        default="TWVL",
        help="EPICS Two Value column name.",
    )
    parser.add_argument(
        "--col-twst",
        default="TWST",
        help="EPICS Two String column name.",
    )
    parser.add_argument(
        "--col-twsv",
        default="TWSV",
        help="EPICS State Two Severity column name.",
    )
    parser.add_argument(
        "--col-thvl",
        default="THVL",
        help="EPICS Three Value column name.",
    )
    parser.add_argument(
        "--col-thst",
        default="THST",
        help="EPICS Three String column name.",
    )
    parser.add_argument(
        "--col-thsv",
        default="THSV",
        help="EPICS State Three Severity column name.",
    )
    parser.add_argument(
        "--col-frvl",
        default="FRVL",
        help="EPICS Four Value column name.",
    )
    parser.add_argument(
        "--col-frst",
        default="FRST",
        help="EPICS Four String column name.",
    )
    parser.add_argument(
        "--col-frsv",
        default="FRSV",
        help="EPICS State Four Severity column name.",
    )
    parser.add_argument(
        "--col-fvvl",
        default="FVVL",
        help="EPICS Five Value column name.",
    )
    parser.add_argument(
        "--col-fvst",
        default="FVST",
        help="EPICS Five String column name.",
    )
    parser.add_argument(
        "--col-fvsv",
        default="FVSV",
        help="EPICS State Five Severity column name.",
    )
    parser.add_argument(
        "--col-sxvl",
        default="SXVL",
        help="EPICS Six Value column name.",
    )
    parser.add_argument(
        "--col-sxst",
        default="SXST",
        help="EPICS Six String column name.",
    )
    parser.add_argument(
        "--col-sxsv",
        default="SXSV",
        help="EPICS State Six Severity column name.",
    )
    parser.add_argument(
        "--col-svvl",
        default="SVVL",
        help="EPICS Seven Value column name.",
    )
    parser.add_argument(
        "--col-svst",
        default="SVST",
        help="EPICS Seven String column name.",
    )
    parser.add_argument(
        "--col-svsv",
        default="SVSV",
        help="EPICS State Seven Severity column name.",
    )
    parser.add_argument(
        "--col-eivl",
        default="EIVL",
        help="EPICS Eight Value column name.",
    )
    parser.add_argument(
        "--col-eist",
        default="EIST",
        help="EPICS Eight String column name.",
    )
    parser.add_argument(
        "--col-eisv",
        default="EISV",
        help="EPICS State Eight Severity column name.",
    )
    parser.add_argument(
        "--col-nivl",
        default="NIVL",
        help="EPICS Nine Value column name.",
    )
    parser.add_argument(
        "--col-nist",
        default="NIST",
        help="EPICS Nine String column name.",
    )
    parser.add_argument(
        "--col-nisv",
        default="NISV",
        help="EPICS State Nine Severity column name.",
    )
    parser.add_argument(
        "--col-tevl",
        default="TEVL",
        help="EPICS Ten Value column name.",
    )
    parser.add_argument(
        "--col-test",
        default="TEST",
        help="EPICS Ten String column name.",
    )
    parser.add_argument(
        "--col-tesv",
        default="TESV",
        help="EPICS State Ten Severity column name.",
    )
    parser.add_argument(
        "--col-elvl",
        default="ELVL",
        help="EPICS Eleven Value column name.",
    )
    parser.add_argument(
        "--col-elst",
        default="ELST",
        help="EPICS Eleven String column name.",
    )
    parser.add_argument(
        "--col-elsv",
        default="ELSV",
        help="EPICS State Eleven Severity column name.",
    )
    parser.add_argument(
        "--col-tvvl",
        default="TVVL",
        help="EPICS Twelve Value column name.",
    )
    parser.add_argument(
        "--col-tvst",
        default="TVST",
        help="EPICS Twelve String column name.",
    )
    parser.add_argument(
        "--col-tvsv",
        default="TVSV",
        help="EPICS State Twelve Severity column name.",
    )
    parser.add_argument(
        "--col-ttvl",
        default="TTVL",
        help="EPICS Thirteen Value column name.",
    )
    parser.add_argument(
        "--col-ttst",
        default="TTST",
        help="EPICS Thirteen String column name.",
    )
    parser.add_argument(
        "--col-ttsv",
        default="TTSV",
        help="EPICS State Thirteen Severity column name.",
    )
    parser.add_argument(
        "--col-ftvl",
        default="FTVL",
        help="EPICS Fourteen Value column name.",
    )
    parser.add_argument(
        "--col-ftst",
        default="FTST",
        help="EPICS Fourteen String column name.",
    )
    parser.add_argument(
        "--col-ftsv",
        default="FTSV",
        help="EPICS State Fourteen Severity column name.",
    )
    parser.add_argument(
        "--col-ffvl",
        default="FFVL",
        help="EPICS Fifteen Value column name.",
    )
    parser.add_argument(
        "--col-ffst",
        default="FFST",
        help="EPICS Fifteen String column name.",
    )
    parser.add_argument(
        "--col-ffsv",
        default="FFSV",
        help="EPICS State Fifteen Severity column name.",
    )
    parser.add_argument(
        "--bi",
        nargs="+",
        default="Binary Input",
        help="EPICS bi data type alias (can be more than one).",
    )
    parser.add_argument(
        "--bo",
        nargs="+",
        default="Binary Output",
        help="EPICS bo data type alias (can be more than one).",
    )
    parser.add_argument(
        "--ai",
        nargs="+",
        default="Analog Input",
        help="EPICS ai data type alias (can be more than one).",
    )
    parser.add_argument(
        "--ao",
        nargs="+",
        default="Analog Output",
        help="EPICS ao data type alias (can be more than one).",
    )
    parser.add_argument(
        "--mbbi",
        nargs="+",
        default="Enum Input",
        help="EPICS mbbi data type alias (can be more than one).",
    )
    parser.add_argument(
        "--mbbo",
        nargs="+",
        default="Enum Output",
        help="EPICS mbbo data type alias (can be more than one).",
    )
    # EPICS base 3.15 only
    parser.add_argument(
        "--lsi",
        nargs="+",
        default="Long String Input",
        help="EPICS lsi data type alias (can be more than one).",
    )
    # EPICS base 3.15 only
    parser.add_argument(
        "--lso",
        nargs="+",
        default="Long String Output",
        help="EPICS lso data type alias (can be more than one).",
    )

    args = parser.parse_args()
    return args


def generate(args):
    sheet_name = args.sheet.split(",")
    logger.info("Args, {}.".format(vars(args)))
    fm = FileManager(args.ioc_name)

    logger.info(
        'Generating "{}.cmd" file at "{}".'.format(args.ioc_name, fm.ioc_db_file_path())
    )

    # generate CMD file
    with open(fm.ioc_cmd_file_path(), "w+") as f:
        f.write(
            cmd_template.safe_substitute(
                arch=args.arch,
                database=args.ioc_name,
                module=args.plc_module,
                plc=args.plc_name,
            )
        )
    tags = {}
    logger.info(
        'Generating "{}.db" file at "{}".'.format(args.ioc_name, fm.ioc_db_file_path())
    )

    # generate DB file
    with open(fm.ioc_db_file_path(), "w+") as f:
        for s_name in sheet_name:
            sheet = pandas.read_excel(args.spreadsheet, sheet_name=s_name, dtype=str, engine="openpyxl")
            replace_info = {"\n": ""}
            sheet.replace(replace_info, inplace=True, regex=True)
            sheet.fillna("", inplace=True)
            # check required columns
            if args.col_pv not in sheet.columns:
                logger.error(
                    "Could not find required {} column in {} sheet.".format(
                        args.col_pv, s_name
                    )
                )
                continue
            if args.col_tag not in sheet.columns:
                logger.error(
                    "Could not find required {} column in {} sheet.".format(
                        args.col_tag, s_name
                    )
                )
                continue
            if args.col_dtype not in sheet.columns:
                logger.error(
                    "Could not find required {} column in {} sheet.".format(
                        args.col_dtype, s_name
                    )
                )
                continue
            for n, row in sheet.iterrows():
                # main columnn
                name = row[args.col_pv]
                tag = row[args.col_tag]
                dtype = row[args.col_dtype]
                # optional columns
                inout = row.get(args.col_inout, "")
                desc = row.get(args.col_desc, defaults["desc"])
                egu = row.get(args.col_egu, defaults["egu"])
                scan = row.get(args.col_scan, defaults["scan"])
                prec = row.get(args.col_prec, defaults["prec"])
                znam = row.get(args.col_znam, defaults["znam"])
                onam = row.get(args.col_onam, defaults["onam"])
                zsv = row.get(args.col_zsv, defaults["zsv"])
                osv = row.get(args.col_osv, defaults["osv"])
                drvh = row.get(args.col_drvh, defaults["drvh"])
                drvl = row.get(args.col_drvl, defaults["drvl"])
                hopr = row.get(args.col_hopr, defaults["hopr"])
                lopr = row.get(args.col_lopr, defaults["lopr"])
                hihi = row.get(args.col_hihi, defaults["hihi"])
                high = row.get(args.col_high, defaults["high"])
                low = row.get(args.col_low, defaults["low"])
                lolo = row.get(args.col_lolo, defaults["lolo"])
                hhsv = row.get(args.col_hhsv, defaults["hhsv"])
                hsv = row.get(args.col_hsv, defaults["hsv"])
                lsv = row.get(args.col_lsv, defaults["lsv"])
                llsv = row.get(args.col_llsv, defaults["llsv"])
                hyst = row.get(args.col_hyst, defaults["hyst"])
                sizv = row.get(args.col_sizv, defaults["sizv"])
                omsl = row.get(args.col_omsl, defaults["omsl"])
                dol = row.get(args.col_dol, defaults["dol"])
                shft = row.get(args.col_shft, defaults["shft"])
                ivoa = row.get(args.col_ivoa, defaults["ivoa"])
                ivov = row.get(args.col_ivov, defaults["ivov"])
                unsv = row.get(args.col_unsv, defaults["unsv"])
                cosv = row.get(args.col_cosv, defaults["cosv"])
                zrvl = row.get(args.col_zrvl, defaults["zrvl"])
                zrst = row.get(args.col_zrst, defaults["zrst"])
                zrsv = row.get(args.col_zrsv, defaults["zrsv"])
                onvl = row.get(args.col_onvl, defaults["onvl"])
                onst = row.get(args.col_onst, defaults["onst"])
                onsv = row.get(args.col_onsv, defaults["onsv"])
                twvl = row.get(args.col_twvl, defaults["twvl"])
                twst = row.get(args.col_twst, defaults["twst"])
                twsv = row.get(args.col_twsv, defaults["twsv"])
                thvl = row.get(args.col_thvl, defaults["thvl"])
                thst = row.get(args.col_thst, defaults["thst"])
                thsv = row.get(args.col_thsv, defaults["thsv"])
                frvl = row.get(args.col_frvl, defaults["frvl"])
                frst = row.get(args.col_frst, defaults["frst"])
                frsv = row.get(args.col_frsv, defaults["frsv"])
                fvvl = row.get(args.col_fvvl, defaults["fvvl"])
                fvst = row.get(args.col_fvst, defaults["fvst"])
                fvsv = row.get(args.col_fvsv, defaults["fvsv"])
                sxvl = row.get(args.col_sxvl, defaults["sxvl"])
                sxst = row.get(args.col_sxst, defaults["sxst"])
                sxsv = row.get(args.col_sxsv, defaults["sxsv"])
                svvl = row.get(args.col_svvl, defaults["svvl"])
                svst = row.get(args.col_svst, defaults["svst"])
                svsv = row.get(args.col_svsv, defaults["svsv"])
                eivl = row.get(args.col_eivl, defaults["eivl"])
                eist = row.get(args.col_eist, defaults["eist"])
                eisv = row.get(args.col_eisv, defaults["eisv"])
                nivl = row.get(args.col_nivl, defaults["nivl"])
                nist = row.get(args.col_nist, defaults["nist"])
                nisv = row.get(args.col_nisv, defaults["nisv"])
                tevl = row.get(args.col_tevl, defaults["tevl"])
                test = row.get(args.col_test, defaults["test"])
                tesv = row.get(args.col_tesv, defaults["tesv"])
                elvl = row.get(args.col_elvl, defaults["elvl"])
                elst = row.get(args.col_elst, defaults["elst"])
                elsv = row.get(args.col_elsv, defaults["elsv"])
                tvvl = row.get(args.col_tvvl, defaults["tvvl"])
                tvst = row.get(args.col_tvst, defaults["tvst"])
                tvsv = row.get(args.col_tvsv, defaults["tvsv"])
                ttvl = row.get(args.col_ttvl, defaults["ttvl"])
                ttst = row.get(args.col_ttst, defaults["ttst"])
                ttsv = row.get(args.col_ttsv, defaults["ttsv"])
                ftvl = row.get(args.col_ftvl, defaults["ftvl"])
                ftst = row.get(args.col_ftst, defaults["ftst"])
                ftsv = row.get(args.col_ftsv, defaults["ftsv"])
                ffvl = row.get(args.col_ffvl, defaults["ffvl"])
                ffst = row.get(args.col_ffst, defaults["ffst"])
                ffsv = row.get(args.col_ffsv, defaults["ffsv"])

                if not name or name.startswith("-"):
                    continue

                # find if record is of command type '-Cmd'
                is_cmd_rec = False
                if name.endswith("-Cmd"):
                    is_cmd_rec = True

                if len(desc) > 28:
                    desc = desc[0:28]

                if type(egu) == float:
                    egu = ""
                else:
                    egu = re.sub(r"[^A-Za-z0-9/% ]+", "", egu)

                if scan not in SCAN_VALUES:
                    logger.error(
                        'Invalid scan value "{}" defined for pv "{}".'.format(
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

                # Concatenate dtype and inout information.
                #     Ex: dype='Analog', inout='Ouput' =>
                #         full_type = 'Analog Output'
                #     If inout has no value, full_type = dtype
                full_type = dtype
                if inout != "" and not inout.startswith("-") and inout.lower != "n/a":
                    full_type = dtype + " " + inout

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
                elif (full_type in args.bo) and (is_cmd_rec == False):
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
                elif (full_type in args.bo) and (is_cmd_rec == True):
                    f.write(
                        bo_cmd_template.safe_substitute(
                            name=name,
                            auxname=name[: name.rfind("-Cmd")] + "CmdAux",
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
                elif full_type in args.mbbi:
                    f.write(
                        mbbi_template.safe_substitute(
                            name=name,
                            tag=tag,
                            desc=desc,
                            scan=scan,
                            shft=shft,
                            unsv=unsv,
                            cosv=cosv,
                            zrvl=zrvl,
                            zrst=zrst,
                            zrsv=zrsv,
                            onvl=onvl,
                            onst=onst,
                            onsv=onsv,
                            twvl=twvl,
                            twst=twst,
                            twsv=twsv,
                            thvl=thvl,
                            thst=thst,
                            thsv=thsv,
                            frvl=frvl,
                            frst=frst,
                            frsv=frsv,
                            fvvl=fvvl,
                            fvst=fvst,
                            fvsv=fvsv,
                            sxvl=sxvl,
                            sxst=sxst,
                            sxsv=sxsv,
                            svvl=svvl,
                            svst=svst,
                            svsv=svsv,
                            eivl=eivl,
                            eist=eist,
                            eisv=eisv,
                            nivl=nivl,
                            nist=nist,
                            nisv=nisv,
                            tevl=tevl,
                            test=test,
                            tesv=tesv,
                            elvl=elvl,
                            elst=elst,
                            elsv=elsv,
                            tvvl=tvvl,
                            tvst=tvst,
                            tvsv=tvsv,
                            ttvl=ttvl,
                            ttst=ttst,
                            ttsv=ttsv,
                            ftvl=ftvl,
                            ftst=ftst,
                            ftsv=ftsv,
                            ffvl=ffvl,
                            ffst=ffst,
                            ffsv=ffsv,
                        )
                    )
                elif full_type in args.mbbo:
                    f.write(
                        mbbo_template.safe_substitute(
                            name=name,
                            tag=tag,
                            desc=desc,
                            scan=scan,
                            omsl=omsl,
                            dol=dol,
                            shft=shft,
                            ivoa=ivoa,
                            ivov=ivov,
                            unsv=unsv,
                            cosv=cosv,
                            zrvl=zrvl,
                            zrst=zrst,
                            zrsv=zrsv,
                            onvl=onvl,
                            onst=onst,
                            onsv=onsv,
                            twvl=twvl,
                            twst=twst,
                            twsv=twsv,
                            thvl=thvl,
                            thst=thst,
                            thsv=thsv,
                            frvl=frvl,
                            frst=frst,
                            frsv=frsv,
                            fvvl=fvvl,
                            fvst=fvst,
                            fvsv=fvsv,
                            sxvl=sxvl,
                            sxst=sxst,
                            sxsv=sxsv,
                            svvl=svvl,
                            svst=svst,
                            svsv=svsv,
                            eivl=eivl,
                            eist=eist,
                            eisv=eisv,
                            nivl=nivl,
                            nist=nist,
                            nisv=nisv,
                            tevl=tevl,
                            test=test,
                            tesv=tesv,
                            elvl=elvl,
                            elst=elst,
                            elsv=elsv,
                            tvvl=tvvl,
                            tvst=tvst,
                            tvsv=tvsv,
                            ttvl=ttvl,
                            ttst=ttst,
                            ttsv=ttsv,
                            ftvl=ftvl,
                            ftst=ftst,
                            ftsv=ftsv,
                            ffvl=ffvl,
                            ffst=ffst,
                            ffsv=ffsv,
                        )
                    )
                else:
                    logger.warning(
                        'Invalid Type "{}".'.format(full_type + " for " + name)
                    )

            for tag, vals in tags.items():
                if len(vals) > 1:
                    logger.warning('Tag "{}" already exists {}.'.format(tag, tags[tag]))


if __name__ == "__main__":
    config_logger(logger)
    args = get_args()
    generate(args)
