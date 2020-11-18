from pygmyhdl import *

initialize()

@chunk
def blinker(clk_i, led_o, length):
    cnt = Bus(length, name='cnt')

    @seq_logic(clk_i.posedge)
    def logic_b():
        cnt.next = cnt + 1

    @comb_logic
    def logic_a():
        led_o.next = cnt[length-1]

clk = Wire(name='clk')
led = Wire(name='led')
blinker(clk_i=clk, led_o=led, length=3)

# Run a simulation of the LED blinker.
clk_sim(clk, num_cycles=16)

# Not executing in Jupyter, so don't display waveforms.
#show_waveforms()

# Show the simulation results as a table.
show_text_table()

# Output the Verilog code for the blinker.
toVerilog(blinker, clk_i=clk, led_o=led, length=22)

# Create the pin constraint file.
with open('blinker.pcf', 'w') as pcf:
    pcf.write(
'''
set_io led_o 99
set_io clk_i 21
'''
    )