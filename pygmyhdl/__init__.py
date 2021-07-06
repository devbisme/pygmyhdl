# -*- coding: utf-8 -*-

'''
PygMyHDL is a thin wrapper around MyHDL (myhdl.org). MyHDL lets you design
and simulate digital hardware using Python. PygMyHDL does the same thing,
but tries to make it a little simpler. Think of it as "MyHDL on training wheels".
Once you get enough experience with PygMyHDL, you'll probably cast it aside
and just use straight MyHDL. That's OK; that's why I invented it.

PygMyHDL adds the following features to MyHDL:

* Wire and Bus classes for declaring single-bit and multi-bit digital signals.

* Bus objects have .o and .i properties that are used to get the value on a
  Bus (that's the .o property) and to drive values onto a Bus (using the .i property).

* The @chunk decorator is used to indicate a function will create one or more
  pieces of logic circuitry. These pieces will be implicitly gathered into a
  list of logic instances that can be simulated and synthesized later.
  (MyHDL requires you to explicitly store logic instances into Python variables
  so they can be found and processed later.)

* The decorators @comb_logic and @seq_logic are used to declare functions that
  perform combinational and sequential logic operations, respectively. (These
  are almost identical to MyHDL's @always_comb and @always_seq decorators
  except they assist with the implicit instantiation of logic.)

* Helper functions are provided for testing a digital design using random test
  vectors, exhaustive test vectors, user-defined test vectors, or a simple clock signal.

* The myhdlpeek module (devbisme.github.io/myhdlpeek) is used to display the
  results of logic simulations as both waveforms or tables.
'''



from myhdl import *
from myhdlpeek import *
from .pygmyhdl import *
from .pckg_info import version
