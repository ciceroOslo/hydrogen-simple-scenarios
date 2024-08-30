import numpy as np

from hydrogen_simple_scenarios import get_emissions_functions, scenario_info


def test_soToHydrogenEmissionsConverter():
    converter_1 = get_emissions_functions.COToHydrogenEmissionsConverter()
    converter_2 = get_emissions_functions.COToHydrogenEmissionsConverter(ignore_bb=True)
    converter_3 = get_emissions_functions.COToHydrogenEmissionsConverter(just_CO2=True)
    # Testing get_co_to_h2_factor_burning_cmip6
    assert converter_1.get_co_to_h2_factor_burning_cmip6("Peat Burning") == 1.2 / 182
    assert converter_2.get_co_to_h2_factor_burning_cmip6("Peat Burning") == 0
    assert converter_1.get_co_to_h2_factor_burning_cmip6(
        "Grassland Burning"
    ) == converter_1.get_co_to_h2_factor_burning_cmip6("Savanna")
    assert converter_1.get_co_to_h2_factor_burning_cmip6(
        "Forest Burning"
    ) == converter_1.get_co_to_h2_factor_burning_cmip6("Extratropical Forest")
    assert converter_1.get_co_to_h2_factor_burning_cmip6(
        "Typo"
    ) == converter_1.get_co_to_h2_factor_burning_cmip6("Garbage Burning")
    assert (
        converter_3.get_co_to_h2_factor_burning_cmip6("Agricultural Waste Burning") == 0
    )
    # Testing get_co_to_h2_factor
    assert converter_1.get_co_to_h2_factor("5B") == 0.005
    assert converter_2.get_co_to_h2_factor("1A4b") == 0.0217
    assert converter_2.get_co_to_h2_factor("1A4c") == 0.0357
    assert converter_3.get_co_to_h2_factor("1A4b") == 0
    assert converter_2.get_co_to_h2_factor("7C") == 0.0143
    # Testing get_co_to_h2_factor_cmip6
    assert converter_2.get_co_to_h2_factor(
        "1A4c"
    ) == converter_1.get_co_to_h2_factor_cmip6("Random")
    assert converter_1.get_co_to_h2_factor(
        "7C"
    ) == converter_2.get_co_to_h2_factor_cmip6("Energy sector")
    assert converter_2.get_co_to_h2_factor_cmip6("Agricultural Waste Burning") == 0
    assert (
        converter_1.get_co_to_h2_factor_cmip6("Agricultural Waste Burning")
        == 2.59 / 102
    )


def test_prepare_emis_df():
    data_emis_yr_1 = get_emissions_functions.prepare_emis_df("CO", "sector")
    data_emis_yr_2 = get_emissions_functions.prepare_emis_df("CO", "fuel")
    assert data_emis_yr_1.shape == (60,)
    assert data_emis_yr_2.shape == (9,)


def test_get_sector_column():
    sector_column = get_emissions_functions.get_sector_column("Total")
    assert sorted(sector_column.columns) == sorted(
        ["H2", "CO2", "CO", "CH4", "NMVOC", "NOx"]
    )
    assert (sector_column.shape) == (1, 6)
    print(sector_column)
    sector_column2 = get_emissions_functions.get_sector_column(
        "natural_gas", type_split="fuel"
    )
    assert sorted(sector_column2.columns) == sorted(
        ["H2", "CO2", "CO", "CH4", "NMVOC", "NOx"]
    )
    assert np.all(sector_column2.values < sector_column.values)

    sector_column3 = get_emissions_functions.get_sector_column_total(
        "natural_gas", type_split="fuel"
    )
    assert np.allclose(sector_column3.values, sector_column2.values)
    tot_sector = np.zeros_like(sector_column3.values)
    for key, value in scenario_info.steel_sectors.items():
        tot_sector = (
            tot_sector
            + get_emissions_functions.get_sector_column_total([key]).values * value[0]
        )

    assert np.allclose(
        tot_sector,
        get_emissions_functions.get_sector_column_total(
            scenario_info.steel_sectors
        ).values,
    )
