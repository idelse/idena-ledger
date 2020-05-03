#!/usr/bin/env python
from __future__ import print_function

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
from decimal import Decimal
import argparse
import struct
import binascii
from dnaBase import Transaction, UnsignedTransaction, unsigned_tx_from_tx
from rlp import encode

# Define here Chain_ID for EIP-155
CHAIN_ID = 0

try:
    from rlp.utils import decode_hex, encode_hex, str_to_bytes
except:
    #Python3 hack import for pyethereum
    from ethereum.utils import decode_hex, encode_hex, str_to_bytes

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
parser.add_argument('--nonce', help="Nonce associated to the account", type=int, required=True)
parser.add_argument('--epoch', help="Epoch", type=int, required=True)
parser.add_argument('--txtype', help="Type of transaction", type=int, required=True)
parser.add_argument('--to', help="Destination address", type=str, required=True)
parser.add_argument('--amount', help="Amount to send in ether", required=True)
parser.add_argument('--maxfee', help="Max Fee", required=True)
parser.add_argument('--tips', help="Tips", required=True)
parser.add_argument('--path', help="BIP 32 path to sign with")
parser.add_argument('--data', help="Data to add, hex encoded")
args = parser.parse_args()

if args.path == None:
    args.path = "44'/515'/0'/0/0"

if args.data == None:
    args.data = b""
else:
    args.data = decode_hex(args.data[2:])

amount = int(float(args.amount) * 10**18)
maxfee = int(float(args.maxfee) * 10**18)
tips = int(float(args.tips) * 10**18)

tx = Transaction(
    nonce=int(args.nonce),
    epoch=int(args.epoch),
    txtype=int(args.txtype),
    to=decode_hex(args.to[2:]),
    value=int(amount),
    maxfee=int(maxfee),
    tips=int(tips),
    data=args.data,
)

encodedTx = encode(tx, Transaction)

donglePath = parse_bip32_path(args.path)
apdu = bytearray.fromhex("e0040000")
apdu.append(len(donglePath) + 1 + len(encodedTx))
apdu.append(len(donglePath) // 4)
apdu += donglePath + encodedTx

dongle = getDongle(True)
result = dongle.exchange(bytes(apdu))

print("Result: ", ''.join('{:02x}'.format(x) for x in result))
