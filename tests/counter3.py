from pygmyhdl import *

initialize()

@group
def counter(clk, q):
    @always_seq(clk.posedge,None)
    def logic():
        q.next = q + 1
    #_instances.append(logic)
    return logic

clk = Wire(0, name='clk')
cnt = Bus(4, name='cnt')
#cntr = counter(clk, cnt)

# def test():
    # for _ in range(14):
        # clk.next = 1
        # yield delay(1)
        # clk.next = 0
        # yield delay(1)

#simulate(test())
#show_text_table('clk cnt')

cnt1 = Bus(4)
toVerilog(counter, clk, cnt1)
