import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from .get_emissions_functions import get_sector_column_total, add_leakage, add_prod_emissions

from .timeseries_functions import calc_GWP 
from .scenario_info import prod_methods, leak_rates, sector_info

def get_benefit_loss_df(sector):

    df_repl = get_sector_column_total(sector_info[sector][0])
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
    print(gwp_values)
    gwp_df = pd.DataFrame(gwp_values, index=prod_methods.keys(), columns=leak_rates)
    print(gwp_df)
    benefit_loss = np.array(
        [
            (gwp_values[:, i] - gwp_values[:, 0]) / gwp_values[:, 0] * 100
            for i in range(len(leak_rates))
        ]
    )
    print(benefit_loss)
    benefit_loss_df = pd.DataFrame(
        benefit_loss, columns=prod_methods.keys(), index=leak_rates
    )
    print(benefit_loss_df)
    return benefit_loss_df
