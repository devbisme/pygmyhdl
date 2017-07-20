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

# a, b, c_in, sum_out, c_out = [Wire() for _ in range(5)]
# print(toVHDL(adder_bit, a, b, c_in, sum_out, c_out))
# import sys
# print('Here!')
# sys.exit()

@group
def unrolled_adder(a, b, sum_out):
    num_bits = len(a)
    c = Bus(num_bits+1,1)
    adder_bit(a.o[0], b.o[0], c.o[0], sum_out.i[0], c.i[1])
    adder_bit(a.o[1], b.o[1], c.o[1], sum_out.i[1], c.i[2])
    adder_bit(a.o[2], b.o[2], c.o[2], sum_out.i[2], c.i[3])
    adder_bit(a.o[3], b.o[3], c.o[3], sum_out.i[3], c.i[4])
    
@group
def adder(a, b, sum_out):
    num_bits = len(a)
    c = Bus(num_bits+1,1)
    for j in range(num_bits):
        adder_bit(a.o[j], b.o[j], c.o[j], sum_out.i[j], c.i[j+1])

a, b, sum_a_b = [Bus(4,0,name) for name in 'a b a+b'.split()]
adder(a, b, sum_a_b)
random_sim(10, a, b)
show_text_table('a b a+b')
#print(adder(a, b, sum_a_b))
#sum_a_b = Bus(4)
#print(unrolled_adder(a, b, sum_a_b))
#print(len(adder(a, b, sum_a_b)))
#print(len(unrolled_adder(a, b, sum_a_b)))
#sum_a_b = Bus(4)
#toVHDL(unrolled_adder, a, b, sum_a_b)
sum_a_b = Bus(4)
toVerilog(adder, a, b, sum_a_b)
