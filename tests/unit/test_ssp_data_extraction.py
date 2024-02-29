import os

import numpy as np

from hydrogen_simple_scenarios import ssp_data_extraction

data_path = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/SSP_CMIP6_201811.csv"

def test_get_sector_string():
    test1 = ssp_data_extraction.get_sector_string("CO")
    assert test1 == "CMIP6 Emissions|CO"


def test_get_data_for_component_sector_region_ssp():
    co_global = ssp_data_extraction.get_data_for_component_sector_region_ssp(data_path, "ssp245", "CO")
    print(co_global)
    assert co_global.shape == (1,15)
    
    numbers = np.zeros(10)
    for sector in ssp_data_extraction.co_ssp_sectors:
        print(sector)
        test = ssp_data_extraction.get_data_for_component_sector_region_ssp(data_path, "ssp245", "CO", sector)
        numbers = numbers + test.iloc[0, 5:].to_numpy(dtype=float)
    assert np.all(np.less_equal(numbers, co_global.iloc[0,5:].to_numpy(dtype=float)))
    assert False


