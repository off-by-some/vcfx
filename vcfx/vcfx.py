from .tokenizer import Parser

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
        yield from self._yield_from_positions("address")

    def alternate_birthday(self):
        return self._get_from_position("altbirthday")

    def birthday(self):
        return self._get_from_position("altbirthday")

    def emails(self):
        yield from self._yield_from_positions("emails")

    def fullname(self):
        return self._get_from_position("fullname")

    def prodid(self):
        return self._get_from_position("prodid")

    def phones(self):
        yield from self._yield_from_positions("telephone")

    def urls(self):
        yield from self._yield_from_positions("url")

    def version():
        return self._get_from_position("version")

    def name(self):
        return self._get_from_position("name")

    def organization(self):
        return self._get_from_position("organization")

    def photo(self):
        node = self._parser.compile_photo()

        if node is None:
            return None
        else:
            return node

    def labels(self):
        yield from self._yield_from_positions("label")

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
