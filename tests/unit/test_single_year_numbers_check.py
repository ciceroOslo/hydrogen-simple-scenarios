import os

import numpy as np
import pandas as pd

from hydrogen_simple_scenarios import single_year_numbers_check

def test_get_benefit_loss_df():
    benefit_loss = single_year_numbers_check.get_benefit_loss_df("steel")
    assert isinstance(benefit_loss, pd.DataFrame)
    assert benefit_loss.shape == (4,3)
    assert np.all(benefit_loss.values <= 0.0)