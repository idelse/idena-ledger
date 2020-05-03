#!/usr/bin/env python
from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
import argparse
import struct


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
    args.path = "44'/60'/0'/0/0"

donglePath = parse_bip32_path(args.path)
apdu = bytearray.fromhex("e0060000") + chr(len(donglePath) + 1).encode() + \
    chr(len(donglePath) // 4).encode() + donglePath

dongle = getDongle(True)
dongle.exchange(bytes(apdu))
