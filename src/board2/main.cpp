#include <Arduino.h>

#include "common/firmware_hash.h"
#include "libfile.h"

#include "board2/board2.h"

void board2_function()
{
	board2_t board2;
	board2.id = COMMON_DEFINE;

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

	board2_function();
	delay(200);
}