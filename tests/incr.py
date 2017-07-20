from myhdl import *
from pygmyhdl import *

initialize()

@group
def adder_bit(a, b, c_in, sum_out, c_out):
    sum_a_b = Wire()
    xor_g(a, b, sum_a_b)
    xor_g(c_in, sum_a_b, sum_out)
    
    cry_a_b, cry_a_c, cry_b_c, cry_1 = Wire(), Wire(), Wire(), Wire()
    and_g(a, b, cry_a_b)
    and_g(a, c_in, cry_a_c)
    and_g(b, c_in, cry_b_c)
    or_g(cry_a_b, cry_a_c, cry_1)
    or_g(cry_b_c, cry_1, c_out)

@group
def adder(a, b, sum_out):
    num_bits = len(a)
    #c = Bus(num_bits+1,0)
    c = Bus(num_bits,0)
    c_in = Wire(0)
    adder_bit(a.o[0], b.o[0], c_in, sum_out.i[0], c.i[0])
    for j in range(1, num_bits):
        adder_bit(a.o[j], b.o[j], c.o[j-1], sum_out.i[j], c.i[j])

@group
def incr(a, a_incr):
    one = Bus(len(a), 1)
    adder(a, one, a_incr)

# Create signals for interfacing to the adder.
a, a_incr, a_incr_1 = [Bus(4,0,name) for name in ['a', 'a++', None]]

incr_1 = incr(a, a_incr)
random_sim(10, a)
show_text_table('a a++')
toVerilog(incr, a, a_incr_1)
