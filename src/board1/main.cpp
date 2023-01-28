#include <Arduino.h>

#include "common/firmware_hash.h"
#include "libfile.h"

#include "board1/board1.h"

void board1_function()
{
	board1_t board1;
	board1.id = COMMON_DEFINE;

	return;
}

void setup()
{
	Serial.begin(9600);

	lib_function();
}

void loop()
{
	Serial.print("Firmware hash: ");
	Serial.println(FIRMWARE_HASH);

	board1_function();
	delay(200);
}