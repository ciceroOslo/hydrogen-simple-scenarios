import numpy as np

from hydrogen_simple_scenarios import scenario_info, ssp_data_extraction

data_path = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/SSP_CMIP6_201811.csv"
data_path_iam = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/SSP_IAM_V2_201811.csv"


def test_get_sector_string():
    test1 = ssp_data_extraction.get_sector_string("CO")
    assert test1 == "CMIP6 Emissions|CO"
    test2 = ssp_data_extraction.get_sector_string("CO", filetype="RCMIP")
    assert test2 == "Emissions|CO"
    test3 = ssp_data_extraction.get_sector_string(
        "CO", sector="Not a sector", filetype="Other"
    )
    assert test3 == "Not a sector|CO"
    test4 = ssp_data_extraction.get_sector_string(
        "CO", sector="Agriculture", filetype="RCMIP"
    )
    assert test4 == "Emissions|CO|MAGICC AFOLU|Agriculture"
    test5 = ssp_data_extraction.get_sector_string(
        "CO", sector="Aircraft", filetype="RCMIP"
    )
    assert test5 == "Emissions|CO|MAGICC Fossil and Industrial|Aircraft"


def test_get_data_for_component_sector_region_ssp():
    ssp = "ssp585"
    region = "World"
    species = "CO"
    co_global = ssp_data_extraction.get_data_for_component_sector_region_ssp(
        data_path, ssp, species, region=region
    )
    assert co_global.shape == (1, 15)
    numbers = np.zeros(10)
    for sector in ssp_data_extraction.co_ssp_sectors:
        test = ssp_data_extraction.get_data_for_component_sector_region_ssp(
            data_path, ssp, species, sector, region=region
        )
        if test.shape == (0, 15):
            continue
        numbers = numbers + test.iloc[0, 5:].to_numpy(dtype=float)
    assert np.allclose(numbers, co_global.iloc[0, 5:].to_numpy(dtype=float))


def test_get_unique_scenarios_and_models():
    unique_full = ssp_data_extraction.get_unique_scenarios_and_models(data_path_iam)
    unique_shorter = ssp_data_extraction.get_unique_scenarios_and_models(data_path)
    assert unique_full.size > unique_shorter.size


def test_get_ts_component_sector_regtion_ssp():
    test_ts1 = ssp_data_extraction.get_ts_component_sector_region_ssp(
        data_path, scen="ssp585", comp="H2"
    )
    test_ts2 = ssp_data_extraction.get_ts_component_sector_region_ssp(
        data_path, scen="ssp585", comp="H2", sector="Aircraft"
    )
    test_ts3 = ssp_data_extraction.get_ts_component_sector_region_ssp(
        data_path_iam, scen="ssp585", comp="CO", filetype="RCMIP"
    )
    assert test_ts1.shape == test_ts2.shape
    print(test_ts2)
    assert np.all(test_ts1 >= test_ts2)
    assert test_ts3.shape == test_ts3.shape


def test_get_ts_energy_and_mass():
    test_ts1 = ssp_data_extraction.get_ts_hydrogen_energy_and_mass(
        data_path_iam, scen="ssp585"
    )
    assert np.allclose(
        test_ts1[0], test_ts1[1] / scenario_info.H2_ENERGY_TO_MASS_CONV_FACTOR
    )


def test_get_years():
    years = ssp_data_extraction.get_years(data_path)
    assert len(years) == 10
    assert np.all(years.values[1:].astype(int) == np.arange(2020, 2110, 10))
