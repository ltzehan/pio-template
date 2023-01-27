#include <zephyr.h>

#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>

#include "common_include.h"

#define LED_DELAY_MS (COMMON_DEFINE * 250)

// LED GPIOs
#define RED_LED_NODE   DT_ALIAS(led2)
#define GREEN_LED_NODE DT_ALIAS(led0)
#define BLUE_LED_NODE  DT_ALIAS(led1)

static const struct gpio_dt_spec red_led = GPIO_DT_SPEC_GET(RED_LED_NODE, gpios);
static const struct gpio_dt_spec green_led = GPIO_DT_SPEC_GET(GREEN_LED_NODE, gpios);
static const struct gpio_dt_spec blue_led = GPIO_DT_SPEC_GET(BLUE_LED_NODE, gpios);

static const struct gpio_dt_spec leds[] = { red_led, green_led, blue_led };
#define NUM_LEDS (sizeof(leds) / sizeof(leds[0]))

void main(void)
{
	int ret;

	for (size_t i = 0; i < NUM_LEDS; i++) {
		const struct gpio_dt_spec led = leds[i];

		ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
		if (ret < 0)
			return;

		// Initialize with all LEDs off
		gpio_pin_set_dt(&led, 0);
	}

	size_t idx = 0;
	while (1) {
		const struct gpio_dt_spec led = leds[idx];

		gpio_pin_set_dt(&led, 1);
		k_msleep(LED_DELAY_MS);
		gpio_pin_set_dt(&led, 0);
		k_msleep(LED_DELAY_MS);

		idx++;
		if (idx >= NUM_LEDS)
			idx = 0;
	}
}