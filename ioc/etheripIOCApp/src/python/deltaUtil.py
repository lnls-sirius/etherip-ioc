import urllib.request as _request
import traceback as _traceback
import re
import math as _math

class UnitConverter(object):
    """ Constructor arguments:

        urlLVTable: URL to access Linear Vertical table data
        urlLHTable: URL to access Linear Horizontal table data
        urlCRTable: URL to access Circular Right table data
        urlCLTable: URL to access Circular Left table data
        xVarLVTable: name of x array monitored by EPICS DB for LV Table
        xVarLHTable: name of x array monitored by EPICS DB for LH Table
        xVarCRTable: name of x array monitored by EPICS DB for CR Table
        xVarCLTable: name of x array monitored by EPICS DB for CL Table
        yVarLVTable: name of y array monitored by EPICS DB for LV Table
        yVarLHTable: name of y array monitored by EPICS DB for LH Table
        yVarCRTable: name of y array monitored by EPICS DB for CR Table
        yVarCLTable: name of y array monitored by EPICS DB for CL Table
        statusVar: name of conversion status var monitored by EPICS DB
        port: http server port """
    def __init__(self, urlLVTable, xVarLVTable, yVarLVTable,
                 urlLHTable, xVarLHTable, yVarLHTable,
                 urlCRTable, xVarCRTable, yVarCRTable,
                 urlCLTable, xVarCLTable, yVarCLTable,
                 statusVar, port=80):

        # properties of conversion tables
        self._urlLVTable = urlLVTable
        self._urlLHTable = urlLHTable
        self._urlCRTable = urlCRTable
        self._urlCLTable = urlCLTable

        self._xVarLVTable = xVarLVTable
        self._yVarLVTable = yVarLVTable
        self._xVarLHTable = xVarLHTable
        self._yVarLHTable = yVarLHTable
        self._xVarCRTable = xVarCRTable
        self._yVarCRTable = yVarCRTable
        self._xVarCLTable = xVarCLTable
        self._yVarCLTable = yVarCLTable

        self._statusVar = statusVar

        # init conversion status as invalid
        pydev.iointr(self._statusVar, 0)
    def update(self):
        try:
            # update conversion data
            ## Linear Vertical
            self.getArrays(self._urlLVTable, self._xVarLVTable, self._yVarLVTable)
            ## Linear Horizontal
            self.getArrays(self._urlLHTable, self._xVarLHTable, self._yVarLHTable)
            ## Circular Right
            self.getArrays(self._urlCRTable, self._xVarCRTable, self._yVarCRTable)
            ## Circular Left
            self.getArrays(self._urlCLTable, self._xVarCLTable, self._yVarCLTable)
            # update conversion status
            pydev.iointr(self._statusVar, 1)
        except Exception:
            # print exception
            _traceback.print_exc(file=_sys.stdout)
            # update conversion status
            pydev.iointr(self._statusVar, 0)
            return

        return

    def getArrays(self, url, xVar, yVar):
        # request data from server
        with _request.urlopen(url) as f:
            resp = f.read()
        # parse data
        x, y = self.parse(resp)
        # send intr to EPICS PVs
        pydev.iointr(xVar, x)
        pydev.iointr(yVar, y)
        return

    def parse(self, raw_data):
        # decode
        d = raw_data.decode('utf-8')
        # split lines
        d = d.split('\n')
        # remove header
        d = [i for i in d if '#' not in i]
        # remove extra spaces from strings
        d = [re.sub(' +', ' ', i) for i in d]
        # split x and y pairs
        x = []
        y = []
        for pair in d:
            xy = pair.split(' ')
            # ignore empty lines
            if len(xy) <= 1:
                continue
            # append values
            x.append(float(xy[0]))
            y.append(float(xy[1]))
        return x, y
