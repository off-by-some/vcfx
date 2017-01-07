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

def flat(a):
    return list(reduce(lambda b, c: b + c, a))

def has_nodes(ast, nodes):
    expected_bucket = set()
    ast = list(ast)
    nodes = list(nodes)

    for node in nodes:
        expected_bucket.add(tuple(filter(lambda x: x.KEY == node.KEY, ast)))

    node_hashes = set(hash(x) for x in nodes)
    expected_nodes = set(hash(x) for x in flat(expected_bucket))

    return node_hashes == expected_nodes

def test_addresses():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.addresses())
    assert has_nodes(vcard, nodes)

def test_alternate_birthday():
    vcard = reader(ios_v3_file)
    nodes = [vcard.alternate_birthday()]
    assert has_nodes(vcard, nodes)

def test_birthday():
    vcard = reader(ios_v3_file)
    nodes = [vcard.birthday()]
    assert has_nodes(vcard, nodes)

def test_emails():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.emails())
    assert has_nodes(vcard, nodes)

def test_fullname():
    vcard = reader(ios_v3_file)
    nodes = [vcard.fullname()]
    assert has_nodes(vcard, nodes)

def test_version():
    vcard = reader(ios_v3_file)
    nodes = [vcard.version()]
    assert has_nodes(vcard, nodes)

def test_name():
    vcard = reader(ios_v3_file)
    nodes = [vcard.name()]
    assert has_nodes(vcard, nodes)

def test_org():
    vcard = reader(ios_v3_file)
    nodes = [vcard.organization()]
    assert has_nodes(vcard, nodes)

def test_prodid():
    vcard = reader(ios_v3_file)
    nodes = [vcard.prodid()]
    assert has_nodes(vcard, nodes)

def test_phones():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.phones())
    assert has_nodes(vcard, nodes)

def test_urls():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.urls())
    assert has_nodes(vcard, nodes)

def test_labels():
    vcard = reader(ios_v3_file)
    nodes = list(vcard.labels())
    assert has_nodes(vcard, nodes)
