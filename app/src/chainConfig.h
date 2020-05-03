#ifndef _CHAIN_CONFIG_H_
#define _CHAIN_CONFIG_H_

#include <stdint.h>

#include "os.h"

typedef enum chain_kind_e {
	CHAIN_KIND_IDENA,
} chain_kind_t;

typedef struct chain_config_s {
	const char* coinName; // ticker
	uint32_t chainId;
	chain_kind_t kind;
#ifdef TARGET_BLUE
    const char* header_text;
    unsigned int color_header;
    unsigned int color_dashboard;
#endif // TARGET_BLUE

} chain_config_t;

#endif /* _CHAIN_CONFIG_H_ */
