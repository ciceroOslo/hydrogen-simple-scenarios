import numpy as np
from hydrogen_simple_scenarios import timeseries_functions

def test_various_timeseries_functions():
    ts_test1 = timeseries_functions.make_linear_replacement_timeseries()
    assert len(ts_test1) == 27
    assert ts_test1[0] == 0
    assert ts_test1[-1] == 0.5
    ts_test2 = timeseries_functions.make_linear_replacement_timeseries(start_year = 1948, end_year = 1974, target_rep = 1.)
    assert len(ts_test2) == 27
    assert np.allclose(ts_test2, 2*ts_test1)
