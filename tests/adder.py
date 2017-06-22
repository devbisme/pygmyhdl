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
    c = Bus(num_bits+1)
    adder_bit(a(0), b(0), c(0), sum_out.i[0], c.i[1])
    adder_bit(a(1), b(1), c(1), sum_out.i[1], c.i[2])
    adder_bit(a(2), b(2), c(2), sum_out.i[2], c.i[3])
    adder_bit(a(3), b(3), c(3), sum_out.i[3], c.i[4])
    
@group
def adder(a, b, sum_out):
    num_bits = len(a)
    c = Bus(num_bits+1)
    for j in range(num_bits):
        adder_bit(a(j), b(j), c(j), sum_out.i[j], c.i[j+1])

a, b, sum_a_b = [Bus(4,name) for name in 'a b a+b'.split()]
print(adder(a, b, sum_a_b))
#print(len(adder(a, b, sum_a_b)))
#print(len(unrolled_adder(a, b, sum_a_b)))
#toVHDL(unrolled_adder, a, b, sum_a_b)
sum_a_b_2 = Bus(4)
toVHDL(adder, a, b, sum_a_b_2)
#toVerilog(adder, a, b, sum_a_b)
