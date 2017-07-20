from myhdl import *
from pygmyhdl import *

#@block
def adder_bit(a, b, c_in, sum_, c_out):
    '''Single bit adder.'''
    @always_comb
    def adder_logic():
        sum_.next = a ^ b ^ c_in
        c_out.next = (a & b) | (a & c_in) | (b & c_in)
    return instances()

#@block
def adder(a, b, sum_):
    '''Connect single-bit adders to create a complete adder.'''
    c = [Signal(bool(0)) for _ in range(len(a)+1)] # Carry signals between stages.
    s = [Signal(bool(0)) for _ in range(len(a))]   # Sum bit for each stage.
    stages = []  # Storage for adder bit instances.
    # Create the adder bits and connect them together.
    for i in range(len(a)):
        stages.append( adder_bit(a=a(i), b=b(i), sum_=s[i], c_in=c[i], c_out=c[i+1]) )
    q = ConcatSignal(*reversed(s))
    # Concatenate the sum bits and send them out on the sum_ output.
    @always_comb
    def make_sum():
        sum_.next = q
    return instances()  # Return all the adder stage instances.

def incr(a, a_incr):
    one = Signal(intbv(1)[len(a):])
    #one = Bus(len(a), 1)
    incr_1 = adder(a, one, a_incr)
    return instances()

# Create signals for interfacing to the adder.
a, a_incr = [Signal(intbv(0,0,16)) for _ in range(2)]

incr_1 = incr(a, a_incr)
#adder_1.convert()
toVerilog(incr, a, a_incr)
