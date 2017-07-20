from pygmyhdl import *

initialize()

@group
def incr(a, a_incr):
    @comb_logic
    def logic():
        a_incr.next = a + 1

# @group
# def register(clk, d, q):
    # for i in range(len(d)):
        # dff_g(clk, d.o[i], q.i[i])

@group
def register(clk, d, q):
    @seq_logic(clk.posedge)
    def logic():
        q.next = d

@group
def counter(clk, q):
    q_plus_1 = Bus(len(q))
    incr(q, q_plus_1)
    register(clk, q_plus_1, q)

clk = Wire(0, name='clk')
cnt = Bus(4, name='cnt')
counter(clk, cnt)

def test():
    for _ in range(14):
        clk.next = 1
        yield delay(1)
        clk.next = 0
        yield delay(1)

simulate(test())
show_text_table('clk cnt')

cnt1 = Bus(4)
toVerilog(counter, clk, cnt1)
