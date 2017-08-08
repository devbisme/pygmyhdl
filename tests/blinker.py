from pygmyhdl import *

initialize()

@chunk
def blinker(clk_i, led_o):
    cnt = Bus(23, name='cnt')
    tap = 2

    @seq_logic(clk_i.posedge)
    def logic_b():
        cnt.next = cnt + 1

    @comb_logic
    def logic_a():
        led_o.next = cnt[tap]

clk = Wire(0, name='clk')
led = Wire(0, name='led')
blinker(clk, led)

clk_sim(clk, num_cycles=20)
show_text_table('clk cnt led')

toVerilog(blinker, clk, led)
