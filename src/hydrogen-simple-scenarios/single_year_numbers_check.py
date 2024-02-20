import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

import get_emissions_functions, timeseries_functions

sectors = {
    "1A2a_Ind-Comb-Iron-steel": 1,
    "2A2_Lime-production": 0.4,
    "2C_Metal-production": 0.75,
}
# sector = '1A3di_International-shipping'
blue_opt = {"CO2": 1}  # kT CO2 per tonne Hydrogen
blue_pes = {"CO2": 3}
green = {"CO2": 0}

prod_methods = {
    "Blue_optimistic": blue_opt,
    "Blue_pessimistic": blue_pes,
    "Green": green,
}

# 1.8e tonnes steel per year
# 1 ton steel requires 50-60 kg H2
# (Bhaskar et al., 2020; Fischedick et al., 2014; Material Economics, 2019; Rechberger et al., 2020; Vogl et al., 2018) from steel report
# Carbon brief source lists 90 kg H2
# https://www.carboncommentary.com/blog/2020/11/4/how-much-hydrogen-will-be-needed-to-replace-coal-in-making-steel
h2_repl_need = 1.8e9 * 5e-5  # tonne* 50kg per tonne
print(h2_repl_need)
leak_rates = [0, 0.01, 0.05, 0.1]
# AGWP_CO2 =
df_repl = get_emissions_functions.get_sector_column_total(sectors)
gwp_values = np.zeros((len(prod_methods), len(leak_rates)))
for i, (prod, prod_emis) in enumerate(prod_methods.items()):
    print(prod)
    df_prod_now = df_repl.copy()
    df_prod_now = get_emissions_functions.add_prod_emissions(
        df_prod_now, h2_repl_need, prod_emis
    )
    for j, leak in enumerate(leak_rates):
        print(leak)
        df_with_leak = get_emissions_functions.add_leakage(
            df_prod_now, leak, h2_repl_need * (1 + leak)
        )

        gwp_values[i, j] = timeseries_functions.calc_GWP(df_with_leak, [0])
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
