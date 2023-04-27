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

dbLoadRecords("database/${database}.db", "PLC=${plc}")
dbLoadRecords("database/${database}-Calc.db", "PLC=${plc}")
dbLoadRecords("database/${database}-Limits.db", "PLC=${plc},P=$(NAME)")
iocInit()

caPutLogInit "$(EPICS_IOC_CAPUTLOG_INET):$(EPICS_IOC_CAPUTLOG_PORT)" 2
"""
)

calcout_generic_template = Template(
    """
record(calcout, "${name}"){
    field(CALC, "${calc}")
    field(DESC, "${desc}")
    field(SCAN, "${scan}")
    field(INPA, "${inpa}")
    field(INPB, "${inpb}")
    field(INPC, "${inpc}")
    field(INPD, "${inpd}")
    field(INPE, "${inpe}")
    field(INPF, "${inpf}")
    field(INPG, "${inpg}")
    field(INPH, "${inph}")
    field(INPI, "${inpi}")
    field(INPJ, "${inpj}")
    field(INPK, "${inpk}")
    field(INPL, "${inpl}")
    field(FLNK, "${flnk}")
    field(OUT,  "${out} PP")
}
"""
)

bi_soft_channel_template = Template(
    """
record(bi, "${name}"){
    field(INP, "${inp} ${inp_type}")
    field(DESC, "${desc}")
    field(SCAN, "${scan}")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
}
"""
)

bo_soft_channel_template = Template(
    """
record(bo, "${name}"){
    field(OUT, "${out} ${out_type}")
    field(DESC, "${desc}")
    field(SCAN, "${scan}")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
}
"""
)

ai_template = Template(
    """
record(ai, "${name}"){
    field(DTYP, "EtherIP")
    field(INP,  "@$(PLC) ${tag}")
    field(DESC, "${desc}")
    field(SCAN, "${scan} second")
    field(PREC, "${prec}")
    field(EGU,  "${egu}")
}
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
}
"""
)

ao_template_closed_loop = Template(
    """
record(ao, "${name}"){
    field(OMSL, "closed_loop")
    field(DOL,  "${name_in} CP")
    field(DESC, "${desc}")
    field(EGU,  "${egu}")
}
"""
)

calcout_template_field = Template(
    """
record(calcout, "${name}"){
    field(CALC, "A${offset}")
    field(INPA, "${name_clp} CP")
    field(OUT,  "${name_target}.${field} PP")
}
"""
)

bo_template = Template(
    """
record(bo, "${name}"){
    field(DTYP, "EtherIP")
    field(OUT, "@$(PLC) ${tag} S .1")
    field(DESC, "${desc}")
    field(SCAN, "Passive")
    field(ONAM, "${onam}")
    field(ZNAM, "${znam}")
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
}
"""
)
