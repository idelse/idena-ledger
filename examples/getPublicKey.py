#!/usr/bin/env python
from __future__ import print_function

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
import argparse
import struct
import binascii


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
parser.add_argument('--path', help="BIP 32 path to retrieve")
args = parser.parse_args()

if args.path == None:
    args.path = "44'/515'/0'/0/0"

donglePath = parse_bip32_path(args.path)
apdu = bytearray.fromhex("e0020100") + chr(len(donglePath) + 1).encode() + \
    chr(len(donglePath) // 4).encode() + donglePath

dongle = getDongle(True)
result = dongle.exchange(bytes(apdu))
offset = 1 + result[0]
address = result[offset + 1: offset + 1 + result[offset]]

print("Public key", binascii.hexlify(result[1: 1 + result[0]]).decode())
print("Address 0x", address.decode(), sep='')
