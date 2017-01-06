# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import range
from future import standard_library
standard_library.install_aliases()
import io
from .field import get_field_by_key
from vcfx.field.nodes import Unknown
from vcfx.field import all_nodes
from pydash.collections import filter_ as ifilter, partition, pluck
from pydash.objects import pick, assign, find_key
from itertools import takewhile
from six import iteritems

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

        self._in_fold = False

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
        photo_pos = self.positions["PHOTO"]
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

    def _determine_pos_fn(self, node):
        if node.SCALAR:
            return self._get_node_positions
        else:
            return self._get_node_position

    def discover(self):
        self._vAST = list(self.tokenize_lines(meta=True))
        self._flatten_labels()

    def _update_position(self, key, value=None):
        if value is None:
            return

        pos = self.positions[key]

        if pos is None:
            self.positions[key] = value
            return

        if pos is not None and type(pos) is not list:
            if self.positions[key] is not list:
                self.positions[key] = [self.positions[key]]

            self.positions[key] = self.positions[key] + [value]
        else:
            self.positions[key].append(value)

    def _replace_position(self, key, value):
        self.positions[key] = value


    # TODO: Py2
    def _find_key_by_item(self, v, node):
        get_all = lambda t: [[x,y] for x, y in iteritems(node) if type(y) is t]
        dicts = get_all(dict)
        lists = get_all(list)
        ints =  get_all(int)

        matches = [x for x, y in dicts if (y is v)]

        if len(matches) is 1: return matches[0]

        matches = []
        for k, i in ints:
            if v is i:
                return k

        matches = []
        for k, l in lists:
            if v in l:
                return k

    def tokenize_lines(self, **kw):
        lineno = 0
        for line in self.handle:
            for v in self._tokenize_line(line, lineno, **kw):
                yield v
            lineno += 1

    # Multi-line fold support, look for unparsable nodes and assign
    # the last known node the concatinated result
    def _determine_fold(self, parsed_line, lineno):
        last_node = self._find_key_by_item(lineno - 1, self.positions)

        if parsed_line is None:
            self._update_position("FOLDED", lineno)

        # We have found the second line of a fold, record the position
        if parsed_line is None and last_node is not "FOLDED":
            self._fold_range = {"start": lineno - 1}

        # We have reached the end of our fold, update the position
        if parsed_line is not None and last_node is "FOLDED":
            start_line = self._fold_range["start"]
            start_key = self._find_key_by_item(start_line, self.positions)
            r = {"start": self._fold_range["start"], "end": lineno - 1}
            self._replace_position(start_key, r)


    def _tokenize_line(self, line, lineno, meta=False, position_tracking=True):
        """ Parse a line and tokenize it with our field tokens """

        # TODO: vcard2 support
        parsed = parseline3(line)

        # Do some book-keeping on the line, determine if it's a folded attribute
        self._determine_fold(parsed, lineno)

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

            if position_tracking:
                self._update_position(key, lineno)

            # We only want meta information
            if meta:
                cls_kwrgs = pick(cls_kwrgs, "lineno", "subkey")

            yield t(**cls_kwrgs)

    def _read_line_numbers(self, l=[]):
        lineno = 0
        for line in self.readlines():
            if lineno in l:
                yield line

            lineno += 1

        self.handle.seek(0)

    def tokenize_rows(self, l=[], **kw):
        lineno = 0
        for line in self.tokenize_lines(**kw):
            if lineno in l:
                yield line

            lineno += 1

        self.handle.seek(0)

    def tokenize_row(self, row_num):
        return list(self.tokenize_row([row_num]))[0]

    def readslice(self, start, end):
        r = list(range(start, end + 1))
        for v in self._read_line_numbers(r):
            yield v

    def tokenize_slice(self, start, end):
        l = list(range(start, end + 1))

        lineno = 0
        for line in self.readlines():
            if lineno in l:
                i = self._tokenize_line(
                    line,
                    lineno,
                    position_tracking=False
                )
                for v in i:
                    yield v

            lineno += 1

        self.handle.seek(0)

    def readlines(self, start=0, end=0):
        for line in self.handle:
            yield line
