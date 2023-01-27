#pragma once

#include <stdint.h>

#error "Should fail"

#include "common_include.h"

typedef struct
{
	uint8_t id = COMMON_DEFINE;
} board1_t;

void board1_function();