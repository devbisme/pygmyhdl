from myhdl import *
from pygmyhdl import *
import byteplay3 as bp

def _postamble(a, b):
    pass


def test_func():
    index = len(pygmyhdl._instances)
    pass
    insts = _postamble(index, instances())
    return insts

f_code = bp.Code.from_code(test_func.__code__)
print(f_code.code)
