import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os

size=22
params = {'legend.fontsize': 'large',
          'axes.labelsize': size,
          'axes.titlesize': size,
          'xtick.labelsize': size*0.75,
          'ytick.labelsize': size*0.75}

plt.rcParams.update(params)

sys.path.append(os.path.join(os.path.dirname(__file__), "../", "src"))

from hydrogen_simple_scenarios import get_emissions_functions, single_year_numbers_check, scenario_info
indices = list(get_emissions_functions.complist)
indices.append("H2 total need")
indices.append("GWP potential")
empty_to_fill_in = pd.DataFrame(0, index = indices, columns = scenario_info.sector_info.keys())
print(empty_to_fill_in)
for i, sector in enumerate(scenario_info.sector_info):
    print(sector)
    df_repl = get_emissions_functions.get_sector_column_total(scenario_info.sector_info[sector][0], type_split=scenario_info.sector_info[sector][2])
    print(df_repl)
    empty_to_fill_in.loc[:"NOx", sector] = df_repl.loc['Total',:].values/1e3
    empty_to_fill_in.loc["H2 total need", sector] = scenario_info.sector_info[sector][1]/1e3
    gwp_values = single_year_numbers_check.get_gwp_values_df(sector)
    empty_to_fill_in.loc["GWP potential", sector] = gwp_values.iloc[-1,0]/1e3
    print(gwp_values)
empty_to_fill_in.to_csv("Table_1.csv")

title_dict = {
    "steel": "Steel",
    "natural_gas": "Natural gas",
    "current_hydrogen": "H2 feedstock",
    "total": "Total"
}