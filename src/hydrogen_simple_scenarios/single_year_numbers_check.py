import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from .get_emissions_functions import get_sector_column_total, add_leakage, add_prod_emissions

from .timeseries_functions import calc_GWP 
from .scenario_info import prod_methods, leak_rates, sector_info


def get_gwp_values_df(sector):
    """
    Get DataFrame of gwp values for total sector replacement

    Given a sector that is defined in sector_info of scenario_info
    the total GWP benefits of replacing current fossil fuel use in this
    sector with hydrogen for each of the scenario_info defined leak_rates
    and prod_methods

    Parameters
    ----------
    sector : str
        Name of sector. Should be one for which values are defined in sector_info
    Returns
    -------
        pd.Dataframe
    """
    df_repl = get_sector_column_total(sector_info[sector][0], type_split=sector_info[sector][2])
    gwp_values = np.zeros((len(prod_methods), len(leak_rates)))
    for i, (prod, prod_emis) in enumerate(prod_methods.items()):
        print(prod)
        df_prod_now = df_repl.copy()
        df_prod_now = add_prod_emissions(
            df_prod_now, sector_info[sector][1], prod_emis
        )
        for j, leak in enumerate(leak_rates):
            print(leak)
            df_with_leak = add_leakage(
                df_prod_now, leak, sector_info[sector][1] * (1 + leak)
            )

            gwp_values[i, j] = calc_GWP(df_with_leak, [0])
    gwp_df = pd.DataFrame(gwp_values, index=prod_methods.keys(), columns=leak_rates)
    return gwp_df

def get_gwp_values_per_hydrogen_used(sector):
    """
    Get DataFrame of gwp replacement per Tg H2 employed

    Given a sector that is defined in sector_info of scenario_info
    the per Tg hydrogen benefit of replacing current fossil fuel use in this
    sector with hydrogen for each of the scenario_info defined leak_rates
    and prod_methods

    Parameters
    ----------
    sector : str
        Name of sector. Should be one for which values are defined in sector_info

    Returns
    -------
        pd.Dataframe
    """
    gwp_values = get_gwp_values_df(sector).values
    gwp_per_h2 = np.zeros_like(gwp_values)
    h2_need = sector_info[sector][1]
    for j, leak in enumerate(leak_rates):
        h2_need_tot =  (1+leak)*h2_need 
        gwp_per_h2[:, j] = gwp_values[:,j]/h2_need_tot
    gwp_per_h2_df = pd.DataFrame(gwp_per_h2, index=prod_methods.keys(), columns=leak_rates)
    return gwp_per_h2_df

def get_benefit_loss_df(sector):
    """
    Get DataFrame of percentage benefit loss due to production or leak emissions

    Given a sector that is defined in sector_info of scenario_info
    the total GWP benefits of replacing current fossil fuel use in this
    sector with hydrogen for each of the scenario_info defined leak_rates
    and prod_methods, then the percentage benefit loss due to either production
    emissions or hydrogen leakage is calculate for each production method and 
    leak rate

    Parameters
    ----------
    sector : str
        Name of sector. Should be one for which values are defined in sector_info

    Returns
    -------
        pd.Dataframe
    """
    gwp_values = get_gwp_values_df(sector).values
    benefit_loss = np.array(
        [
            (gwp_values[:, i] - gwp_values[:, 0]) / gwp_values[:, 0] * 100
            for i in range(len(leak_rates))
        ]
    )
    benefit_loss_df = pd.DataFrame(
        benefit_loss, columns=prod_methods.keys(), index=leak_rates
    )
    return benefit_loss_df
