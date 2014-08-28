# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import io

import pandas as pd
import numpy as np

from sktracker.utils import progress_apply
from sktracker.utils import print_progress


def test_print_progress():
    out = io.StringIO()
    print_progress(15, out=out)
    output = out.getvalue().strip()
    bar = "15% [======>                                          ]"
    assert bar == output


def test_print_progress_remove_bar():
    out = io.StringIO()
    print_progress(-1, out=out)
    output = out.getvalue().strip()
    bar = ""
    assert bar == output


def test_progress_apply():
    df = pd.DataFrame(np.random.choice(range(100), (1000000, 4)), columns=['A', 'B', 'C', 'D'])
    gp = df.groupby('A')
    out = io.StringIO()
    progress_apply(gp, lambda x: np.sqrt((x**2) / 1e99), out=out)
    progress = out.getvalue().strip()
    assert '50% [========================>                         ]' in progress
