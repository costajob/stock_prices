import doctest 
from pkgutil import iter_modules


def load_tests(loader, tests, ignore):
    modules = [name for _, name, _ in iter_modules(['stockp']) if name != 'tests']
    for mod in modules:
        tests.addTests(doctest.DocTestSuite(mod))
    return tests
