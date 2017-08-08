from pygmyhdl import *

initialize()

@block
def register(clk, d, q):
    for i in range(len(d)):
        dff_g(clk, d.o[i], q.i[i])
    inst = q.i_inst

# @block
# def register(clk, d, q):
    # @seq_logic(clk.posedge)
    # def logic():
        # q.next = d

clk = Wire(0, name='clk')
d = Bus(4, name='d')
q = Bus(4, name='q')
reg = register(clk, d, q)

def test():
    for i in range(16):
        d.next = i
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)

simulate(test(), reg)
show_text_table('clk d q')

reg.convert()
#cnt1 = Bus(4)
#toVerilog(counter, clk, cnt1)
