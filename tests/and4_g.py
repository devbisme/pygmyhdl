from myhdl import *
from pygmyhdl import *
import byteplay3 as bp

initialize()

@group
def and4_g(in0, in1, in2, in3, out):
    #begin = len(pygmyhdl._instances)
    out_0_1, out_2_3 = Wire(), Wire()
    and_g(in0, in1, out_0_1)
    and_g(in2, in3, out_2_3)
    and_g(out_0_1, out_2_3, out)
    #insts = pygmyhdl._instances[begin:]
    #pygmyhdl._instances = pygmyhdl._instances[:begin]
    #pygmyhdl._instances.append(insts)
    #return insts

#f_code = bp.Code.from_code(and4_g.__code__)
#print(f_code.code)

@group
def and8_g(in0, in1, in2, in3, in4, in5, in6, in7, out):
    out_0_1_2_3, out_4_5_6_7 = Wire(), Wire()
    and4_g(in0, in1, in2, in3, out_0_1_2_3)
    and4_g(in4, in5, in6, in7, out_4_5_6_7)
    and_g(out_0_1_2_3, out_4_5_6_7, out)

# def and8_g(in0, in1, in2, in3, in4, in5, in6, in7, out):
    # begin = len(pygmyhdl._instances)
    # out_0_1_2_3, out_4_5_6_7 = Wire(), Wire()
    # and4_g(in0, in1, in2, in3, out_0_1_2_3)
    # and4_g(in4, in5, in6, in7, out_4_5_6_7)
    # and_g(out_0_1_2_3, out_4_5_6_7, out)
    # insts = pygmyhdl._instances[begin:]
    # pygmyhdl._instances = pygmyhdl._instances[:begin]
    # pygmyhdl._instances.append(insts)
    # return insts

# def and8_g(in0, in1, in2, in3, in4, in5, in6, in7, out):
    # out_0_1_2_3, out_4_5_6_7 = Wire(), Wire()
    # g1 = and4_g(in0, in1, in2, in3, out_0_1_2_3)
    # g2 = and4_g(in4, in5, in6, in7, out_4_5_6_7)
    # g3 = and_g(out_0_1_2_3, out_4_5_6_7, out)
    # return instances()
    
a, b, c, d, e, f, g, h, result = [Wire(name) for name in 'a b c d e f g h result'.split()]
print(a, b, c, d, e, f, g, h, result)
print(and8_g(a, b, c, d, e, f, g, h, result))
toVHDL(and8_g, a, b, c, d, e, f, g, h, result)
#toVerilog(and4_g, a, b, c, d, result)
