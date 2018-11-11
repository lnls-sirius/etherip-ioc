#!/usr/bin/python3
import argparse
import pandas

parser = argparse.ArgumentParser(description="Generate Sirius RF - IOC.")

parser.add_argument('spreadsheet', help='Excel spreadsheet location.')

parser.add_argument('--ring-sheet', default='Anel', help='Ring sheet name.')
parser.add_argument('--booster-sheet', default='Booster', help='Booster sheet name.')

parser.add_argument('--ring-ioc-name', default='Rf-Ring', help='Ring IOC name.')
parser.add_argument('--booster-ioc-name', default='Rf-Booster', help='Booster IOC name.')

parser.add_argument('--col-pv', default='EPICS', help='PV column name.')
parser.add_argument('--col-desc', default='Descrição', help='Desc column name.')
parser.add_argument('--col-tag', default='RS Logix', help='Desc column name.')
parser.add_argument('--col-inout', default='Input/Output', help='Input/Output column name.')
parser.add_argument('--col-dtype', default='Tipo de dado', help='Data type column name.')

parser.add_argument('--arch', choices=['linux-x86_64', 'linux-arm'], default='linux-x86_64',
                    help='System architecture.')
parser.add_argument('--rf-system', choices=['all', 'booster', 'ring'], default='all',
                    help='System architecture.')
args = parser.parse_args()

def generate_booster(sheet):
    print(sheet.head())
    for pv, desc, tag, inout, dtype in \
            zip(sheet[args.col_pv],
             sheet[args.col_desc],
             sheet[args.col_tag],
             sheet[args.col_inout],
             sheet[args.col_dtype]):

        print(pv,desc,tag,inout,dtype)

def generate_ring(sheet):
    print(sheet.head())
    for pv, desc, tag, inout, dtype in \
            zip(sheet[args.col_pv],
             sheet[args.col_desc],
             sheet[args.col_tag],
             sheet[args.col_inout],
             sheet[args.col_dtype]):

        print(pv,desc,tag,inout,dtype)

if __name__ == '__main__':
    ring_sheet = pandas.read_excel(args.spreadsheet, sheet_name=args.ring_sheet)
    booster_sheet = pandas.read_excel(args.spreadsheet, sheet_name=args.booster_sheet)
    if args.rf_system == 'booster':
        generate_booster(booster_sheet)
    elif args.rf_system == 'ring':
        generate_ring(ring_sheet)
    else:
        generate_booster(booster_sheet)
        generate_ring(ring_sheet)
        
    # print(booster_sheet[args.col_pv])
    # print(booster_sheet[args.col_desc])


