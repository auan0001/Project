#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#define F_CPU 16000000UL
#define __AVR_ATmega328p__
#define BAUD 9600
#define BRC ((F_CPU/16/BAUD)-1)
#define TX_BUF_SZ 128
char serialBuf[TX_BUF_SZ];
uint8_t serialReadPos = 0;
uint8_t serialWritePos = 0;

void appendSerial(char c);
void serialWrite(char c[]);

void main(void)
{
  UBRR0H = (BRC >> 8);
  UBRR0L = BRC;

  UCSR0B = (1 << TXEN0) | (TXCIE0);
  UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
  sei();

  serialWrite("ABBE\n\r");
  serialWrite("63...\n\r");
  _delay_ms(1500);
  while(1){

  }
  //while(1){UDR0 = 'A'; _delay_ms(1000);}
}

void appendSerial(char c)
{
}

void serialWrite(char c[])
{
  for (uint8_t i = 0; i < strlen(c); i++)
  {
   appendSerial(c[i]);
  }

  if (UCSR0A & (1 << UDRE0))
  {
    UDR0=0;
  }
}

ISR(USART_TX_Vect)
{
  if (serialReadPos!=serialWritePos)
  {
    UDR0 = serialBuf[serialReadPos];
    serialReadPos++;
  }
  if (serialReadPos >= TX_BUF_SZ)
  {
    serialReadPos++;
  }
}
