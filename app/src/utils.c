#include <stdint.h>
#include <string.h>

#include "dnaUstream.h"
#include "uint256.h"

static const unsigned char hex_digits[] = {'0', '1', '2', '3', '4', '5', '6', '7',
                                           '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

void array_hexstr(char *strbuf, const void *bin, unsigned int len) {
    while (len--) {
        *strbuf++ = hex_digits[((*((char *)bin)) >> 4) & 0xF];
        *strbuf++ = hex_digits[(*((char *)bin)) & 0xF];
        bin = (const void *)((unsigned int)bin + 1);
    }
    *strbuf = 0; // EOS
}

void convertUint256BE(uint8_t *data, uint32_t length, uint256_t *target) {
    uint8_t tmp[32];
    os_memset(tmp, 0, 32);
    os_memmove(tmp + 32 - length, data, length);
    readu256BE(tmp, target);
}

int local_strchr(char *string, char ch) {
    unsigned int length = strlen(string);
    unsigned int i;
    for (i=0; i<length; i++) {
        if (string[i] == ch) {
            return i;
        }
    }
    return -1;
}

uint32_t getV(txContent_t *txContent) {
    uint32_t v = 0;
    if (txContent->vLength == 1) {
      v = txContent->v[0];
    }
    else
    if (txContent->vLength == 2) {
      v = (txContent->v[0] << 8) | txContent->v[1];
    }
    else
    if (txContent->vLength == 3) {
      v = (txContent->v[0] << 16) | (txContent->v[1] << 8) | txContent->v[2];
    }
    else
    if (txContent->vLength == 4) {
      v = (txContent->v[0] << 24) | (txContent->v[1] << 16) |
          (txContent->v[2] << 8) | txContent->v[3];
    }
    else
    if (txContent->vLength != 0) {
        PRINTF("Unexpected v format\n");
        THROW(EXCEPTION);
    }
    return v;
}