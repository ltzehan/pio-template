#include <Arduino.h>

#include "libfile.h"

#include "board2/board2.h"

void board2_function()
{
	board2_t board2;
	board2.id = COMMON_DEFINE;
	board2.id++;

	return;
}

void setup()
{
	lib_function();
}

void loop()
{
	board2_function();
}