#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include "DS18B20.h"

inline __attribute__((gnu_inline)) void therm_delay(uint16_t delay)
{
  while(delay--) asm volatile("nop");
}

uint8_t therm_reset()
{
  THERM_LOW();
  THERM_OUTPUT_MODE();
  _delay_us(480);

  THERM_INPUT_MODE();
  _delay_us(64);

  return ((THERM_PIN & (1 << THERM_DQ)) == 0) ? PRESENT : NOT_PRESENT;
}

void therm_write_bit(uint8_t bit)
{
  //Pull line low for 1uS
  THERM_LOW();
  THERM_OUTPUT_MODE();
  _delay_us(1);

  //If we want to write 1, release the line (if not will keep low)
  if(bit) THERM_INPUT_MODE();

  //Wait for 60uS and release the line
  _delay_us(60);
  THERM_INPUT_MODE();
}

uint8_t therm_read_bit(void)
{
  uint8_t bit=0;
  //Pull line low for 1uS
  THERM_LOW();
  THERM_OUTPUT_MODE();
  _delay_us(1);
  //Release line and wait for 14uS
  THERM_INPUT_MODE();
  _delay_us(14);
  //Read line value
  if(THERM_PIN&(1<<THERM_DQ)) bit=1;
  //Wait for 45uS to end and return read value
  _delay_us(45);
  return bit;
}

uint8_t therm_read_byte(void)
{
  uint8_t i=8, n=0;
  while(i--)
  {
    n >>= 1;
    n |= (therm_read_bit() << 7);
  }
  return n;
}

void therm_write_byte(uint8_t byte)
{
  uint8_t i = 8;
  while(i--)
  {
    therm_write_bit(byte & 1);
    byte >>= 1;
  }
}

void therm_read_temperature(char *buffer)
{
  // Buffer length must be at least 12bytes long! ["+XXX.XXXX C"]
  uint8_t temperature[2];
  int8_t digit;
  uint16_t decimal;
  //Reset, skip ROM and start temperature conversion
  therm_reset();
  therm_write_byte(THERM_CMD_SKIPROM);
  therm_write_byte(THERM_CMD_CONVERTTEMP);
  //Wait until conversion is complete
  while(!therm_read_bit());
  //Reset, skip ROM and send command to read Scratchpad
  therm_reset();
  therm_write_byte(THERM_CMD_SKIPROM);
  therm_write_byte(THERM_CMD_RSCRATCHPAD);
  //Read Scratchpad (only 2 first bytes)
  temperature[0]=therm_read_byte();
  temperature[1]=therm_read_byte();
  therm_reset();
  //Store temperature integer digits and decimal digits
  digit=temperature[0]>>4;
  digit|=(temperature[1]&0x7)<<4;
  //Store decimal digits
  decimal=temperature[0]&0xf;
  decimal*=THERM_DECIMAL_STEPS_12BIT;
  //Format temperature into a string [+XXX.XXXX C]
  sprintf(buffer, "%+d.%04u C", digit, decimal);
}
