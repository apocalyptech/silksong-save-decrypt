#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Python Silksong Save Decrypter/Encrypter
# Copyright (c) 2025, CJ Kucera
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the development team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CJ KUCERA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import json
import base64
import argparse
import Crypto.Cipher.AES
import Crypto.Util.Padding


# Format gleaned from https://github.com/bloodorca/hollow/blob/489b2d313953a6b54e49b9b8633657c9baee7bd0/src/functions.js
# ... though there are plenty of other examples out there besides that one.
#
# Also, it appears that this might be identical to how the original Hollow Knight stores
# its savegames, so it might work perfectly well on the original game, too.


header = bytes([0, 1, 0, 0, 0, 255, 255, 255, 255, 1, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0])
footer = bytes([11])
key = b'UKu52ePUBwetZ9wNX88o54dnfKRu0T1l'
cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_ECB)


def decrypt(filename):

    global header, footer, cipher

    with open(filename, 'rb') as df:
        data = df.read()

    # Strip out our header and footer
    assert(data[:len(header)] == header)
    assert(data[-len(footer):] == footer)
    data = data[len(header):-len(footer)]

    # Data is prefixed by a varint decribing the length of the data
    data_start = 0
    data_len = 0
    while True:
        this_data = data[data_start]
        data_len += ((this_data & 0x7F) << (7*data_start))
        data_start += 1
        if this_data & 0x80 == 0:
            break
    data = data[data_start:]
    assert(len(data) == data_len)

    # Now un-base64, un-encrypt, and un-pad
    data = base64.b64decode(data)
    data = cipher.decrypt(data)
    return Crypto.Util.Padding.unpad(data, 16)


def encrypt(filename):

    global header, footer, cipher

    # Read in JSON and de-prettify it
    with open(filename) as df:
        data = json.load(df)
    data = json.dumps(data, separators=(',', ':'))

    # Pad, encrypt, and base64
    data = Crypto.Util.Padding.pad(data.encode('utf-8'), 16)
    data = cipher.encrypt(data)
    data = base64.b64encode(data)

    # Construct a new varint for the length
    varint = []
    data_len = len(data)
    while data_len > 0:
        if data_len > 127:
            varint.append(0x80 | (data_len & 0x7F))
        else:
            varint.append(data_len)
        data_len >>= 7

    # Final data
    return header + bytes(varint) + data + footer


def main():

    parser = argparse.ArgumentParser(
            description='Encrypt/Decrypt Silksong (and possibly Hollow Knight) Savegames (PC Only)',
            )

    parser.add_argument('-f', '--force',
            action='store_true',
            help='Force overwrite of output file, if it already exists',
            )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-e', '--encrypt',
            action='store_true',
            help='Encrypt savegame',
            )

    group.add_argument('-d', '--decrypt',
            action='store_true',
            help='Decrypt savegame (will write a JSON file)',
            )

    parser.add_argument('input',
            type=str,
            help='Input filename',
            )

    parser.add_argument('output',
            type=str,
            help='Output filename',
            )

    args = parser.parse_args()

    if not args.force and os.path.exists(args.output):
        print('')
        print(f'WARNING: {args.output} already exists!')
        resp = input('Overwrite [y/N]? ').strip()
        if len(resp) == 0 or resp[0].casefold() != 'y':
            sys.exit(1)

    if args.decrypt:
        data = decrypt(args.input)
        # May as well save as pretty-printed JSON
        data = json.loads(data)
        with open(args.output, 'w') as odf:
            json.dump(data, odf, indent=4)
        print(f'Wrote decrypted data to: {args.output}')

    elif args.encrypt:
        data = encrypt(args.input)
        with open(args.output, 'wb') as odf:
            odf.write(data)
        print(f'Wrote encrypted data to: {args.output}')


if __name__ == '__main__':
    main()

