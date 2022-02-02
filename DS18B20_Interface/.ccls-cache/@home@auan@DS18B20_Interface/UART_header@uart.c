#include "uart.h"

/*Never optimize this variable*/
volatile static uint8_t uart_tx_active = 1;

/* Recv interrupt */
ISR(USART_RX_vect)
{

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

void uart_send_arr(uint8_t *c, uint16_t len)
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
