import numpy as np
import pandas as pd

from hydrogen_simple_scenarios import (
    get_emissions_functions,
    scenario_info,
    timeseries_functions,
)


def test_various_timeseries_functions():
    ts_test1 = timeseries_functions.make_linear_replacement_timeseries()
    assert len(ts_test1) == 27
    assert ts_test1[0] == 0
    assert ts_test1[-1] == 0.5
    ts_test2 = timeseries_functions.make_linear_replacement_timeseries(
        start_year=1948, end_year=1974, target_rep=1.0
    )
    assert len(ts_test2) == 27
    assert np.allclose(ts_test2, 2 * ts_test1)

    h2_tot_test = 100
    leak_rate = np.random.uniform(high=0.1)
    assert np.allclose(
        timeseries_functions.get_hydrogen_available(h2_tot_test, leak_rate)
        * (1 + leak_rate),
        h2_tot_test,
    )

    sum_need_test = timeseries_functions.get_hydrogen_used(
        ts_test1, leak_rate, h2_tot_test
    )
    assert sum_need_test > np.sum(ts_test1 * h2_tot_test)

    df_test_set_tot = get_emissions_functions.get_sector_column("Total")
    years = np.arange(2024, 2050 + 1)
    test_emis = timeseries_functions.make_emission_ts(df_test_set_tot, ts_test1, years)
    assert isinstance(test_emis, pd.DataFrame)

    assert test_emis.shape == (len(years) + 1, df_test_set_tot.shape[1])

    test_emis_with_leak = timeseries_functions.add_leakage_ts(
        test_emis, ts_test1, years, leak_rate, h2_tot_test
    )

    assert test_emis_with_leak.shape == (len(years) + 1, df_test_set_tot.shape[1])
    assert np.allclose(
        timeseries_functions.add_leakage_ts(
            df_test_set_tot, ts_test1, years, 0, h2_tot_test
        ).values,
        test_emis.values,
    )

    test_emis_with_leak_prod = timeseries_functions.add_prod_emissions_ts(
        test_emis_with_leak, h2_tot_test, scenario_info.green, years, ts_test1
    )
    assert test_emis_with_leak_prod.shape == (len(years) + 1, df_test_set_tot.shape[1])
    assert np.allclose(test_emis_with_leak.values, test_emis_with_leak_prod.values)

    gwp_normal = timeseries_functions.calc_GWP(test_emis_with_leak_prod, years)
    gwp_co2 = timeseries_functions.calc_GWP(
        test_emis_with_leak_prod, years, just_CO2=True
    )

    assert gwp_normal > gwp_co2

    gwp20 = timeseries_functions.calc_GWP20(test_emis_with_leak_prod, years)
    gwp20_co2 = timeseries_functions.calc_GWP20(
        test_emis_with_leak_prod, years, just_CO2=True
    )
    assert gwp20 > gwp_normal
    assert gwp20_co2 == gwp_co2

    gwpstar = timeseries_functions.calc_GWP_star(test_emis_with_leak_prod, years)
    gwpstar_co2 = timeseries_functions.calc_GWP_star(
        test_emis_with_leak_prod, years, just_CO2=True
    )
    assert gwpstar[0].sum() > gwp20
    assert np.allclose(gwpstar_co2[0], gwpstar_co2[1])

    temp_equiv_tot = timeseries_functions.transform_GWP_series_to_mitigated_warming(
        gwpstar[0]
    )
    temp_equiv_tot_co2 = timeseries_functions.transform_GWP_series_to_mitigated_warming(
        gwpstar_co2[0]
    )

    assert np.all(temp_equiv_tot >= temp_equiv_tot_co2)
