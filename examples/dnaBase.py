#!/usr/bin/env python
from rlp.sedes import big_endian_int, binary, Binary
from rlp import Serializable
from Cryptodome.Hash import keccak

def sha3_256(x): return keccak.new(digest_bits=256, data=x.encode()).digest()

address = Binary.fixed_length(20, allow_empty=True)

def sha3(seed):
    return sha3_256(str(seed))


class Transaction(Serializable):
    fields = [
        ('nonce', big_endian_int),
        ('epoch', big_endian_int),
        ('txtype', big_endian_int),
        ('to', address),
        ('value', big_endian_int),
        ('maxfee', big_endian_int),
        ('tips', big_endian_int),
        ('data', binary),
    ]

    def __init__(self, nonce, epoch, txtype, to, value, maxfee, tips, data):
        super(Transaction, self).__init__(
            nonce,
            epoch,
            txtype,
            to,
            value,
            maxfee,
            tips,
            data,
        )

class UnsignedTransaction(Serializable):
    fields = [
        ('nonce', big_endian_int),
        ('epoch', big_endian_int),
        ('txtype', big_endian_int),
        ('to', address),
        ('value', big_endian_int),
        ('maxfee', big_endian_int),
        ('tips', big_endian_int),
        ('data', binary),
    ]

def unsigned_tx_from_tx(tx):
    return UnsignedTransaction(
        nonce=tx.nonce,
        epoch=tx.epoch,
        txtype=tx.txtype,
        to=tx.to,
        value=tx.value,
        maxfee=tx.maxfee,
        tips=tx.tips,
        data=tx.data,
    )
