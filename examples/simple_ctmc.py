#!/usr/bin/env python

import sys
import os.path
import numpy as np
# context for the examples
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jmarkov.ctmc import ctmc


Q = np.array([[-4, 1, 3], [2, -5, 3], [1, 2, -3]])

mc = ctmc(Q)
print(mc.generator)

ss = mc.steady_state()
print(ss)