all: rf delta

linacskid:
	@echo "Linac Skid IOC"
	./ioc_gen_skids.py \
       ../etc/NewSkidPVs.xlsx\
       --arch linux-x86_64 \
       --ioc-name LinacSkid \
       --plc-module 0 \
       --plc-name plc1 \
       --sheet 'Linac'

	sed -i -e  's/\n")/")/g' ../ioc/database/LinacSkid.db

p5skid:
	@echo "Petra 5 Skid IOC"
	./ioc_gen_skids.py \
       ../etc/NewSkidPVs.xlsx\
       --arch linux-x86_64 \
       --ioc-name P5Skid \
       --plc-module 0 \
       --plc-name plc1 \
       --sheet 'Petra5'

	sed -i -e  's/\n")/")/g' ../ioc/database/P5Skid.db

p7skid:
	@echo "Petra 7 Skid IOC"
	./ioc_gen_skids.py \
       ../etc/NewSkidPVs.xlsx\
       --arch linux-x86_64 \
       --ioc-name P7Skid \
       --plc-module 0 \
       --plc-name plc1 \
       --sheet 'Revisado'

	sed -i -e  's/\n")/")/g' ../ioc/database/P7Skid.db


rf: rf-bo rf-si
rf-bo:
	@echo "RF Booster IOC"
	./ioc_gen_rf.py \
       ../etc/Booster_Interlock_EPICS_2.0.xlsx\
       --arch linux-x86_64 \
       --ioc-name RF-Booster \
       --plc-module 0 \
       --plc-name plc1 \
       --sheet 'SSAmp Tower,Interlock,Petra 5,LLRF,Transmission Line'

	sed -i -e  's/\n")/")/g' ../ioc/database/RF-Booster.db

rf-si:
	@echo "RF Ring IOC"
	./ioc_gen_rf.py \
       ../etc/'Storage Ring A Interlock EPICS.xlsx'\
       --arch linux-x86_64 \
       --ioc-name RF-Ring1 \
       --plc-module 0 \
       --plc-name plc1 \
       --sheet 'SSAmp Tower 01,SSAmp Tower 02,Petra 7,LLRF,Transmission Line'

delta:
	@echo "Delta Undulator IOC"
	./ioc_gen_delta.py \
            ../etc/Delta.xlsx \
            --arch linux-x86_64 \
            --ioc-name Delta \
            --plc-module 0 \
            --plc-name plc1 \
            --bi "Bit Input" \
            --bo "Bit Output" \
            --ai "Real Input" \
            --ao "Real Output" \
            --mbbi "Enum Input" \
            --mbbo "Enum Output" \
            --lsi "String Input" \
            --lso "String Output" \
            --sheet 'Delta'

delta-v2:
	@echo "Delta Undulator IOC v2"
	./ioc_gen_delta.py \
            ../etc/Delta_v2.xlsx \
            --arch linux-x86_64 \
            --ioc-name Delta_v2 \
            --plc-module 0 \
            --plc-name plc1 \
            --bi "Bit Input" \
            --bo "Bit Output" \
            --ai "Real Input" \
            --ao "Real Output" \
            --mbbi "Enum Input" \
            --mbbo "Enum Output" \
            --lsi "String Input" \
            --lso "String Output" \
            --sheet 'Global,Mod01,Mod02,Mod03'

clean:
	rm -rf __pycache__
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +
