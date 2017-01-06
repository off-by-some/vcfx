import os
from vcfx import reader
from builtins import filter

def dotdotslash(path):
    segs = [x for x in path.split(os.path.sep) if x != ""]
    segs.pop()
    return "/" + os.path.sep.join(segs)

def generate_ast(nodes):
    return ("\n".join([repr(x) for x in nodes])) + "\n"

def file_to_string(path):
    body = None
    f = open(path)
    body = "".join(f.readlines())
    f.close()
    return body

def write_to_fixture(path, text):
    with open(path, 'w') as f:
        for node in nodes:
            f.write(repr(node) + "\n")
    f.close()

def fixture_path_for(fname):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dotdotslash(dir_path) + "/fixtures/" + fname

stringify_fixture = lambda fname: file_to_string(fixture_path_for(fname))

ios_v3_ast = stringify_fixture("reggie-smalls-ios-v3.0.ast")
ios_v3_file = fixture_path_for("reggie-smalls-ios-v3.0.vcf")

def test_iteration():
    vcard = reader(ios_v3_file)
    nodes = list(vcard)
    generated_ast = generate_ast(nodes)

    # Assert that we get the expected AST back
    assert generated_ast == ios_v3_ast

def test_indexing():
    vcard = reader(ios_v3_file)
    node = vcard[5]
    with open(fixture_path_for("reggie-smalls-ios-v3.0.ast")) as f:
        assert repr(node) == f.readlines()[5].strip()

def test_addresses():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.addresses())
    all_expected = filter(lambda x: x.KEY == "ADR", list(vcard))

    assert len(set(all_expected) & set(nodes)) == len(nodes)

def test_emails():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.emails())
    all_expected = filter(lambda x: x.KEY == "EMAIL", list(vcard))

    assert len(set(all_expected) & set(nodes)) == len(nodes)

def test_phones():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.phones())
    all_expected = filter(lambda x: x.KEY == "TEL", list(vcard))

    assert len(set(all_expected) & set(nodes)) == len(nodes)

def test_urls():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.urls())
    all_expected = filter(lambda x: x.KEY == "URL", list(vcard))

    assert len(set(all_expected) & set(nodes)) == len(nodes)

def test_labels():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.labels())
    all_expected = filter(lambda x: x.KEY == "X-ABLabel", list(vcard))

    assert len(set(all_expected) & set(nodes)) == len(nodes)
