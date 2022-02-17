#include "uart.h"

/*Global volatile variables for this file*/
volatile static uint8_t uart_tx_active = 1;
volatile static uint8_t rx_buf[RX_BUF_SZ] = {0};
volatile static uint16_t rx_count = 0;

/* Recv interrupt */
ISR(USART_RX_vect)
{
  volatile static uint16_t rx_write_pos = 0;

  rx_buf[rx_write_pos] = UDR0;
  rx_count++;
  if (rx_write_pos >= RX_BUF_SZ)
  {
    rx_write_pos = 0; 
  }

}
/* Transf interrupt */
ISR(USART_TX_vect)
{
  uart_tx_active = 1;

}

void uart_init(void)
{
#if SPEED2X
    UCSR0A |= 1 << U2X0;
#else
    UCSR0A &= ~(1 << U2X0);
#endif 
 /* Baud rate helpers (set baud.h) */
  UBRR0H = UBRRH_VALUE;
  UBRR0L = UBRRL_VALUE;

  UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0) | (1 << TXCIE0);

}

void uart_send_byte(uint8_t c)
{
  while (!uart_tx_active);
  uart_tx_active = 0;
  UDR0 = c;
}

void uart_send_arr(char *c, uint16_t len)
{
  for (uint16_t i = 0; i < len; i++)
  {
    uart_send_byte(c[i]);
  }
}

void uart_send_str(uint8_t *c)
{
  uint16_t i = 0;
  do 
  {
    uart_send_byte(c[i]);
    i++;
  } while (c[i] != '\0'); 
}

uint16_t uart_read_count(void)
{
  return rx_count;
}

uint8_t uart_read(void)
{
  static uint16_t rx_read_pos = 0;
  uint8_t data = 0;
  data = rx_buf[rx_read_pos];
  rx_read_pos++;
  rx_count--;
  if (rx_read_pos)
  {
    rx_read_pos = 0;
  }
  return data;
}
