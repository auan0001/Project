#include "uart.h"
void uart_init(uint32_t baud, uint8_t high_speed)
{
  uint8_t speed = 16;
  if (high_speed != 0) {
    speed = 8;
    UCSR0A |= 1 << U2X0;
    
    
  }
}
