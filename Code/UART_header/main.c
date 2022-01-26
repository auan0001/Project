#include <stdint.h>
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "uart.h"

void main(void)
{
  uint8_t data = 'A';

  uart_init();
  sei();

  while(1)
  {
    uart_send_byte(data);
    _delay_ms(500);
    data++;
    if (data > 'Z') {
      data = 'A';
    }
  }
}
