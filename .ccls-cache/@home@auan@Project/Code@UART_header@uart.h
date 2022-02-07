#ifndef UART_H_
#define UART_H_
#define RX_BUF_SZ 12

#include "avrconf.h"
#include <avr/io.h>
#include <util/delay.h>
#include <util/setbaud.h>
#include <avr/interrupt.h>

void uart_init(void);
void uart_send_byte(uint8_t c);
void uart_send_str(uint8_t *c);
void uart_send_arr(uint8_t *c, uint16_t len);
uint16_t uart_read_count(void);
uint8_t uart_read(void);

#endif /* ifndef UART_H_ */
