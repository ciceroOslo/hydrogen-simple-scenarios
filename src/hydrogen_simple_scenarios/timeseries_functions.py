"""
Make various timeseries functions
"""

import numpy as np

from .get_emissions_functions import (
    GWP20_dict,
    GWP_dict,
    add_leakage,
    add_prod_emissions,
)


def make_linear_replacement_timeseries(start_year=2024, end_year=2050, target_rep=0.5):
    """
    Make timeseries with linear growth from 0 to target replacement ratio

    Parameters
    ----------
    start_year : int
        Year of start of replacement
    end_year : int
        Year when replacement target should be reached
    target_rep : float
        Target replacement ratio should be between 0 and 1
    Returns
    -------
    np.ndarray
        With linearly growing values from zero to target_rep
        with lenght equal to the number of years from start_year to end_year
    """
    years_here = range(start_year, end_year + 1)
    values = np.linspace(0, target_rep, num=len(years_here))
    return values


def make_emission_ts(df_repl, ts, years):
    """
    Make emissions timeseries

    Parameters
    ----------
    df_repl : pd.DatFrame
        A dataframe with emissions values for each compound for a total sector
    ts : np.ndarray
        Timeseries of replacement ratios
    years : np.ndArray
        Array of the years for which the replacement timeseries is given

    Returns
    -------
    pd.DataFrame
        With values of replaced emissions for each year in the timeseries
    """
    df_repl_ts = df_repl.copy()
    for i, ts_val in enumerate(ts):
        df_repl_ts.loc[years[i]] = df_repl.loc["Total"] * ts_val
    return df_repl_ts


def add_leakage_ts(df_repl, ts, years, leak_rate, h2_repl_need):
    """
    Add hydrogen leakage to replacement timeseries

    Parameters
    ----------
    df_repl : pd.DataFrame
        A dataframe with emissions per year being replaced
    ts : np.ndarray
        Timeseries of replacement ratios
    years : np.ndArray
        Array of the years for which the replacement timeseries is given
    leak_rate : float
        Leak rate for hydrogen, should be in the range 0 to 1, most likely 0.1 or below
    h2_repl_need : float
        The amount of H2 needed for total replacement of the sector

    Returns
    -------
    pd.DataFrame
        With values of replaced emissions for each year in the timeseries
        and hydrogen leaks accounted for
    """
    df_repl_ts_leak = make_emission_ts(df_repl, ts, years)
    if leak_rate > 0:
        for i, year in enumerate(years):
            df_repl_ts_leak.loc[year] = add_leakage(
                df_repl_ts_leak.loc[year], ts[i] * h2_repl_need, leak_rate
            ).values.flatten()
    # print(df_repl_ts_leak)
    return df_repl_ts_leak


def add_prod_emissions_ts(df_repl_ts_leak, h2_repl_need, emis_per_unit_h2, years, ts):
    """
    Add production emissions to replacement timeseries

    Parameters
    ----------
    df_repl_ts_leak : pd.DataFrame
        A dataframe with emissions per year being replaced and hydrogen accounted for
    emis_per_unit_h2 : pd.DataFrame or dict
        With emissions per compound per hydrogen unit produced
    h2_repl_need : float
        The amount of H2 needed for total replacement of the sector
    years : np.ndArray
        Array of the years for which the replacement timeseries is given
    ts : np.ndarray
        Timeseries of replacement ratios

    Returns
    -------
    pd.DataFrame
        With values of replaced emissions for each year in the timeseries
        and hydrogen leaks accounted for
    """
    for i, year in enumerate(years):
        df_repl_ts_leak.loc[year] = add_prod_emissions(
            df_repl_ts_leak.loc[year], ts[i] * h2_repl_need, emis_per_unit_h2
        ).values.flatten()
        # print(df_repl_ts_leak.loc[year])
    return df_repl_ts_leak


def get_hydrogen_used(ts, leak_rate, h2_repl_need):
    """
    Get amount of hydrogen that needs to be produced

    Parameters
    ----------
    ts : np.ndarray
        Timeseries of replacement ratios
    leak_rate : float
        Leak rate for hydrogen, should be in the range 0 to 1, most likely 0.1 or below
    h2_repl_need : float
        The amount of H2 needed for total replacement of the sector

    Returns
    -------
    float
        The total amount of hydrogen that needs to be produced accounting for hydrogen leaked
    """
    per_year_h2 = ts * h2_repl_need * (1 + leak_rate)
    return per_year_h2.sum()


def get_hydrogen_available(h2_total, leak_rate):
    """
    Get amount of hydrogen available for use

    Parameters
    ----------
    h2_total : float
        Amount of hydrogen produced
    leak_rate : float
        Leak rate for hydrogen, should be in the range 0 to 1, most likely 0.1 or below

    Returns
    -------
    float
        The total amount of hydrogen available after accounting for leaked amount
    """
    h2_avail = h2_total / (1 + leak_rate)
    return h2_avail


