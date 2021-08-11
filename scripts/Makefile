all: rf delta

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
       --sheet 'SSAmp Tower 01,SSAmp Tower 02,Interlock,Petra 7,LLRF,Transmission Line'

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
            --lsi "String Input" \
            --lso "String Output" \
            --sheet 'Delta'

clean:
	rm -rf __pycache__
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +
