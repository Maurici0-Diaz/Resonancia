#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import numpy as np

#genera vector con zeros para extender las series hasta tener 2^n elementos
def relleno_zeros(x):
    l_original=len(x)
    n_exp=np.ceil(np.log2(l_original))
    n_exp=n_exp.astype(int)
    l_ext=2**n_exp
    zeros=[0]*(l_ext-l_original)
    x_ext=np.append(x,zeros)
    return x_ext

