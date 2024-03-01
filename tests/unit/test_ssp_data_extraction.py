import os

import numpy as np

from hydrogen_simple_scenarios import ssp_data_extraction

data_path = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/SSP_CMIP6_201811.csv"
data_path_iam = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/SSP_IAM_V2_201811.csv"

def test_get_sector_string():
    test1 = ssp_data_extraction.get_sector_string("CO")
    assert test1 == "CMIP6 Emissions|CO"


def test_get_data_for_component_sector_region_ssp():
    n = 1
    ssp = "ssp585"
    region = "World"
    species = "CO"
    co_global = ssp_data_extraction.get_data_for_component_sector_region_ssp(data_path, ssp, species, region=region)
    assert co_global.shape == (1,15) 
    numbers = np.zeros(10)
    for sector in ssp_data_extraction.co_ssp_sectors:
        print(sector)
        test = ssp_data_extraction.get_data_for_component_sector_region_ssp(data_path, ssp, species, sector, region=region)
        if test.shape == (0,15):
            continue
        numbers = numbers + test.iloc[0, 5:].to_numpy(dtype=float)
    assert np.allclose(numbers, co_global.iloc[0,5:].to_numpy(dtype=float))
    assert False

def test_get_unique_scenarios_and_models():
    unique_full = ssp_data_extraction.get_unique_scenarios_and_models(data_path_iam)
    unique_shorter = ssp_data_extraction.get_unique_scenarios_and_models(data_path)
    print(unique_full.shape)
    print(unique_full)
    print(unique_shorter.shape)
    assert unique_full.size > unique_shorter.size
    assert False
