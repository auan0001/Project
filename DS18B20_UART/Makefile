FILENAME   = main
HEADER1		 = onewire
HEADER2		 = uart
F_CPU = 16000000UL
PORT       = /dev/ttyUSB0
DEVICE     = atmega328p
PROGRAMMER = avrisp
BAUD       = 57600
FLAGS			 = -Wall -Os -ffreestanding
COMPILE    = avr-gcc $(FLAGS) -mmcu=$(DEVICE) -DBAUD=$(BAUD) -DF_CPU=$(F_CPU) -I$(INCLUDE)
INCLUDE		 = ./inc

default: compile upload clean

compile:
	$(COMPILE) -c src/$(FILENAME).c -o obj/$(FILENAME).o
	$(COMPILE) -c src/$(HEADER1).c -o obj/$(HEADER1).o
	$(COMPILE) -c src/$(HEADER2).c -o obj/$(HEADER2).o
	$(COMPILE) -o $(FILENAME).elf obj/$(FILENAME).o obj/$(HEADER1).o obj/$(HEADER2).o
	avr-objcopy -j .text -j .data -O ihex $(FILENAME).elf $(FILENAME).hex 
	avr-size --format=avr --mcu=$(DEVICE) $(FILENAME).elf

upload:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -b $(BAUD) -U flash:w:$(FILENAME).hex:i

clean:
	rm obj/*.o
	rm $(FILENAME).elf
	rm $(FILENAME).hex
