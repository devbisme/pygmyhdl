===============================
PygMyHDL
===============================

.. image:: https://img.shields.io/pypi/v/pygmyhdl.svg
        :target: https://pypi.python.org/pypi/pygmyhdl


PygMyHDL is a thin wrapper around `MyHDL <myhdl.org>`_. MyHDL lets you design
and simulate digital hardware using Python. PygMyHDL does the same thing,
but tries to make it a little simpler. Think of it as "MyHDL on training wheels".
Once you get enough experience with PygMyHDL, you'll probably cast it aside
and just use straight MyHDL. That's OK; that's why I invented it.

* Free software: MIT license

* Documentation: http://xesscorp.github.io/pygmyhdl


Features
--------

PygMyHDL adds the following features to MyHDL:

* ``Wire`` and ``Bus`` classes for declaring single-bit and multi-bit digital signals.

* ``Bus`` objects have ``.o`` and ``.i`` properties that are used to get the value on a
  bus (that's the ``.o`` property) and to drive values onto a bus (using the ``.i`` property).

* ``State`` objects are used to declare state variables for finite-state machines.
  Each ``State`` object also stores all the defined states in its ``s`` attribute
  for use in making comparisons to states or updating state values.

* The ``@chunk`` decorator is used to indicate a function will create one or more
  pieces of logic circuitry. These pieces will be implicitly gathered into a
  list of logic instances that can be simulated and synthesized later.
  (MyHDL requires you to explicitly store logic instances into Python variables
  so they can be found and processed later.)

* The decorators ``@comb_logic`` and ``@seq_logic`` are used to declare functions that
  perform combinational and sequential logic operations, respectively. (These
  are almost identical to MyHDL's ``@always_comb`` and ``@always_seq`` decorators
  except they assist with the implicit instantiation of logic.)

* Helper functions are provided for testing a digital design using random test
  vectors, exhaustive test vectors, user-defined test vectors, or a simple clock signal.

* The `myhdlpeek module <xesscorp.github.io/myhdlpeek>`_ is used to display the
  results of logic simulations as waveforms or tables.


Getting Started
------------------

Below are some examples of Jupyter notebooks using PygMyHDL.
Unfortunately, the Github Notebook viewer doesn't render the waveform displays
so you'll have to download and run the notebooks locally or click on the static HTML
link to see what PygMyHDL can do.

* The Fastest, Easiest FPGA Blinker, Ever!:
  `[Notebook1] <https://github.com/xesscorp/pygmyhdl/blob/master/examples/1_blinker/fastest_easiest_FPGA_blinker_ever.ipynb>`_ 
  `[HTML1] <https://xess.com/myhdlpeek/docs/_build/singlehtml/notebooks/fastest_easiest_FPGA_blinker_ever.html>`_

* Hierarchy and Abstraction and Ursidae, Oh My!:
  `[Notebook2] <https://github.com/xesscorp/pygmyhdl/blob/master/examples/2_hierarchy/hierarchy_and_abstraction_and_ursidae_oh_my.ipynb>`_
  `[HTML2] <https://xess.com/myhdlpeek/docs/_build/singlehtml/notebooks/hierarchy_and_abstraction_and_ursidae_oh_my.html>`_

* Pulse Width Modulators:
  `[Notebook3] <https://github.com/xesscorp/pygmyhdl/blob/master/examples/3_pwm/pwm.ipynb>`_ 
  `[HTML3] <https://xess.com/myhdlpeek/docs/_build/singlehtml/notebooks/examples/3_pwm/pwm.html>`_

* Block (RAM) Party!:
  `[Notebook4] <https://github.com/xesscorp/pygmyhdl/blob/master/examples/4_blockram/block_ram_party.ipynb>`_ 
  `[HTML4] <https://xess.com/myhdlpeek/docs/_build/singlehtml/notebooks/4_blockram/block_ram_party.html>`_

* FSMs Without Monsters!:
  `[Notebook5] <https://github.com/xesscorp/pygmyhdl/blob/master/examples/5_fsm/fsm.ipynb>`_ 
  `[HTML5] <https://xess.com/myhdlpeek/docs/_build/singlehtml/notebooks/5_fsm/fsm.html>`_

|
