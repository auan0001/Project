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
  uint8_t data;
  uint16_t len = 8;
  char buffer[len];

  for(;;)
  {
    /* Polling for 'R' */
    if (uart_read_count() > 0)
    {
      data = uart_read();
      if (data == 'R') {
        ow_reset();
        ow_temp_rd(buffer);
        uart_send_arr(buffer, len);
        /*uart_send_byte('\r');*/
        uart_send_byte('\n');
      }
    }
  }
}
