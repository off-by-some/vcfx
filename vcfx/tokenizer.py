# -*- coding: utf-8 -*-
import io
from .field import get_field_by_key
from vcfx.field.nodes import Unknown
from vcfx.field import all_nodes
from pydash.collections import filter_ as ifilter, partition, pluck
from pydash.objects import pick, assign
from itertools import takewhile

def parseline3(line):

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

    attrs = [normalizeAttr(x) for x in attrs]

    return subkey, key, attrs, value


class Parser(object):
    def __init__(self, fpath=None, scan=False):
        super(Parser, self).__init__()
        self.fpath = fpath

        if fpath == None or type(fpath) != str:
            raise ValueError("A valid filepath must be provided")

        self.handle = io.open(self.fpath, "r", encoding="utf-8", newline="\r\n")

        node_keys = [getattr(x, "KEY") for x in all_nodes]

        self._vAST = None

        # Init our positions map with the keys from our defined nodes
        self.positions = {}
        for key in node_keys:
            self.positions[key] = None

        if scan:
            self.discover()
            self.handle.seek(0)

    def _filter_nodes(self, fn):
        return ifilter(self._vAST, fn)

    def find_nodes_by_key(self, key):
        return self._filter_nodes(lambda n: n.KEY == key)

    def find_nodes_by_subkey(self, subkey):
        return self._filter_nodes(lambda n: n.subkey == subkey)

    # IOS Labels
    def _flatten_labels(self):
        label_idxs = self.positions["X-ABLabel"]

        if label_idxs == None:
            return

        label_nodes = [self._vAST[x] for x in label_idxs]

        for node in label_nodes:
            subkey = node.subkey
            idx = self._vAST.index(node)

            # Find the parent node to attach our label
            # TODO(cassidy): This could break if there can be more than 2 items
            #                with the same subkey, research
            parent = self._filter_nodes(
                lambda n: n.subkey == subkey and n is not node
            )[0]

            # Assign our label to it's parent
            parent.label = node.value

    def _get_node_position(self, key, required=False):
        """Discovers a single node position in vAST"""
        q = self.find_nodes_by_key(key)

        if len(q) == 0 and required:
            raise ValueError("Could not find node by key " + key )
        elif len(q) == 0:
            return None

        return q[0].lineno

    def _get_node_positions(self, key, required=False):
        """Discovers many node positions in vAST"""
        q = self.find_nodes_by_key(key)

        if len(q) == 0 and required:
            raise ValueError("Could not determine vcard version")
        elif len(q) == 0:
            return None

        return [x.lineno for x in q]

    def compile_photo(self):
        photo_pos = self.positions["photo"]

        if photo_pos is None:
            return None

        start, end = photo_pos["start"], photo_pos["end"]

        # Retokenize and grab real-boy data
        photo_tokens = list(self.tokenize_slice(start, end))

        b64segs = [x.value for x in photo_tokens]

        # Strip the spaces + CLRF, and join the segments
        newvalue = "".join([x.strip(" \r\n") for x in b64segs])

        # Update the parent photo node with the correct value
        photo_tokens[0].value = newvalue
        photo_tokens[0].b64 = newvalue

        return photo_tokens[0]


    def _get_photo_range(self):
        """Attempts to discover where the photo attribute starts and ends
           based on information from the vAST
        """

        # Do we have a photo?
        photo = self.find_nodes_by_key("PHOTO")

        if len(photo) == 0:
            # Nope.
            return None

        # Grab where our photo starts in our vAST
        start_idx = self._vAST.index(photo[0])

        # Slice off anything before it
        vAST_slice = self._vAST[start_idx:]

        def not_known_token(t):
            """ Stop at the first token that doesn't match t : <T> or Unknown
            """
            def wrapped(a):
                if type(a) == type(t) or type(a) == Unknown:
                    return True
                else:
                    return False
            return wrapped

        # Take every item in our vAST from the photo declaration
        # to the last UNKNOWN token.. A bit of a weak heruristic,
        # as it only works for photos.
        # TODO(cassidy): Investigate this before a folded 80 character
        #                address does
        photo_slice = list(takewhile(not_known_token(photo[0]), vAST_slice))
        start_line, end_line = photo_slice[0].lineno, photo_slice[-1].lineno

        return {"start": start_line, "end": end_line}

    def _determine_pos_fn(self, node):
        if node.KEY is "PHOTO":
            return lambda x: self._get_photo_range()
        if node.SCALAR:
            return self._get_node_positions
        else:
            return self._get_node_position

    def discover(self):
        self._vAST = list(self.tokenize_lines(meta=True))

        # Find the position of every node we know about
        positions = {}
        for node in self._vAST:
            getpos = self._determine_pos_fn(node)
            positions[node.KEY] = getpos(node.KEY)

        # Update our positions
        assign(self.positions, positions)

        self._flatten_labels()

    def tokenize_lines(self, meta=False):
        lineno = 0
        for line in self.handle:
            yield from self._tokenize_line(line, lineno=lineno, meta=meta)
            lineno += 1

    def _tokenize_line(self, line, lineno=None, meta=False):
        """ Parse a line and tokenize it with our field tokens """

        parsed = parseline3(line)

        if parsed is None:
            yield Unknown(rawvalue=line, lineno=lineno)
        else:
            subkey, key, attrs, value = parsed
            t = get_field_by_key(key)


            cls_kwrgs = {
                "subkey": subkey,
                "attrs": attrs, "rawvalue": value,
                "lineno": lineno
            }

            # We only want meta information
            if meta:
                cls_kwrgs = pick(cls_kwrgs, "lineno", "subkey")


            UnknownNode = lambda kw: Unknown(**kw)
            FieldNode = lambda kw: t(**kw)

            if t == None:
                yield UnknownNode(cls_kwrgs)
            else:
                yield FieldNode(cls_kwrgs)


    def _read_line_numbers(self, l=[]):
        lineno = 0
        for line in self.readlines():
            if lineno in l:
                yield line

            lineno += 1

        self.handle.seek(0)

    def tokenize_rows(self, l=[]):
        lineno = 0
        for line in self.tokenize_lines():
            if lineno in l:
                yield line

            lineno += 1

        self.handle.seek(0)

    def tokenize_row(self, row_num):
        return list(self.tokenize_row([row_num]))[0]

    def readslice(self, start, end):
        r = list(range(start, end + 1))
        yield from self._read_line_numbers(r)

    def tokenize_slice(self, start, end):
        l = list(range(start, end + 1))

        lineno = 0
        for line in self.readlines():
            if lineno in l:
                yield from self._tokenize_line(line, lineno=lineno)

            lineno += 1

        self.handle.seek(0)

    def readlines(self, start=0, end=0):
        yield from self.handle
