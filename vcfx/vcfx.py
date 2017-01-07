from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import filter
from future import standard_library

standard_library.install_aliases()

from .tokenizer import Parser
from .field import all_nodes
from pydash.functions import partial

class reader(object):
    """docstring for reader"""
    def __init__(self, vcfpath, scan=True):
        super(reader, self).__init__()
        self._scanned = scan
        self._parser = Parser(vcfpath, scan=scan)

    def __iter__(self):
        for line in self._parser.tokenize_lines():
            yield line
        self._parser.handle.seek(0)

    def __getitem__(self, index):
        return self._parser._vAST[index]

    def addresses(self):
        positions = self._determine_accessor("ADR")
        for p in positions():
            yield p

    def alternate_birthday(self):
        positions = self._determine_accessor("X-ALTBDAY")
        return positions()

    def birthday(self):
        positions = self._determine_accessor("BDAY")
        return positions()

    def emails(self):
        positions = self._determine_accessor("EMAIL")
        for p in positions():
            yield p

    def fullname(self):
        positions = self._determine_accessor("FN")
        return positions()

    def prodid(self):
        positions = self._determine_accessor("PRODID")
        return positions()

    def phones(self):
        positions = self._determine_accessor("TEL")
        for p in positions():
            yield p

    def urls(self):
        positions = self._determine_accessor("URL")
        for p in positions():
            yield p

    def version(self):
        return self._get_from_position("VERSION")

    def name(self):
        return self._get_from_position("N")

    def organization(self):
        return self._get_from_position("ORG")

    def photo(self):
        return self._parser.compile_photo()

    def labels(self):
        for p in self._yield_from_positions("X-ABLabel"):
            yield p

    def _determine_accessor(self, key):
        node = list(filter(lambda n: n.KEY == key, all_nodes))[0]

        if node.SCALAR:
            return partial(self._yield_from_positions, node.KEY)
        else:
            return partial(self._get_from_position, node.KEY)

    def _get_from_position(self, pname):
        # find our desired position in the file
        position = self._parser.positions[pname]

        if position is None:
            return None
        else:
            return list(self._parser.tokenize_rows([position]))[0]

    def _yield_from_positions(self, pname):
        # find our desired positions in the file
        positions = self._parser.positions[pname]

        if positions is None:
            yield None
        elif type(positions) is not list and type(positions) is int:
            for r in self._parser.tokenize_rows([positions]):
                yield r
        else:
            for r in self._parser.tokenize_rows(positions):
                yield r
