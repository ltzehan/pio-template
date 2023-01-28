#include <Arduino.h>

#include "common/firmware_hash.h"
#include "libfile.h"

#include "board1/board1.h"

void board1_function()
{
	board1_t board1 { .id = COMMON_DEFINE };
	Serial.println(FIRMWARE_HASH);
	Serial.println(board1.id);

	return;
}

void setup()
{
	lib_function();
}

void loop()
{
	board1_function();
}