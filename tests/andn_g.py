from myhdl import *
from pygmyhdl import *

initialize()

o, a, b, c, d = [Wire(1,name) for name in 'o a b c d'.split()]
orn_g(o, a, b, c, d)

exhaustive_sim(a, b, c, d)

show_text_table('a b c d o')
toVerilog(orn_g, o, a, b, c, d)
