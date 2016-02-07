# -*- coding: utf-8 -*-
import io
from .fields import getField, Unknown
from pydash.collections import filter_ as ifilter, partition, map_ as imap


def parseline(line):
    segs = line.split(":")

    # We could be in a multi-line value
    if len(segs) == 1:
        return None

    descriptors = segs[0].split(";")

    # No attributes with this field
    value = segs[1]

    # Seperate our field attributes from their name
    keys, attrs = partition(descriptors, lambda x: "=" not in x)
    key = keys[0]

    # Check for the existance of a subkey:
    subkey = None
    if "." in key:
        subkey, key = key.split(".")

    def normalizeAttr(item):
        key, value = item.split("=")
        return {key: value}

    attrs = imap(attrs, normalizeAttr)

    return subkey, key, attrs, value


class VCF(object):
    """docstring for VCF"""

    def __init__(self, fpath=None):
        super(VCF, self).__init__()
        self.fpath = fpath

        if fpath == None or type(fpath) != str:
            raise ValueError("A valid filepath must be provided")

        self.handle = io.open(self.fpath, "r", encoding="utf-8", newline="\r\n")

    def tokenize_lines(self):
        lineno = 0
        for line in self.readlines():
            parsed = parseline(line)

            if (parsed != None):
                subkey, key, attrs, value = parseline(line)
                t = getField(key)

                if t == None:
                    # We don't know what it is, process it later
                    t = Unknown(line, lineno=lineno)
                else:
                    t = t(value=value, attrs=attrs, lineno=lineno, subkey=subkey)

                yield t
            else:
                yield Unknown(line, lineno=lineno)

            lineno += 1

    def readlines(self):
        yield from self.handle

    def filterlines(self, fn=(lambda x: x)):
        for line in readlines(self):
            if fn(line):
                yield line
