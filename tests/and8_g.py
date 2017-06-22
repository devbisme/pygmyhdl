from myhdl import *
from pygmyhdl import *

initialize()

@group
def and4_g(in0, in1, in2, in3, out):
    out_0_1, out_2_3 = Wire(), Wire()
    and_g(in0, in1, out_0_1)
    and_g(in2, in3, out_2_3)
    and_g(out_0_1, out_2_3, out)
    
a, b, c, d, result = [Wire(name) for name in 'a b c d result'.split()]
#print(and4_g(a, b, c, d, result))
toVHDL(and4_g, a, b, c, d, result)
#toVerilog(and4_g, a, b, c, d, result)