def calc_gwp(df_repl_ts, years, just_CO2=False):
    """
    Calculate accumulated GWP100 for all components ver a timeseries

    Parameters
    ----------
    df_repl_ts : pd.DataFrame
        A dataframe with emissions per year being replaced
    years : np.ndArray
        Array of the years for which the replacement timeseries is given
    just_CO2 : bool
        Whether to only consider direct CO2 impacts

    Returns
    -------
    float
        The accumulated GWP100 of mitigation over the replacement timeseries
    """
    sum_gwp = 0
    for year in years:
        for comp, factor in GWP_dict.items():
            if just_CO2 and comp not in ["CO2"]:
                continue
            sum_gwp = sum_gwp + df_repl_ts[comp][year] * factor
    return sum_gwp


def calc_gwp20(df_repl_ts, years, just_CO2=False):
    """
    Calculate accumulated GWP20 for all components ver a timeseries

    Parameters
    ----------
    df_repl_ts : pd.DataFrame
        A dataframe with emissions per year being replaced
    years : np.ndArray
        Array of the years for which the replacement timeseries is given
    just_CO2 : bool
        Whether to only consider direct CO2 impacts

    Returns
    -------
    float
        The accumulated GWP20 of mitigation over the replacement timeseries
    """
    sum_gwp = 0
    for year in years:
        for comp, factor in GWP20_dict.items():
            if just_CO2 and comp not in ["CO2"]:
                continue
            sum_gwp = sum_gwp + df_repl_ts[comp][year] * factor
    return sum_gwp


def calc_gwp_star(df_repl_ts, years, just_CO2=False):
    """
    Calculate accumulated GWP* for all components ver a timeseries

    Parameters
    ----------
    df_repl_ts : pd.DataFrame
        A dataframe with emissions per year being replaced
    years : np.ndArray
        Array of the years for which the replacement timeseries is given
    just_CO2 : bool
        Whether to only consider direct CO2 impacts

    Returns
    -------
    float
        The accumulated GWP* of mitigation over the replacement timeseries
    """
    sum_gwp_star = np.zeros(len(years))
    sum_gwp_just_co2 = np.zeros(len(years))
    sum_gwp_star_per_component = np.zeros((len(GWP_dict) - 1, len(years)))
    for i, year in enumerate(years):
        # print(f"i:{i} and year: {year}")
        j_non_co2 = 0
        for comp, factor in GWP_dict.items():
            # For CO2 cumulative value:
            if comp == "CO2":
                if i > 0:
                    sum_gwp_just_co2[i] = sum_gwp_just_co2[i - 1]
                sum_gwp_just_co2[i] = sum_gwp_just_co2[i] + df_repl_ts[comp][year]
                sum_gwp_star[i] = sum_gwp_star[i] + sum_gwp_just_co2[i]
            # TODO: Redo this to cumulate right way for GWP*
            elif not just_CO2:  # or comp == "H2":
                if i > 1:
                    sum_gwp_star_per_component[j_non_co2, i] = (
                        sum_gwp_star_per_component[j_non_co2, i - 1]
                    )
                to_multiply = 4 * df_repl_ts[comp][year]
                if i >= 20:
                    # print(comp)
                    # print(f"Value from last year: {sum_gwp_star_per_component[j_non_co2, i]}")
                    to_multiply = to_multiply - 3.75 * df_repl_ts[comp][year - 20]
                # print(f"From this year: {to_multiply*factor}")
                sum_gwp_star_per_component[j_non_co2, i] = (
                    sum_gwp_star_per_component[j_non_co2, i] + to_multiply * factor
                )
                # print(f"Value for this year: {sum_gwp_star_per_component[j_non_co2, i]}")
                sum_gwp_star[i] = (
                    sum_gwp_star[i] + sum_gwp_star_per_component[j_non_co2, i]
                )
                j_non_co2 = j_non_co2 + 1
    return sum_gwp_star, sum_gwp_just_co2, sum_gwp_star_per_component


def transform_gwp_series_to_mitigated_warming(co2_equiv_timeseries, TCRE=0.4e-6):
    """
    Transform mitigated GWP* timeseries into mitigate warming

    Parameters
    ----------
    co2_equiv_timeseries : pd.DataFrame
        A timeseries of CO2_equivalents mitigated per year
    TCRE : float
        TCRE value to use for transformation

    Returns
    -------
    pd.DataFrame
        Timeseries of estimated mitigated warming
    """
    return co2_equiv_timeseries * TCRE
