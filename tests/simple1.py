from myhdl import *
from pygmyhdl import *
from random import randint

# @block
# def adder_bit(a, b, c_in, sum_, c_out):
    # '''Single bit adder.'''
    # @always_comb
    # def adder_logic():
        # sum_.next = a ^ b ^ c_in
        # c_out.next = (a & b) | (a & c_in) | (b & c_in)
    # return instances()

@block
@group
def adder_bit(a, b, c_in, sum_, c_out):
    '''Single bit adder.'''
    @comb_logic
    def logic():
        sum_.next = a ^ b ^ c_in
        c_out.next =  (a & b) | (a & c_in) | (b & c_in)
    #return logic

@block
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

# Create signals for interfacing to the adder.
a, b, sum_ = [Signal(intbv(0,0,8)) for _ in range(3)]

adder_1 = adder(a, b, sum_)

def test():
    for _ in range(10):
        a.next = randint(0, a.max-1)
        b.next = randint(0, b.max-1)
        yield delay(1)

test_1 = test()

Simulation(adder_1, test_1).run()

adder_1.convert()
#toVerilog(adder, a, b, sum_)