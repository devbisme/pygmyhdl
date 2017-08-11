from pygmyhdl import *
from pygmyhdl.gates import *

initialize()

@chunk
def adder_bit(a, b, c_in, sum_out, c_out):
    xor_g(sum_out, a, b, c_in)
    
    cry_a_b, cry_a_c, cry_b_c = Wire(), Wire(), Wire()
    and_g(cry_a_b, a, b)
    and_g(cry_a_c, a, c_in)
    and_g(cry_b_c, b, c_in)
    or_g(c_out, cry_a_b, cry_a_c, cry_b_c)

@chunk
def adder(a, b, sum_out):
    num_bits = len(a)
    #c = Bus(num_bits+1,0)
    c = Bus(num_bits,0)
    c_in = Wire(0)
    adder_bit(a.o[0], b.o[0], c_in, sum_out.i[0], c.i[0])
    for j in range(1, num_bits):
        adder_bit(a.o[j], b.o[j], c.o[j-1], sum_out.i[j], c.i[j])

@chunk
def incr(a, a_incr):
    one = Bus(len(a), 1)
    adder(a, one, a_incr)

@chunk
def register(clk, d, q):
    for i in range(len(d)):
        dff_g(clk, d.o[i], q.i[i])

@chunk
def counter(clk, q):
    q_plus_1 = Bus(len(q))
    incr(q, q_plus_1)
    register(clk, q_plus_1, q)

@chunk
def blinker(clk_i, led_o):
    cnt = Bus(23, name='cnt')
    counter(clk_i, cnt)
    @comb_logic
    def logic():
        led_o.next = cnt[22]

clk = Wire(0, name='clk')
led = Wire(0, name='led')
blinker(clk, led)

clk_sim(clk, num_cycles=20)
show_text_table('clk led')

led1 = Wire(0)
toVerilog(blinker, clk, led1)
