#!/usr/bin/python3
from string import Template

cmd_template = Template(
    """#!../../bin/linux-x86_64/etheripIOC
< envPaths
< logEnv

cd "${TOP}"

# Load dbd, register the drvEtherIP .. commands
dbLoadDatabase("dbd/etheripIOC.dbd")
etheripIOC_registerRecordDeviceDriver(pdbbase)

asSetFilename("${TOP}/db/Security.as")

# Autosave settings
set_requestfile_path("$(TOP)", "autosave")
set_savefile_path("$(TOP)/autosave/save")

save_restoreSet_DatedBackupFiles(1)
save_restoreSet_NumSeqFiles(2)
save_restoreSet_SeqPeriodInSeconds(600)

iocLogInit

# Initialize EtherIP driver, define PLCs
EIP_buffer_limit(450)
drvEtherIP_init()
EIP_verbosity(7)
drvEtherIP_define_PLC("${plc}", "$(DEVIP)", ${module})

dbLoadRecords("database/${database}.db", "P=${P}, R=${R}, PLC=${plc}")
iocInit()

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
"""
)

ao_template = Template(
    """
record(ao, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag} S ${scan}")
    field(DESC, "${desc}")
    field(SCAN, "Passive")
    field(PREC, "${prec}")
    field(EGU,  "${egu}")
    field(DRVH, "${drvh}")
    field(DRVL, "${drvl}")
    field(HOPR, "${hopr}")
    field(LOPR, "${lopr}")
    field(HIHI, "${hihi}")
    field(HIGH, "${high}")
    field(LOW, "${low}")
    field(LOLO, "${lolo}")
    field(HHSV, "${hhsv}")
    field(HSV, "${hsv}")
    field(LSV, "${lsv}")
    field(LLSV, "${llsv}")
    field(HYST, "${hyst}")
}
"""
)

ai_template = Template(
    """
record(ai, "${name}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(PREC, "${prec}")
    field(EGU,  "${egu}")
    field(HOPR, "${hopr}")
    field(LOPR, "${lopr}")
    field(HIHI, "${hihi}")
    field(HIGH, "${high}")
    field(LOW, "${low}")
    field(LOLO, "${lolo}")
    field(HHSV, "${hhsv}")
    field(HSV, "${hsv}")
    field(LSV, "${lsv}")
    field(LLSV, "${llsv}")
    field(HYST, "${hyst}")
}
"""
)

bo_template = Template(
    """
record(bo, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag} S ${scan}")
    field(DESC, "${desc}")
    field(SCAN, "Passive")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
    field(ZSV, "${zsv}")
    field(OSV, "${osv}")
}
"""
)

bi_template = Template(
    """
record(bi, "${name}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
    field(ZSV, "${zsv}")
    field(OSV, "${osv}")
}
"""
)

lsi_template = Template(
    """
record(lsi, "${name}"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(SIZV,  "${sizv}")
}
"""
)

lso_template = Template(
    """
record(lso, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(SIZV,  "${sizv}")
}
"""
)

bo_cmd_template = Template(
    """
record(bo, "${name}"){
    field(DESC, "${desc}")
    field(OUT, "${auxname}1.PROC PP")
    field(SCAN, "Passive")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
    field(ZSV, "${zsv}")
    field(OSV, "${osv}")
}
record(calcout, "${auxname}1"){
    field(OUT, "${auxname}2.VAL PP")
    field(DESC, "aux rec 1")
    field(CALC, "1")
}
record(bo, "${auxname}2"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag} S ${scan}")
    field(DESC, "aux rec 2")
    field(SCAN, "Passive")
    field(ONAM, "0")
    field(ZNAM, "1")
    field(ZSV, "${zsv}")
    field(OSV, "${osv}")
}
"""
)

