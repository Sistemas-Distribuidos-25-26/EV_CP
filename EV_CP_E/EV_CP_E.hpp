#pragma once

enum class CPState : uint8_t {
	UNKNOWN,
	ACTIVE = 1,
	OUT_OF_ORDER,
	CHARGING,
	BROKEN,
	DISCONNECTED
};