====================
 Reed Solomon Armor
====================

This is a small utility for converting binary files into lines of
hexadecimal digits, with the added benefit of having some error
correction. I find it particularly useful for making printouts of
critical stuff like the metadata of my LUKS partitions, or private
encryption keys.

The error correction is useful, if you are a sloppy typer, or if you
have issues with your OCR software.

If you run this program without any arguments, it will work as a
traditional UNIX pipe, but if you want to have more control over what
is does, you can make it behave differently using the following
command line arguments::

  Usage: rsarm [options]
  
  Options:
    -h, --help            show this help message and exit
    -e, --encode          Encode the input [default]
    -d, --decode          Decode the input
    -i INPUT, --input=INPUT
                          Input file [stdin]
    -o OUTPUT, --output=OUTPUT
                          Output file [stdout]
    -l L                  Original block size [20]
    -n N                  Encoded block size [24]

If you're more of the programming kind, you can also call the encoding
and decoding routines directly:

  >>> from rsarm import rsarm
  >>> d = """Beautiful is better than ugly.
  ... Explicit is better than implicit."""

  >>> e = rsarm.encode(d)
  >>> print e
  426561 757469   66756c 206973   206265 747465   7220c7 970213
  746861 6e2075   676c79 2e0a45   78706c 696369   74206f 5ec2e0
  697320 626574   746572 207468   616e20 696d70   6c69e8 b82f7f
  636974 2e0000   000000 000000   000000 000000   0004f7 794587
  <BLANKLINE>

  >>> print rsarm.decode(e)
  Beautiful is better than ugly.
  Explicit is better than implicit.

So far so good! Now, we'll change the first byte, to see that the
error correction works::

  >>> e = '3' + e[1:]
  >>> import sys
  >>> from StringIO import StringIO
  >>> old_stderr, sys.stderr = sys.stderr, StringIO()
  >>> print rsarm.decode(e)
  Beautiful is better than ugly.
  Explicit is better than implicit.

We also get a meaningful hint on stderr:  
  >>> print sys.stderr.getvalue(),
  Found recoverable error in line 1, byte(s) [0]

  >>> sys.stderr.truncate(0)

With the current parameters `l` and `n` we can even break two bytes::

  >>> e = '333' + e[3:]
  >>> print rsarm.decode(e)
  Beautiful is better than ugly.
  Explicit is better than implicit.

Once again, we get a meaningful hint on stderr. 
  >>> print sys.stderr.getvalue(),
  Found recoverable error in line 1, byte(s) [0, 1]
  >>> sys.stderr.truncate(0)

However, breaking three bytes is too much:
  >>> e = '33333' + e[5:]
  >>> print rsarm.decode(e)
  Traceback (most recent call last):
  ...
  UncorrectableError: Too many errors or erasures in input

Note that stderr gives a line number:
  >>> print sys.stderr.getvalue(),
  Too many errors or erasures in line 1, giving up
  >>> sys.stderr.truncate(0)

  >>> sys.stderr = old_stderr

.. EOM
