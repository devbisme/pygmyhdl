# -*- coding: utf-8 -*-

# MIT license
# 
# Copyright (C) 2017 by XESS Corp.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
Some basic logic gates implemented in PygMyHDL.
'''


from pygmyhdl import *

############## Logic gate definitions. #################

@chunk
def inv_g(o, a):
    '''Single-bit inverter (NOT gate).'''
    @comb_logic
    def logic():
        o.next = not a

@chunk
def and_g(o, a, b, c=Wire(1), d=Wire(1), e=Wire(1)):
    '''AND gate for up to 5 single-bit inputs.'''
    @comb_logic
    def logic():
        o.next = a & b & c & d & e

@chunk
def or_g(o, a, b, c=Wire(0), d=Wire(0), e=Wire(0)):
    '''OR gate for up to 5 single-bit inputs.'''
    @comb_logic
    def logic():
        o.next = a | b | c | d | e

@chunk
def xor_g(o, a, b, c=Wire(0), d=Wire(0), e=Wire(0)):
    '''XOR gate for up to 5 single-bit inputs.'''
    @comb_logic
    def logic():
        o.next = a ^ b ^ c ^ d ^ e

@chunk
def dff_g(clk, d, q):
    '''Positive-edge triggered D flip-flop.'''
    @seq_logic(clk.posedge)
    def logic():
        q.next = d
