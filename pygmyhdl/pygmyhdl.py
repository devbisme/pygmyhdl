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
PygMyHDL main code module.
'''

from __future__ import print_function
#from __future__ import unicode_literals   # Messes up byteplay on Python 2.
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import range
from future import standard_library
standard_library.install_aliases()

import sys
USING_PYTHON2 = (sys.version_info.major == 2)
USING_PYTHON3 = not USING_PYTHON2

import pdb
import random
import types
import itertools
import functools

from myhdl import *
from myhdlpeek import *

if USING_PYTHON3:
    import byteplay3 as bp
else:
    import byteplay as bp


# List for storing MyHDL instances generated by this module.
_instances = list()


############## @comb_logic & @seq_logic decorators. #################

try:
    # These are the logic function decorators for MyHDL version >= 1.0.

    from myhdl._instance import _getCallInfo
    from myhdl._always_comb import _AlwaysComb
    from myhdl._always_seq import _AlwaysSeq
    import myhdl._instance as myhdlinst
    import myhdl._always_comb as myhdlcomb
    import myhdl._always_seq as myhdlseq
    import myhdl._always as myhdlalways
    import myhdl._Signal as myhdlsig
    import myhdl._util as myhdlutil
    from types import FunctionType

    def comb_logic(func):
        '''Decorator for combinational logic functions in PygMyHDL.
           Create a combinational logic block and store it on the instance list.'''
        callinfo = myhdlinst._getCallInfo()
        if not isinstance(func, FunctionType):
            raise myhdlcomb.AlwaysCombError(myhdlcomb._error.ArgType)
        if myhdlutil._isGenFunc(func):
            raise myhdlcomb.AlwaysCombError(myhdlcomb._error.ArgType)
        if func.__code__.co_argcount > 0:
            raise myhdlcomb.AlwaysCombError(myhdlcomb._error.NrOfArgs)
        c = myhdlcomb._AlwaysComb(func, callinfo=callinfo)
        _instances.append(c)
        return c

    def seq_logic(edge, reset=None):
        '''Decorator for sequential (clocked) logic functions in PygMyHDL.
           Creates a sequential logic block and stores it on the instance list.'''
        callinfo = myhdlinst._getCallInfo()
        sigargs = []
        if not isinstance(edge, myhdlsig._WaiterList):
            raise AlwaysSeqError(myhdlseq._error.EdgeType)
        edge.sig._read = True
        edge.sig._used = True
        sigargs.append(edge.sig)
        if reset is not None:
            if not isinstance(reset, myhdlseq.ResetSignal):
                raise AlwaysSeqError(myhdlseq._error.ResetType)
            reset._read = True
            reset._used = True
            sigargs.append(reset)
        sigdict = myhdlalways._get_sigdict(sigargs, callinfo.symdict)

        def _always_seq_decorator(func):
            if not isinstance(func, FunctionType):
                raise myhdlseq.AlwaysSeqError(myhdlseq._error.ArgType)
            if myhdlutil._isGenFunc(func):
                raise myhdlseq.AlwaysSeqError(myhdlseq._error.ArgType)
            if func.__code__.co_argcount > 0:
                raise myhdlseq.AlwaysSeqError(myhdlseq._error.NrOfArgs)
            c = myhdlseq._AlwaysSeq(func, edge, reset, callinfo=callinfo, sigdict=sigdict)
            _instances.append(c)
            return c
        return _always_seq_decorator

except ImportError:
    # If the import statements in the above section throw an exception,
    # that means we're using MyHDL < 1.0 which has a different way of
    # doing the logic function decorators.

    def comb_logic(f):
        '''Decorator for combinational logic functions in PygMyHDL.
           Create a combinational logic block and store it on the instance list.'''
        def comb_func(f):
            return always_comb(f)
        inst = comb_func(f)
        _instances.append(inst)
        return inst

    def seq_logic(trigger):
        '''Decorator for sequential (clocked) logic functions in PygMyHDL.
           Creates a sequential logic block and stores it on the instance list.'''
        def seq_logic_decorator(f):
            def seq_func(f):
                return always_seq(trigger,None)(f)
            inst = seq_func(f)
            _instances.append(inst)
            return inst
        return seq_logic_decorator



############## @chunk decorator. #################

if USING_PYTHON3:
    def _func_copy(f, new_code) :
        '''
        Return a copy of function f with __code__ section replaced with new_code.
        Copied from https://stackoverflow.com/questions/13503079/how-to-create-a-copy-of-a-python-function
        '''
        g = types.FunctionType(new_code, f.__globals__, name=f.__name__,
                               argdefs=f.__defaults__,
                               closure=f.__closure__)
        g = functools.update_wrapper(g, f)
        g.__kwdefaults__ = f.__kwdefaults__
        return g
else:
    def _func_copy(f, new_code) :
        '''
        Return a copy of function f with __code__ section replaced with new_code.
        Copied from https://stackoverflow.com/questions/13503079/how-to-create-a-copy-of-a-python-function
        '''
        g = types.FunctionType(new_code, f.func_globals, name=f.func_name,
                               argdefs=f.func_defaults,
                               closure=f.func_closure)
        g = functools.update_wrapper(g, f)
        return g

def preamble_func():
    '''Preamble inserted to mark the hardware instantiated previous to this chunk.'''
    return len(_instances)

def postamble_func(index, myhdl_instances):
    '''Postamble inserted to hardware instantiated in this chunk.'''
    global _instances

    # Build a list of unique instances created by the chunked function.
    chunk_insts = _instances[index:] + myhdl_instances
    chunk_insts = sorted(chunk_insts, key=id)
    chunk_insts = [k for k,_ in itertools.groupby(chunk_insts)]

    # Append the list of instances to the global _instances list.
    _instances = _instances[:index]
    _instances.append(chunk_insts)

    # Return the list of instances.
    return chunk_insts

def chunk(f):
    '''
    Decorator for grouping components generated by function f.

    Gets the generator function code section and prepends/appends code to
    observe what components are instantiated in the _instances list and then
    stores them in a local variable so MyHDL can detect them. 
    '''

    # Get the generator function code section.
    f_code = bp.Code.from_code(f.__code__)

    # Add this code to the start to store the beginning index of the _instances list.
    # Python version of preamble:
    #   instances_begin_index = len(pygmyhdl._instances)
    preamble = [
        (bp.LOAD_GLOBAL, 'preamble_func'),
        (bp.CALL_FUNCTION, 0),
        (bp.STORE_FAST, 'instances_begin_index')
    ]

    # Add this code to the end to copy the new components added by f() to the
    # _instances list and also return them.
    # Python version of postamble:
    #   loc_insts = postamble_func(instances_begin_index, instances())
    #   return loc_insts
    postamble = [
        (bp.LOAD_GLOBAL, 'postamble_func'),
        (bp.LOAD_FAST, 'instances_begin_index'),
        (bp.LOAD_GLOBAL, 'instances'),
        (bp.CALL_FUNCTION, 0),
        (bp.CALL_FUNCTION, 2),
        (bp.STORE_FAST, 'loc_insts'),
        (bp.LOAD_FAST, 'loc_insts'),
        (bp.RETURN_VALUE, None)
    ]

    # Remove the original return value and return instruction from f().
    f_code.code.pop()
    f_code.code.pop()

    # Create new code section from preamble + original code + postamble.
    new_code = preamble
    new_code.extend(f_code.code)
    new_code.extend(postamble)
    f_code.code = new_code

    # Make a copy of the original function, replace its code section with the
    # altered code section, and return the result as the decorated function.
    return _func_copy(f, f_code.to_code())


############## Wire and Bus object classes. #################

@chunk
def _sig_xfer(a, b):
    '''A simple hardware chunk to transfer one signal to another.'''
    @comb_logic
    def logic():
        b.next = a

class Wire(SignalType):
    '''A one-bit signal.'''
    def __init__(self, init_val=0, name=None):
        super(Wire, self).__init__(bool(init_val)) # Don't use super(). Fails on Python 2.
        if name:
            Peeker(self, name)

class Bus(SignalType):
    '''A multi-bit signal.'''
    def __init__(self, width=1, init_val=0, name=None, vtype=modbv):
        super(Bus, self).__init__(vtype(init_val)[width:]) # Don't use super(). Fails on Python 2.
        self.width = width
        self.i_wires = None
        self.o_wires = None
        if name:
            Peeker(self, name)

    @property
    def i(self):
        '''Return a list of wires that will drive this Bus object.'''
        if not self.i_wires:
            self.i_wires = IWireBus([Wire(self.val[i]) for i in range(self.width)])
            wires_bus = ConcatSignal(*reversed(self.i_wires))
            _sig_xfer(wires_bus, self)
        return self.i_wires

    @property
    def o(self):
        '''Return a list of wires carrying the bit values of the Bus wires.'''
        if not self.o_wires:
            self.o_wires = OWireBus([self(i) for i in range(self.width)])
        return self.o_wires

class WireBus(list):
    '''List of Wire objects.'''
    def __init__(self, *args, **kwargs):
        super(WireBus, self).__init__(*args, **kwargs)

    def __getitem__(self, slice_):
        if isinstance(slice_, slice):
            slice_ = slice(slice_.stop, slice_.start)
            return type(self)(super(WireBus, self).__getitem__(slice_))
        elif isinstance(slice_, int):
            return super(WireBus, self).__getitem__(slice_)

class OWireBus(WireBus):
    '''List of output Wire objects driven from a Bus object.'''
    def __init__(self, *args, **kwargs):
        super(OWireBus, self).__init__(*args, **kwargs)

    @property
    def o(self):
        '''Get the output bus of an output bus which is the bus itself.'''
        return self

    @property
    def i(self):
        '''Raise an exception if trying to get an input bus from an output bus.'''
        raise Exception('Attempting to get inputs from the outputs of a Bus.')

class IWireBus(WireBus):
    '''List of input Wire objects that drive a Bus object.'''
    def __init__(self, *args, **kwargs):
        super(IWireBus, self).__init__(*args, **kwargs)

    @property
    def i(self):
        '''Get the input bus of an input bus which is the bus itself.'''
        return self

    @property
    def o(self):
        '''Raise an exception if trying to get an output bus from an input bus.'''
        raise Exception('Attempting to get outputs from the inputs of a Bus.')

    def __setitem__(self, slice_, value):
        '''Drive selected bits of a bus to a value.'''

        # Turn integer index into a slice object.
        if isinstance(slice_, int):
            slice_ = slice(slice_+1, slice_)  # single bit slice.

        # Convert value into a bit-vector object.
        try:
            bv = intbv(value.val)  # Do this if the value iss a Signal.
        except AttributeError:
            bv = intbv(value)  # Do this if the value is an integer.

        # Set individual wires in this bus to bit values.
        for indx, wire in enumerate(self[slice_]):
            _sig_xfer(Signal(bv[indx]), wire)


############## Simulation. #################

def initialize():
    '''Initialize the use of pygmyhdl module.'''
    global _instances
    _instances = list() # Remove any created instances.
    Peeker.clear()      # Remove any signal peekers.

def simulate(*modules):
    '''Run a simulation with a set of modules.'''
    def flatten(nested_list):
        '''Flatten list-of-lists instances into a flat list of instances.'''
        lst = []
        for item in nested_list:
            if isinstance(item, (list, tuple)):
                lst.extend(flatten(item))
            else:
                lst.append(item)
        return lst

    # Combine all the explicit and internal instances into a single set.
    all_modules = set(flatten(modules))
    all_modules.update(flatten(_instances))
    all_modules.update(Peeker.instances())

    # Simulate the set of instances.
    Simulation(*all_modules).run()

def _get_max(signal):
    '''Get maximum value of a signal.'''
    return signal.max or 2**len(signal)

def _get_min(signal):
    '''Get minimum value of a signal.'''
    return signal.min or 0

def _random_test(*signals, **kwargs):
    '''
    Generate a set of test vectors with random values assigned to the signals.
    Parameters:
        signals: One or more signals.
        num_tests: Number of random test vectors to simulate.
        dly: Time delay between changes of the clock signal.
    '''
    dly = kwargs.get('dly', 1)
    num_tests = kwargs.get('num_tests', 10)
    for _ in range(num_tests):
        for sig in signals:
            # Assign a random value within the allowable range of this signal.
            sig.next = random.randrange(_get_min(sig), _get_max(sig))
        yield delay(dly)

def random_sim(*signals, **kwargs):
    '''
    Run a simulation with a set of random test vectors.
    Parameters:
        signals: One or more signals.
        num_tests: Number of random test vectors to simulate.
        dly: Time delay between changes of the clock signal.
    '''
    simulate(_random_test(*signals, **kwargs))
    
def _exhaustive_test(*signals, **kwargs):
    '''
    Generate all possible test vectors for a set of signals.
    Parameters:
        signals: One or more signals.
        dly: Time delay between changes of the clock signal.
    '''
    dly = kwargs.get('dly', 1)
    if len(signals) == 0:
        yield delay(dly)
    else:
        for signals[0].next in range(_get_min(signals[0]), _get_max(signals[0])):
            #yield from exhaustive_test(*signals[1:])
            for d in _exhaustive_test(*signals[1:]):
                yield d

def exhaustive_sim(*signals, **kwargs):
    '''
    Run a simulation with an exhaustive set of test vectors.
    Parameters:
        signals: One or more signals.
        dly: Time delay between changes of the clock signal.
    '''
    simulate(_exhaustive_test(*signals, **kwargs))

def _clk_test(clk, **kwargs):
    '''
    Strobe a clock signal for a number of cycles.
    Parameters:
        num_cycles: Number of clock cycles to execute.
        dly: Time delay between changes of the clock signal.
    '''
    dly = kwargs.get('dly', 1)
    num_cycles = kwargs.get('num_cycles', 10)
    for _ in range(num_cycles):
        clk.next = 0
        yield delay(dly)
        clk.next = 1
        yield delay(dly)

def clk_sim(clk, **kwargs):
    '''
    Run a simulation for a number of clock cycles.
    Parameters:
        num_cycles: Number of clock cycles to execute.
        dly: Time delay between changes of the clock signal.
    '''
    simulate(_clk_test(clk, **kwargs))

def _vector_test(*vectors, **kwargs):
    '''
    Apply vectors of values to signals.
    Parameters:
        vectors: Each vector is a two-element list with a Signal as the first
            element and a list of values as the second element.
        num_cycles: Number of clock cycles to execute.
        dly: Time delay between changes of the clock signal.
    '''
    dly = kwargs.get('dly', 1)
    try:
        num_cycles = max([len(v[1]) for v in vectors])
    except ValueError:
        num_cycles = 0
    num_cycles = kwargs.get('num_cycles', num_cycles)

    for i in range(num_cycles):
        for v in vectors:
            try:
                v[0].next = v[1][i]
            except IndexError:
                v[0].next = v[1][-1]
        yield delay(1)

def vector_sim(*vectors, **kwargs):
    simulate(_vector_test(*vectors, **kwargs))
