#!/usr/bin/env python3

########################### Run in Python 3 ###########################

from xlsxwriter import Workbook
import argparse
from templates_delta import *

def write_template_based_sheet(workbook, sheetname, tmpl, *othercols):
    # create sheet
    sh = workbook.add_worksheet(sheetname)
    # write column names explicitly provided
    i = 0
    for col_name in othercols:
        sh.write(0, i, col_name) 
        i = i+1
    # get additional columns from template
    #   code snippet from
    #   https://stackoverflow.com/questions/35866232
    fields = [m.group('named') or m.group('braced')
              for m in tmpl.pattern.finditer(tmpl.template)
              if m.group('named') or m.group('braced')]
    # write column names corresponding to template fields
    for col_name in fields:
        if col_name in othercols:
            continue
        sh.write(0, i, col_name.upper())
        i = i+1

# create example workbook
def create_workbook(wb_name='example_wb.xlsx',
                    sh_dict={'ao_sheet':ao_template,
                             'ai_sheet':ai_template,
                             'bo_sheet':bo_template,
                             'bi_sheet':bi_template,
                             'lso_sheet':lso_template,
                             'lsi_sheet':lsi_template
                    }):
    # create workbook
    wb = Workbook(wb_name)
    # insert sheets
    for sheet, tmpl in sh_dict.items():
        write_template_based_sheet(wb, sheet, tmpl, 'Data type', 'In/Out')
    # close and write workbook
    wb.close()

# Main
if __name__ == '__main__':
    # parse input
    parser = argparse.ArgumentParser(description="Generate Example Worksheet")
    parser.add_argument("--name",
                        dest="wb_name",
                        help="Example workbook name")
    args = parser.parse_args()
    if args.wb_name is None:
        # use defaults
        create_workbook()
    else:
        create_workbook(wb_name=args.wb_name)
