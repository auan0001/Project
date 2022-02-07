#include </usr/avr/include/avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "uart.h"

#define CHARRSZ 8

void main(void)
{
  const uint16_t len = CHARRSZ;
  uint8_t carr[CHARRSZ] = "ABBE63\n";
  uart_init();
  sei();

  for(;;)
  {
    if (uart_read_count() > 0) {
      if (uart_read() == 'A') {
        _delay_ms(200);
        uart_send_arr(carr, len);
      }
    }
  }
}
