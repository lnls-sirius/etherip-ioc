all: rf delta

sirius-temp: fcs-plc1-temp fcs-plc2-temp fcs-plc3-temp
fcs-plc1-temp:
	@echo "Sirius Temperature IOC from Fan Coils PLC number 1"
	./ioc_gen_temp.py \
       ../etc/SiriusAmbTempPVs.xlsx\
       --arch linux-x86_64 \
       --ioc-name sirius-amb-temp-ioc-1 \
       --plc-module 0 \
       --plc-name plc1 \
       --sheet 'plc1'

	sed -i -e  's/\n")/")/g' ../ioc/database/sirius-amb-temp-plc1.db


fcs-plc2-temp:
	@echo "Sirius Temperature IOC from Fan Coils PLC number 2"
	./ioc_gen_temp.py \
       ../etc/SiriusAmbTempPVs.xlsx\
       --arch linux-x86_64 \
       --ioc-name sirius-amb-temp-ioc-2 \
       --plc-module 0 \
       --plc-name plc1 \
       --sheet 'plc2'

	sed -i -e  's/\n")/")/g' ../ioc/database/sirius-amb-temp-plc2.db

fcs-plc3-temp:
	@echo "Sirius Temperature IOC from Fan Coils PLC number 3"
	./ioc_gen_temp.py \
       ../etc/SiriusAmbTempPVs.xlsx\
       --arch linux-x86_64 \
       --ioc-name sirius-amb-temp-ioc-3 \
       --plc-module 0 \
       --plc-name plc1 \
       --sheet 'plc3'

	sed -i -e  's/\n")/")/g' ../ioc/database/sirius-amb-temp-plc3.db
