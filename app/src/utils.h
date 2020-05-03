#ifndef _UTILS_H_
#define _UTILS_H_

#include <stdint.h>

#include "uint256.h"

void array_hexstr(char *strbuf, const void *bin, unsigned int len);

void convertUint256BE(uint8_t *data, uint32_t length, uint256_t *target);

int local_strchr(char *string, char ch);

uint32_t getV(txContent_t *txContent);

#endif /* _UTILS_H_ */