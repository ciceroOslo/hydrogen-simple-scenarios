import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from .get_emissions_functions import add_leakage, add_prod_emissions, GWP_dict, GWP20_dict


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
            df_repl_ts_leak.loc[year] = add_leakage(
                df_repl_ts_leak.loc[year], ts[i] * h2_repl_need, leak_rate
            ).values.flatten()
    # print(df_repl_ts_leak)
    return df_repl_ts_leak


def add_prod_emissions_ts(df_repl_ts_leak, h2_repl_need, emis_per_unit_h2, years, ts):
    for i, year in enumerate(years):
        df_repl_ts_leak.loc[year] = add_prod_emissions(
            df_repl_ts_leak.loc[year], ts[i] * h2_repl_need, emis_per_unit_h2
        ).values.flatten()
        #print(df_repl_ts_leak.loc[year])
    return df_repl_ts_leak


def get_hydrogen_used(ts, leak_rate, h2_repl_need):
    per_year_h2 = ts * h2_repl_need * (1 + leak_rate)
    return per_year_h2.sum()

def get_hydrogen_available(h2_total, leak_rate):
    h2_avail = h2_total/(1+ leak_rate)
    return h2_avail


def calc_GWP(df_repl_ts, years, just_CO2 = False):
    sum_GWP = 0
    for year in years:
        for comp, factor in GWP_dict.items():
            # print(df_repl_ts.columns)
            # print(df_repl_ts[comp])
            if just_CO2 and not comp in ["CO2"]:
                continue
            sum_GWP = sum_GWP + df_repl_ts[comp][year] * factor
        # sys.exit(4)
    return sum_GWP

def calc_GWP20(df_repl_ts, years, just_CO2 = False):
    sum_GWP = 0
    for year in years:
        for comp, factor in GWP20_dict.items():
            # print(df_repl_ts.columns)
            # print(df_repl_ts[comp])
            if just_CO2 and not comp in ["CO2"]:
                continue
            sum_GWP = sum_GWP + df_repl_ts[comp][year] * factor
        # sys.exit(4)
    return sum_GWP

def calc_GWP_star(df_repl_ts, years, just_CO2=False):
    sum_GWP_star = np.zeros(len(years))
    sum_GWP_just_CO2 = np.zeros(len(years))
    sum_GWP_star_per_component = np.zeros((len(GWP_dict)-1, len(years)))
    for i, year in enumerate(years):
        #print(f"i:{i} and year: {year}")
        j_non_CO2 = 0
        for comp, factor in GWP_dict.items():
            # For CO2 cumulative value: 
            if comp == "CO2":
                if i > 0:
                    sum_GWP_just_CO2[i] = sum_GWP_just_CO2[i-1]
                sum_GWP_just_CO2[i] = sum_GWP_just_CO2[i] + df_repl_ts[comp][year] 
                sum_GWP_star[i] = sum_GWP_star[i] + sum_GWP_just_CO2[i]
            # TODO: Redo this to cumulate right way for GWP*
            elif not just_CO2: # or comp == "H2":
                if i > 1:
                    sum_GWP_star_per_component[j_non_CO2, i] = sum_GWP_star_per_component[j_non_CO2, i-1]
                to_multiply = 4*df_repl_ts[comp][year]
                if i >= 20:
                    #print(comp)
                    #print(f"Value from last year: {sum_GWP_star_per_component[j_non_CO2, i]}")
                    to_multiply = to_multiply - 3.75*df_repl_ts[comp][year -20]
                #print(f"From this year: {to_multiply*factor}")
                sum_GWP_star_per_component[j_non_CO2, i] = sum_GWP_star_per_component[j_non_CO2, i] + to_multiply*factor
                #print(f"Value for this year: {sum_GWP_star_per_component[j_non_CO2, i]}")
                sum_GWP_star[i] = sum_GWP_star[i] + sum_GWP_star_per_component[j_non_CO2, i]
                j_non_CO2 = j_non_CO2 + 1
    return sum_GWP_star, sum_GWP_just_CO2, sum_GWP_star_per_component

def transform_GWP_series_to_mitigated_warming(CO2_equiv_timeseries, TCRE = 0.4e-6):
    return CO2_equiv_timeseries*TCRE