mbbo_template = Template(
    """
record(ao, "${auxname}1"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag} S ${scan}")
}

record(mbbo, "${name}"){
    field(OUT, "${auxname}1 PP")
    field(DESC, "${desc}")
    field(SCAN, "Passive")
    field(OMSL, "${omsl}")
    field(DOL, "${dol}")
    field(SHFT, "${shft}")
    field(IVOA, "${ivoa}")
    field(IVOV, "${ivov}")
    field(UNSV, "${unsv}")
    field(COSV, "${cosv}")
    field(ZRVL, "${zrvl}")
    field(ZRST, "${zrst}")
    field(ZRSV, "${zrsv}")
    field(ONVL, "${onvl}")
    field(ONST, "${onst}")
    field(ONSV, "${onsv}")
    field(TWVL, "${twvl}")
    field(TWST, "${twst}")
    field(TWSV, "${twsv}")
    field(THVL, "${thvl}")
    field(THST, "${thst}")
    field(THSV, "${thsv}")
    field(FRVL, "${frvl}")
    field(FRST, "${frst}")
    field(FRSV, "${frsv}")
    field(FVVL, "${fvvl}")
    field(FVST, "${fvst}")
    field(FVSV, "${fvsv}")
    field(SXVL, "${sxvl}")
    field(SXST, "${sxst}")
    field(SXSV, "${sxsv}")
    field(SVVL, "${svvl}")
    field(SVST, "${svst}")
    field(SVSV, "${svsv}")
    field(EIVL, "${eivl}")
    field(EIST, "${eist}")
    field(EISV, "${eisv}")
    field(NIVL, "${nivl}")
    field(NIST, "${nist}")
    field(NISV, "${nisv}")
    field(TEVL, "${tevl}")
    field(TEST, "${test}")
    field(TESV, "${tesv}")
    field(ELVL, "${elvl}")
    field(ELST, "${elst}")
    field(ELSV, "${elsv}")
    field(TVVL, "${tvvl}")
    field(TVST, "${tvst}")
    field(TVSV, "${tvsv}")
    field(TTVL, "${ttvl}")
    field(TTST, "${ttst}")
    field(TTSV, "${ttsv}")
    field(FTVL, "${ftvl}")
    field(FTST, "${ftst}")
    field(FTSV, "${ftsv}")
    field(FFVL, "${ffvl}")
    field(FFST, "${ffst}")
    field(FFSV, "${ffsv}")
}
"""
)

mbbi_template = Template(
    """
record(ai, "${auxname}1"){
    field(DTYP, "EtherIP")
    field(INP, "@$(PLC) ${tag} S ${scan}")
    field(SCAN, "I/O Intr")
    field(FLNK, "${name}")
}

record(mbbi, "${name}"){
    field(INP, "${auxname}1")
    field(DESC, "${desc}")
    field(SHFT, "${shft}")
    field(UNSV, "${unsv}")
    field(COSV, "${cosv}")
    field(ZRVL, "${zrvl}")
    field(ZRST, "${zrst}")
    field(ZRSV, "${zrsv}")
    field(ONVL, "${onvl}")
    field(ONST, "${onst}")
    field(ONSV, "${onsv}")
    field(TWVL, "${twvl}")
    field(TWST, "${twst}")
    field(TWSV, "${twsv}")
    field(THVL, "${thvl}")
    field(THST, "${thst}")
    field(THSV, "${thsv}")
    field(FRVL, "${frvl}")
    field(FRST, "${frst}")
    field(FRSV, "${frsv}")
    field(FVVL, "${fvvl}")
    field(FVST, "${fvst}")
    field(FVSV, "${fvsv}")
    field(SXVL, "${sxvl}")
    field(SXST, "${sxst}")
    field(SXSV, "${sxsv}")
    field(SVVL, "${svvl}")
    field(SVST, "${svst}")
    field(SVSV, "${svsv}")
    field(EIVL, "${eivl}")
    field(EIST, "${eist}")
    field(EISV, "${eisv}")
    field(NIVL, "${nivl}")
    field(NIST, "${nist}")
    field(NISV, "${nisv}")
    field(TEVL, "${tevl}")
    field(TEST, "${test}")
    field(TESV, "${tesv}")
    field(ELVL, "${elvl}")
    field(ELST, "${elst}")
    field(ELSV, "${elsv}")
    field(TVVL, "${tvvl}")
    field(TVST, "${tvst}")
    field(TVSV, "${tvsv}")
    field(TTVL, "${ttvl}")
    field(TTST, "${ttst}")
    field(TTSV, "${ttsv}")
    field(FTVL, "${ftvl}")
    field(FTST, "${ftst}")
    field(FTSV, "${ftsv}")
    field(FFVL, "${ffvl}")
    field(FFST, "${ffst}")
    field(FFSV, "${ffsv}")
}
"""
)

