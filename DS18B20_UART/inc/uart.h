#ifndef UART_H_
#define UART_H_
/* TODO get rid of this redefenition */
#define BAUD 9600
#include <avr/io.h>
#include <util/delay.h>
#include <util/setbaud.h>
#include <avr/interrupt.h>

void uart_init(void);
void uart_send_byte(uint8_t c);
void uart_send_str(uint8_t *c);
void uart_send_arr(char *c, uint16_t len);

#endif /* ifndef UART_H_ */
