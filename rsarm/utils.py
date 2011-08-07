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

def window(seq, n=1, s=None):
    """walks over a sequence, returns a sequence of windowed views of
    the sequence, with window size n (defaults to one), and stride s
    (defaults to n)"""

    i = iter(seq)

    if s is None:
        s = n

    b = []
    try:
        for _ in xrange(n):
            b.append(i.next())
    except StopIteration:
        pass
    while True:
        yield b[:]
        try:
            for _ in range(s):
                b.append(i.next())
        except StopIteration:
            del b[:s]
            break
        del b[:s]
    if len(b):
        yield b[:]
        raise StopIteration()

def read_stream(s):
    while True:
        c = s.read(1)
        if c:
            yield c
        else:
            raise StopIteration()
