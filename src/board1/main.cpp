#include <Arduino.h>

#include "libfile.h"

#include "board1/board1.h"

void board1_function()
{
	board1_t board1 { .id = 1 };
	return;
}

void setup() { }

void loop()
{
	board1_function();
}