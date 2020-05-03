#!/usr/bin/env python3
from __future__ import print_function

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
from decimal import Decimal
from dnaBase import sha3
from eth_keys import KeyAPI
import argparse
import struct
import binascii

# Define here Chain_ID
CHAIN_ID = 0

# Magic define
SIGN_MAGIC = b'\x19Idena Signed Message:\n'

def parse_bip32_path(path):
    if len(path) == 0:
        return b""
    result = b""
    elements = path.split('/')
    for pathElement in elements:
        element = pathElement.split('\'')
        if len(element) == 1:
            result = result + struct.pack(">I", int(element[0]))
        else:
            result = result + struct.pack(">I", 0x80000000 | int(element[0]))
    return result


parser = argparse.ArgumentParser()
parser.add_argument('--path', help="BIP 32 path to sign with")
parser.add_argument('--message', help="Message to sign", required=True)
args = parser.parse_args()

args.message = args.message.encode()

if args.path == None:
    args.path = "44'/515'/0'/0/0"

encodedTx = struct.pack(">I", len(args.message))
encodedTx += args.message

donglePath = parse_bip32_path(args.path)
apdu = bytearray.fromhex("e0080000")
apdu.append(len(donglePath) + 1 + len(encodedTx))
apdu.append(len(donglePath) // 4)
apdu += donglePath + encodedTx

dongle = getDongle(True)
result = dongle.exchange(bytes(apdu))

print("Result: ", ''.join('{:02x}'.format(x) for x in result))
