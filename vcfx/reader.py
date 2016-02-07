# -*- coding: utf-8 -*-
import io
from .fields import getField, Unknown
from pydash.collections import filter_ as ifilter, partition, map_ as imap
from itertools import takewhile

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


class Reader(object):
    def __init__(self, fpath=None):
        super(Reader, self).__init__()
        self.fpath = fpath

        if fpath == None or type(fpath) != str:
            raise ValueError("A valid filepath must be provided")

        self.handle = io.open(self.fpath, "r", encoding="utf-8", newline="\r\n")

        # A "virtual" AST, Doesn't store any data from the vcard,
        # just metadata (i.e lineno)
        self._vAST = list(self._discover_nodes())

        self.positions = {
            "begin":     0,
            "version":      self._get_node_position("VERSION"),
            "prodid":       self._get_node_position("PRODID"),
            "name":         self._get_node_position("N"),
            "fullname":     self._get_node_position("FN"),
            "organization": self._get_node_position("ORG"),
            "email":        self._get_node_positions("EMAIL"),
            "telephone":    self._get_node_positions("TEL"),
            "label":        self._get_node_positions("X-ABLabel"),
            "address":      self._get_node_positions("ADR"),
            "url":          self._get_node_positions("URL"),
            "altbirthday":  self._get_node_position("X-ALTBDAY"),
            "birthday":     self._get_node_position("BDAY"),
            "photo":        self._get_photo_range(),
            "end":          self._get_node_position("END")
        }

    def findNodesByKey(self, key):
        return ifilter(self._vAST, lambda n: n.KEY == key)

    def _get_node_position(self, key, required=False):
        q = self.findNodesByKey(key)

        if len(q) == 0 and required:
            raise ValueError("Could not determine vcard version")
        elif len(q) == 0:
            return None

        return q[0].lineno

    def _get_node_positions(self, key, required=False):
        q = self.findNodesByKey(key)

        if len(q) == 0 and required:
            raise ValueError("Could not determine vcard version")
        elif len(q) == 0:
            return None

        return [x.lineno for x in q]

    def _get_photo_range(self):
        """Attempts to discover where the photo attribute starts and ends"""

        # Do we have a photo?
        photo = self.findNodesByKey("PHOTO")

        if len(photo) == 0:
            return None

        # Grab where our photo starts in our vAST
        start_idx = self._vAST.index(photo[0])
        vAST_slice = self._vAST[start_idx:]

        def inPhotoSince(start):
            def wrapped(a):
                if type(a) == type(start) or type(a) == Unknown:
                    return True
                else:
                    return False
            return wrapped

        # Take every item in our vAST from the photo declaration
        # to the last UNKNOWN token
        photo_slice = list(takewhile(inPhotoSince(photo[0]), vAST_slice))
        start_line, end_line = photo_slice[0].lineno, photo_slice[-1].lineno

        return {"start": start_line, "end": end_line}

    def _discover_nodes(self):
        """ Cycle through our fields and record their positions for later
            retrieval
        """
        lineno = 0
        for line in self.readlines():
            parsed = parseline(line)

            if (parsed != None):
                subkey, key, attrs, value = parseline(line)
                t = getField(key)

                if t == None:
                    # We don't know what it is, process it later
                    t = Unknown(lineno=lineno)
                else:
                    t = t(lineno=lineno)

                yield t
            else:
                yield Unknown(lineno=lineno)

            lineno += 1

        # Return us to the beginning of the file
        self.handle.seek(0)

    def _read_line_numbers(self, l=[]):
        lineno = 0
        for line in self.readlines():
            if lineno in l:
                yield line

            lineno += 1

        self.handle.seek(0)

    def _read_line_range(self, start, end):
        r = list(range(start, end + 1))
        yield from self._read_line_numbers(r)

    def readlines(self, start=0, end=0):
        yield from self.handle

    def filterlines(self, fn=bool):
        for line in readlines(self):
            if fn(line):
                yield line
