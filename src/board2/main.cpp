#include <Arduino.h>

#include "board2/board2.h"

void board2_function()
{
	board2_t board2 { .id = 2 };
	return;
}

void setup() { }

void loop()
{
	board2_function();
}