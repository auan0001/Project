#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "onewire.h"
#include "uart.h"

#define MSG_LEN_Y 17
#define MSG_LEN_N 14

void main(void)
{
  sei();
  uart_init();
  ow_reset();
  uint8_t stat;
  uint16_t len = 11;
  char buffer[len];

  for(;;)
  {
    ow_temp_rd(buffer);
    _delay_ms(500);
    uart_send_arr(buffer, len);
    uart_send_byte('\r');
    uart_send_byte('\n');
  }
}
