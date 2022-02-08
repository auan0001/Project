FILENAME   = main
HEADER1		 = onewire
HEADER2		 = uart
F_CPU = 16000000
PORT       = /dev/ttyUSB0
DEVICE     = atmega328p
PROGRAMMER = avrisp
BAUD       = 57600 
COMPILE    = avr-gcc -Wall -Os -mmcu=$(DEVICE) -DF_CPU=$(F_CPU) -I$(INCLUDE)
INCLUDE		 = ./include


default: compile upload clean

compile:
	$(COMPILE) -c $(FILENAME).c -o obj/$(FILENAME).o
	$(COMPILE) -c $(HEADER1).c -o obj/$(HEADER1).o
	$(COMPILE) -c $(HEADER2).c -o obj/$(HEADER2).o
	$(COMPILE) -o $(FILENAME).elf obj/$(FILENAME).o obj/$(HEADER1).o obj/$(HEADER2).o
	avr-objcopy -j .text -j .data -O ihex $(FILENAME).elf $(FILENAME).hex 
	avr-size --format=avr --mcu=$(DEVICE) $(FILENAME).elf

upload:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -b $(BAUD) -U flash:w:$(FILENAME).hex:i

clean:
	rm obj/*.o
	rm *.o
	rm $(FILENAME).elf
	rm $(FILENAME).hex
