from pygmyhdl import *

initialize()

@group
def xfer(a, b):
    @comb_logic
    def logic():
        b.next = a

@group
def bus_xfer(a, b):
    for j in range(len(a)):
        xfer(a.o[j], b.i[j])

a_bus = Bus(5, name='a')
b_bus = Bus(5, name='b')
bus_xfer(a_bus, b_bus)

def test():
    for d in range(20):
        a_bus.next = d & ((1<<len(a_bus))-1)
        yield delay(1)

simulate(test())
show_text_table()

initialize()
a_bus = Bus(5, name='a')
b_bus = Bus(5, name='b')
toVerilog(bus_xfer, a_bus, b_bus)

# def adder_bit(a, b, c_in, sum_out, c_out):
    # xor_g(sum_out, a, b, c_in)
    
    # cry_a_b, cry_a_c, cry_b_c = Wire(), Wire(), Wire()
    # and_g(cry_a_b, a, b)
    # and_g(cry_a_c, a, c_in)
    # and_g(cry_b_c, b, c_in)
    # or_g(c_out, cry_a_b, cry_a_c, cry_b_c)

# @group
# def adder(a, b, sum_out):
    # num_bits = len(a)
    # #c = Bus(num_bits+1,0)
    # c = Bus(num_bits,0)
    # c_in = Wire(0)
    # adder_bit(a.o[0], b.o[0], c_in, sum_out.i[0], c.i[0])
    # for j in range(1, num_bits):
        # adder_bit(a.o[j], b.o[j], c.o[j-1], sum_out.i[j], c.i[j])

# @group
# def incr(a, a_incr):
    # one = Bus(len(a), 1)
    # adder(a, one, a_incr)

# @group
# def register(clk, d, q):
    # @seq_logic(clk.posedge)
    # def logic():
        # q.next = d

# @group
# def counter(clk, q):
    # q_plus_1 = Bus(len(q))
    # incr(q, q_plus_1)
    # register(clk, q_plus_1, q)

# clk = Wire(0, name='clk')
# cnt = Bus(4, name='cnt')
# counter(clk, cnt)

# def test():
    # for _ in range(20):
        # clk.next = 1
        # yield delay(1)
        # clk.next = 0
        # yield delay(1)

# simulate(test())
# show_text_table('clk cnt')

# cnt1 = Bus(4)
# toVerilog(counter, clk, cnt1)
