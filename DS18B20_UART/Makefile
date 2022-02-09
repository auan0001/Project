# Makefile for ATmega328p written by August Forsman

FILENAME		= main
HEADER1			= onewire
HEADER2			= uart
F_CPU				= 16000000UL
PORT				= /dev/ttyUSB0
DEVICE			= atmega328p
PROGRAMMER 	= avrisp
BAUD				= 57600
CFLAGS				= -Wall -Os -ffreestanding
COMPILE			= avr-gcc $(CFLAGS) -mmcu=$(DEVICE) -DBAUD=$(BAUD) -DF_CPU=$(F_CPU) -I$(INCLUDE)
INCLUDE			= ./inc
OBJECTS			= obj/$(FILENAME).o obj/$(HEADER1).o obj/$(HEADER2).o


default: main.elf upload clean

$(FILENAME).elf: $(OBJECTS)
		$(COMPILE) -o $(FILENAME).elf $(OBJECTS)
		avr-objcopy -j .text -j .data -O ihex $(FILENAME).elf $(FILENAME).hex 
		avr-size --format=avr --mcu=$(DEVICE) $(FILENAME).elf

obj/$(FILENAME).o: src/$(FILENAME).c
	$(COMPILE) -c src/$(FILENAME).c -o obj/$(FILENAME).o
obj/$(HEADER1).o: src/$(HEADER1).c inc/$(HEADER1).h
	$(COMPILE) -c src/$(HEADER1).c -o obj/$(HEADER1).o
obj/$(HEADER2).o: src/$(HEADER2).c inc/$(HEADER2).h
	$(COMPILE) -c src/$(HEADER2).c -o obj/$(HEADER2).o

upload:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -b $(BAUD) -U flash:w:$(FILENAME).hex:i

.PHONY clean:
	rm obj/*.o
	rm $(FILENAME).elf
	rm $(FILENAME).hex
