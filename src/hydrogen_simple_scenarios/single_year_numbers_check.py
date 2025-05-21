"""
Module to get values for single years (not time series)
"""
import sys
import numpy as np
import pandas as pd

from .get_emissions_functions import (
    add_leakage,
    add_prod_emissions,
    get_sector_column_total,
)
from .scenario_info import leak_rates, prod_methods, sector_info_all
from .timeseries_functions import calc_gwp, calc_gwp20, calc_gwp_star


def get_gwp_values_df(sector, just_CO2=False, star=False, gwp20=False):
    """
    Get DataFrame of gwp values for total sector replacement

    Given a sector that is defined in sector_info_all of scenario_info
    the total GWP benefits of replacing current fossil fuel use in this
    sector with hydrogen for each of the scenario_info defined leak_rates
    and prod_methods

    Parameters
    ----------
    sector : str
        Name of sector. Should be one for which values are defined in sector_info_all
    just_CO2 : bool
        Whether to consider just direct CO2 emissions
    star : bool
        Whether to do GWPstar rather than GWP100
    gwp20: bool
        Whether to do GWP20 rather than GWP100
    Returns
    -------
        pd.Dataframe
    """
    df_repl = get_sector_column_total(sector_info_all[sector][0], just_CO2)
    gwp_values = np.zeros(
        (
            len(prod_methods[sector_info_all[sector][2]]),
            len(leak_rates[sector_info_all[sector][2]]),
        )
    )
    leak_rate_name = []
    for j, leak in enumerate(leak_rates[sector_info_all[sector][2]]):
        if isinstance(leak, (float, int)):
            leak_rate_name.append(leak)
        else:
            leak_rate_name.append(leak["name"])
    for i, (prod, prod_emis) in enumerate(  # pylint: disable=unused-variable
        prod_methods[sector_info_all[sector][2]].items()
    ):
        df_prod_now = df_repl.copy()
        print(f"Starting copy: {df_prod_now}")
        df_prod_now = add_prod_emissions(
            df_prod_now, sector_info_all[sector][1], prod_emis
        )
        print(f"Adding production: {df_prod_now}")
        for j, leak in enumerate(leak_rates[sector_info_all[sector][2]]):
            if isinstance(leak, (float, int)):
                tot_leak_loss = leak
            else:
                tot_leak_loss = leak["total"]
            df_with_leak = add_leakage(
                df_prod_now,
                sector_info_all[sector][1] * (1 + tot_leak_loss),
                leak,
                total_unit=sector_info_all[sector][2],
            )
            print(f"With leak: {df_prod_now}")
            if star:
                gwp_values[i, j] = calc_gwp_star(df_with_leak, [0], just_CO2=just_CO2)[
                    0
                ]
            elif gwp20:
                gwp_values[i, j] = calc_gwp20(df_with_leak, [0], just_CO2=just_CO2)
            else:
                gwp_values[i, j] = calc_gwp(df_with_leak, [0], just_CO2=just_CO2)
    print(gwp_values)
    print(f"gwp values for replacement: {gwp_values}")
    print(leak_rates[sector_info_all[sector][2]])
    gwp_df = pd.DataFrame(
        gwp_values,
        index=prod_methods[sector_info_all[sector][2]].keys(),
        columns=leak_rate_name#leak_rates[sector_info_all[sector][2]],
    )
    print(gwp_df.reindex(["Green", "Blue_optimistic", "Blue_compliance"]))
    return gwp_df

def get_energy_loss_replacement_sector(orig_sector, alt_sector, e_loss_rates, just_CO2=False, star=False, gwp20=False):
    df_repl = get_sector_column_total(sector_info_all[alt_sector][0], just_CO2)
    gwp_values = np.zeros(
        (
            len(e_loss_rates),
            len(leak_rates[sector_info_all[orig_sector][2]]),
        )
    )
    leak_rate_name = []
    for j, leak in enumerate(leak_rates[sector_info_all[orig_sector][2]]):
        if isinstance(leak, (float, int)):
            tot_leak_loss = leak
            leak_rate_name.append(leak)
        else:
            tot_leak_loss = leak["total"]
            leak_rate_name.append(leak["name"])
        # Total energy need per unit energy:
        for i, e_loss in enumerate(e_loss_rates):
            e_need = (1 + tot_leak_loss)/(e_loss)
            # Energy lost to inefficient production + lost to leaks
            e_lost_from_direct = e_need * (1 - e_loss) + e_need * (e_loss) * tot_leak_loss
            recalc_factor =  e_lost_from_direct  # * sector_info_all[orig_sector][1] / sector_info_all[alt_sector][1]
            print(e_loss)
            print(e_lost_from_direct)
            if star:
                gwp_values[i, j] = calc_gwp_star(df_repl, [0], just_CO2=just_CO2)[
                    0
                ] * recalc_factor
            elif gwp20:
                gwp_values[i, j] = calc_gwp20(df_repl, [0], just_CO2=just_CO2) * recalc_factor
            else:
                gwp_values[i, j] = calc_gwp(df_repl, [0], just_CO2=just_CO2) * recalc_factor
    print(gwp_values)
    print(leak_rates[sector_info_all[orig_sector][2]])
    #print(sys.exit(4))
    gwp_df = pd.DataFrame(
        gwp_values/sector_info_all[alt_sector][1],
        index=e_loss_rates,
        columns=leak_rate_name,
    )
    return gwp_df 
            


