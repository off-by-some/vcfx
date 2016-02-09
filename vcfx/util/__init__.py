import imp

def filter_defined_cls(module_obj):
    mattrs = module_obj.__dict__
    clses = []
    for attr in mattrs:
        cls = mattrs[attr]
        if isinstance(cls, type) and cls.__module__ == module_obj.__name__:
            clses.append(cls)

    return clses

def get_modules(pnames, path, name=""):
    mpath = [imp.find_module(x, path) for x in pnames]
    paths = [x[1] for x in mpath]

    if len(paths) is not len(pnames):
        raise Exception("Could not discover nodes requested")

    modules = []
    for pname, fpath in zip(pnames, paths):
        namespace = name + "." + pname + ".nodes"
        fpath += "/nodes.py"
        modules.append(imp.load_source(namespace, fpath))

    return modules
