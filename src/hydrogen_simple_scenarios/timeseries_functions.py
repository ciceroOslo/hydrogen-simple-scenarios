import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

import get_emissions_functions


def make_linear_replacement_timeseries(start_year=2024, end_year=2050, target_rep=0.5):
    years_here = range(start_year, end_year + 1)
    values = np.linspace(0, target_rep, num=len(years_here))
    return values


def make_emission_ts(df_repl, ts, years):
    df_repl_ts = df_repl.copy()
    for i, ts in enumerate(ts):
        df_repl_ts.loc[years[i]] = df_repl.loc["Total"] * ts
    return df_repl_ts


def add_leakage_ts(df_repl, ts, years, leak_rate, h2_repl_need):
    df_repl_ts_leak = make_emission_ts(df_repl, ts, years)
    if leak_rate > 0:
        for i, year in enumerate(years):
            df_repl_ts_leak.loc[year] = get_emissions_functions.add_leakage(
                df_repl_ts_leak.loc[year], ts[i] * h2_repl_need, leak_rate
            ).values.flatten()
    # print(df_repl_ts_leak)
    return df_repl_ts_leak


def add_prod_emissions_ts(df_repl_ts_leak, h2_repl_need, emis_per_unit_h2, years, ts):
    for i, year in enumerate(years):
        df_repl_ts_leak.loc[year] = get_emissions_functions.add_prod_emissions(
            df_repl_ts_leak.loc[year], ts[i] * h2_repl_need, emis_per_unit_h2
        ).values.flatten()
        print(df_repl_ts_leak.loc[year])
    return df_repl_ts_leak


def get_hydrogen_used(ts, years, leak_rate, h2_repl_need):
    per_year_h2 = ts * h2_repl_need * (1 + leak_rate)
    return per_year_h2.sum()


def calc_GWP(df_repl_ts, years):
    sum_GWP = 0
    for year in years:
        for comp, factor in get_emissions_functions.GWP_dict.items():
            # print(df_repl_ts.columns)
            # print(df_repl_ts[comp])
            if get_emissions_functions.just_CO2 and comp not in ["H2", "CO2"]:
                continue
            sum_GWP = sum_GWP + df_repl_ts[comp][year] * factor
        # sys.exit(4)
    return sum_GWP
