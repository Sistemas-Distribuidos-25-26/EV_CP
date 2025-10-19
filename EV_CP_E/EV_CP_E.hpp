#pragma once

enum class CPState : uint8_t {
	UNKNOWN,
	ACTIVE = 1,
	OUT_OF_ORDER,
	CHARGING,
	BROKEN,
	DISCONNECTED
};

float TOTAL_POWER = 50.0;
float PRICE = 0.34;