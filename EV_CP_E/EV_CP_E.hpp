#pragma once

enum class CPState : uint8_t {
	ACTIVE,
	OUT_OF_ORDER,
	CHARGING,
	BROKEN,
	DISCONNECTED
};