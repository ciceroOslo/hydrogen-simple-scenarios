import os

import numpy as np

from hydrogen_simple_scenarios import ssp_data_extraction

def test_get_data_for_component_sector_region_ssp():
    co_global = ssp_data_extraction.get_data_for_component_sector_region_ssp("/div/amoc/CSCM/SCM_Linux_v2019/input_SSP/SSP_CMIP6_201811.csv", "ssp245", "CO")

    assert False