PHONY: all rf rf-booster rf-ring clean

all: rf

rf: rf-bo rf-ring
rf-bo:
	@echo "RF Booster IOC"
	./ioc.py \
           ../etc/BOIlk \
           --arch linux-x86_64 \
           --ioc-name RF-Booster \
           --plc-module 0 \
           --plc-name plc1 \
           --sheet 'SSAmp Tower,Interlock,Petra 5,LLRF,Transmission Line'

	sed -i -e  's/\n")/")/g' ../database/RF-Booster.db
rf-ring:
	@echo "RF Ring IOC"
	./ioc.py \
            ../etc/SR1 \
            --arch linux-x86_64 \
            --ioc-name RF-Ring1 \
            --plc-module 0 \
            --plc-name plc1 \
            --sheet 'SSAmp Tower 01,SSAmp Tower 02,Interlock,Petra 7,LLRF,Transmission Line'

clean:
	 find . -name '*.pyc' -exec rm --force {} +
	 find . -name '*.pyo' -exec rm --force {} +
	 find . -name '*~' -exec rm --force  {} +