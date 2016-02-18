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
        yield from self._parser.tokenize_lines()
        self._parser.handle.seek(0)

    def addresses(self):
        positions = self._determine_accessor("ADR")
        yield from positions()

    def alternate_birthday(self):
        positions = self._determine_accessor("X-ALTBDAY")
        return positions()

    def birthday(self):
        positions = self._determine_accessor("BDAY")
        return positions()

    def emails(self):
        positions = self._determine_accessor("EMAIL")
        yield from positions()

    def fullname(self):
        positions = self._determine_accessor("FN")
        return positions()

    def prodid(self):
        positions = self._determine_accessor("PRODID")
        return positions()

    def phones(self):
        positions = self._determine_accessor("TEL")
        yield from positions()

    def urls(self):
        positions = self._determine_accessor("URL")
        yield from positions()

    def version():
        return self._get_from_position("VERSION")

    def name(self):
        return self._get_from_position("N")

    def organization(self):
        return self._get_from_position("ORG")

    def photo(self):
        return self._parser.compile_photo()


    def labels(self):
        yield from self._yield_from_positions("X-ABLabel")

    def _determine_accessor(self, key):
        node = list(filter(lambda n: n.KEY == key, all_nodes))[0]

        if node.SCALAR:
            return partial(self._yield_from_positions, node.KEY)
        else:
            return self._get_from_position

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
            yield from self._parser.tokenize_rows([positions])
        else:
            yield from self._parser.tokenize_rows(positions)
