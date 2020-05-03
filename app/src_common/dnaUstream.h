#ifndef _DNAUSTREAM_H_
#define _DNAUSTREAM_H_

#include <stdbool.h>
#include <stdint.h>

#include "os.h"
#include "cx.h"

struct txContext_t;

typedef enum customStatus_e {
    CUSTOM_NOT_HANDLED,
    CUSTOM_HANDLED,
    CUSTOM_SUSPENDED,
    CUSTOM_FAULT
} customStatus_e;

typedef customStatus_e (*ustreamProcess_t)(struct txContext_t *context);

#define TX_FLAG_TYPE 0x01

typedef enum rlpTxField_e {
    TX_RLP_NONE = 0,
    TX_RLP_CONTENT,
    TX_RLP_TYPE,
    TX_RLP_NONCE,
    TX_RLP_EPOCH,
    TX_RLP_TXTYPE,
    TX_RLP_TO,
    TX_RLP_VALUE,
    TX_RLP_MAXFEE,
    TX_RLP_TIPS,
    TX_RLP_DATA,
    TX_RLP_V,
    TX_RLP_R,
    TX_RLP_S,
    TX_RLP_DONE
} rlpTxField_e;

typedef enum parserStatus_e {
    USTREAM_PROCESSING,
    USTREAM_SUSPENDED,
    USTREAM_FINISHED,
    USTREAM_FAULT
} parserStatus_e;

typedef struct txInt256_t {
    uint8_t value[32];
    uint8_t length;
} txInt256_t;

typedef struct txContent_t {
    txInt256_t nonce;
    txInt256_t epoch;
    txInt256_t txtype;
    uint8_t destination[20];
    uint8_t destinationLength;
    txInt256_t value;
    txInt256_t maxfee;
    txInt256_t tips;
    uint8_t v[4];
    uint8_t vLength;
} txContent_t;

typedef struct txContext_t {
    rlpTxField_e currentField;
    cx_sha3_t *sha3;
    uint32_t currentFieldLength;
    uint32_t currentFieldPos;
    bool currentFieldIsList;
    bool processingField;
    bool fieldSingleByte;
    uint32_t dataLength;
    uint8_t rlpBuffer[5];
    uint32_t rlpBufferPos;
    uint8_t *workBuffer;
    uint32_t commandLength;
    uint32_t processingFlags;
    ustreamProcess_t customProcessor;
    txContent_t *content;
    void *extra;
} txContext_t;

void initTx(txContext_t *context, cx_sha3_t *sha3, txContent_t *content,
            ustreamProcess_t customProcessor, void *extra);
parserStatus_e processTx(txContext_t *context, uint8_t *buffer,
                         uint32_t length, uint32_t processingFlags);
parserStatus_e continueTx(txContext_t *context);
void copyTxData(txContext_t *context, uint8_t *out, uint32_t length);
uint8_t readTxByte(txContext_t *context);

#endif /* _DNAUSTREAM_H_ */