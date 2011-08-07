#  Copyright 2011 C.J. Spaans <j@jasper.es>
#
#  This file is part of rsarm.
#
#  rsarm is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  rsarm is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with rsarm.  If not, see <http://www.gnu.org/licenses/>.

import optparse
from itertools import chain, ifilter

import reedsolomon

from .utils import read_stream, window

def chunkify(s, l=32):
    """Convert the input strings s into chunks of length l, padding them"""
    if l > 256:
        raise ValueError("Chunksize is currently limited to 256 characters.")

    did_padding = False
    for w in map(''.join, window(s, l, l)):
        if not len(w)==l:
            yield padded(w, l)
            did_padding = True
        else:
            yield [ ord(c) for c in w ]
    if not did_padding:
        yield padded('', l)


def padded(s, l):
    """pads the sequence s to length l, using null bytes. return a
    list of ascii values, not a string"""

    o_s = [ ord(c) for c in s ]
    if (l > 256):
        raise ValueError("Chunksize is currently limited to 256 characters.")
    nulls = [ 0 ] * (l - (len(s) + 1))
    padchar = [ len(o_s) ]
    return o_s + nulls + padchar

def unpadded(chunk):
    l = ord(chunk[-1])
    return chunk[0:l]

import sys
def encode(i, l=20, n=24):

    codec = reedsolomon.IntegerCodec(n, l, 8)

    ochunks = []
    for lnum, chunk in enumerate(chunkify(i, l)):
        echunk = codec.encode(chunk)
        l = ("".join(c) for c in window(("%02x" % c for c in echunk), 3))
        l1 = (" ".join(c) for c in window(l, 2))
        l2 = "   ".join(l1)
        ochunks.append(l2+"\n")
    return ''.join(ochunks)

def decode(i, l=20, n=24):
    codec = reedsolomon.IntegerCodec(n, l, 8)
    hexchars = "0123456789abcdefABCDEF"
    ochunks = []

    for line, echunk in enumerate(window(ifilter(hexchars.__contains__, i), n*2)):
        hexdigits = [int("".join(c), 16) for c in window(echunk, 2)]
        try:
            chunk, faults = codec.decode(hexdigits)
            if faults:
                print >> sys.stderr, "Found recoverable error in line %d, byte(s) %s" % (line + 1,  faults)
        except reedsolomon.UncorrectableError:
            print >> sys.stderr, "Too many errors or erasures in line %d, giving up" % (line + 1)
            raise
        ochunks.append([ chr(c) for c in chunk ])
    ochunks[-1] = unpadded(ochunks[-1])
    return ''.join(chain(*ochunks))

def options_setup():
    parser = optparse.OptionParser()
    parser.add_option("-e" ,"--encode", action="store_true", dest="encode", default=True, help="Encode the input [default]")
    parser.add_option("-d" ,"--decode", action="store_false", dest="encode", default=True, help="Decode the input")
    parser.add_option("-i", "--input", action="store", dest="input", default=None, help="Input file [stdin]")
    parser.add_option("-o", "--output", action="store", dest="output", default=None, help="Output file [stdout]")

    parser.add_option("-l", action="store", type="int", dest="l", default=20, help="Original block size [%default]")
    parser.add_option("-n", action="store", type="int", dest="n", default=24, help="Encoded block size [%default]")

    return parser

def main():
    options, args = options_setup().parse_args()
    if not options.input:
        i = sys.stdin
    else:
        i = file(options.input, "r")
    if not options.output:
        o = sys.stdout
    else:
        o = file(options.output, "w")

    l = options.l
    n = options.n

    data = read_stream(i)

    if options.encode:
        o.write(encode(data, l, n))
    else:
        try:
            o.write(decode(data, l, n))
        except reedsolomon.UncorrectableError:
            sys.exit(-1)

if __name__ == '__main__':
    main()
