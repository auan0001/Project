#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#define F_CPU 16000000UL
#define __AVR_ATmega328p__
#define BAUD 9600
#define BRC ((F_CPU/16/BAUD)-1)
#define TX_BUF_SZ 128
char serBuf[TX_BUF_SZ];
uint8_t serReadPos = 0;
uint8_t serWritePos = 0;

void appendSer(char c);
void serWrite(char c[]);

void main(void)
{
  UBRR0H = (BRC >> 8);
  UBRR0L = BRC;

  UCSR0B = (1 << TXEN0) | (TXCIE0);
  UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
  sei();

  serWrite("ABBE\n\r");
  serWrite("63...\n\r");
  _delay_ms(1500);
  while(1){

  }
  //while(1){UDR0 = 'A'; _delay_ms(1000);}
}

void appendSer(char c)
{
  serBuf[serWritePos] = c;
  serWritePos++;

  if (serWritePos >= TX_BUF_SZ)
  {
    serWritePos = 0;
  }
}

void serWrite(char c[])
{
  for (uint8_t i = 0; i < strlen(c); i++)
  {
   appendSer(c[i]);
  }

  if (UCSR0A & (1 << UDRE0))
  {
    UDR0=0;
  }
}

ISR(USART_TX_Vect)
{
  if (serReadPos!=serWritePos)
  {
    UDR0 = serBuf[serReadPos];
    serReadPos++;
  }
  if (serReadPos >= TX_BUF_SZ)
  {
    serReadPos++;
  }
}