def make_column_names_from_leak_rate(leak_rate):
    """
    Make leak_rate definition into column name

    Method to handle that leak rates can be single numbers
    or whole lists of total and compoundwise leak rates with
    names

    Parameters
    ----------
    leak_rate : obj
        If number this number will just be returned
        Otherwise it should be a dict and the entry for
        the key 'name' will be returned

    Returns
    -------
    obj
        float or int if leak_rate is this type, otherwise
        the str that is the entry for the key name in the leak_rate
        dict
    """
    if isinstance(leak_rate, (float, int)):
        return leak_rate
    return leak_rate["name"]


def get_gwp_values_per_hydrogen_used(sector, just_CO2=False, star=False, gwp20=False):
    """
    Get DataFrame of gwp replacement per Tg H2 employed

    Given a sector that is defined in sector_info_all of scenario_info
    the per Tg hydrogen benefit of replacing current fossil fuel use in this
    sector with hydrogen for each of the scenario_info defined leak_rates
    and prod_methods

    Parameters
    ----------
    sector : str
        Name of sector. Should be one for which values are defined in sector_info_all
    just_CO2 : bool
        Whether to consider just direct CO2 emissions
    star : bool
        Whether to do GWPstar rather than GWP100
    gwp20: bool
        Whether to do GWP20 rather than GWP100

    Returns
    -------
        pd.Dataframe
    """
    gwp_values = get_gwp_values_df(
        sector, just_CO2=just_CO2, star=star, gwp20=gwp20
    ).values
    gwp_per_h2 = np.zeros_like(gwp_values)
    h2_need = sector_info_all[sector][1]
    for j, leak in enumerate(leak_rates[sector_info_all[sector][2]]):
        if isinstance(leak, (float, int)):
            tot_leak_loss = leak
        else:
            tot_leak_loss = leak["total"]
        h2_need_tot = (1 + tot_leak_loss) * h2_need
        gwp_per_h2[:, j] = gwp_values[:, j] / h2_need_tot
    gwp_per_h2_df = pd.DataFrame(
        gwp_per_h2,
        index=prod_methods[sector_info_all[sector][2]].keys(),
        columns=[
            make_column_names_from_leak_rate(leak_rate)
            for leak_rate in leak_rates[sector_info_all[sector][2]]
        ],
    )
    return gwp_per_h2_df


def get_benefit_loss_df(sector, just_CO2=False):
    """
    Get DataFrame of percentage benefit loss due to production or leak emissions

    Given a sector that is defined in sector_info_all of scenario_info
    the total GWP benefits of replacing current fossil fuel use in this
    sector with hydrogen for each of the scenario_info defined leak_rates
    and prod_methods, then the percentage benefit loss due to either production
    emissions or hydrogen leakage is calculate for each production method and
    leak rate

    Parameters
    ----------
    sector : str
        Name of sector. Should be one for which values are defined in sector_info_all
    just_CO2 : bool
        Whether to consider just direct CO2 emissions

    Returns
    -------
        pd.Dataframe
    """
    gwp_values = get_gwp_values_df(sector, just_CO2=just_CO2).values
    benefit_loss = np.array(
        [
            (gwp_values[:, i] - gwp_values[:, 0]) / gwp_values[:, 0] * 100
            for i in range(len(leak_rates[sector_info_all[sector][2]]))
        ]
    )
    benefit_loss_df = pd.DataFrame(
        benefit_loss,
        columns=prod_methods[sector_info_all[sector][2]].keys(),
        index=[
            make_column_names_from_leak_rate(leak_rate)
            for leak_rate in leak_rates[sector_info_all[sector][2]]
        ],
    )
    return benefit_loss_df
