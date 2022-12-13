TOP = ../..
include $(TOP)/configure/CONFIG
ARCH = $(EPICS_HOST_ARCH)
TARGETS = envPaths
TARGETS += logEnvCreate
logEnvCreate:
	envsubst < logEnv.tmplt > logEnv

include $(TOP)/configure/RULES.ioc
