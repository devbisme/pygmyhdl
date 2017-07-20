from myhdl import *
from pygmyhdl import *

initialize()

clk, d, q = [Wire(0,name) for name in ['clk','d','q']]
dff_1 = dff_g(clk, d, q)

def test(clk, d):
    for d.next in [0,1,1,0,0,1]:
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)

test_1 = test(clk, d)

simulate(test_1)

show_text_table()

# Create signals for interfacing to the adder.
# a, a_incr, a_incr_1 = [Bus(4,0,name) for name in ['a', 'a++', None]]

# incr_1 = incr(a, a_incr)
# random_sim(10, a)
# show_text_table('a a++')
# toVerilog(incr, a, a_incr_1)
