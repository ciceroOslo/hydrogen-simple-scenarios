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

from hydrogen_simple_scenarios import get_emissions_functions, timeseries_functions, single_year_numbers_check, scenario_info

title_dict = {
    "steel": "Steel",
    "natural_gas": "Natural gas",
    "current_hydrogen": "H2 feedstock",
    "total": "Total"
}

# Figure 1:
fig, axs = plt.subplots(ncols=len(scenario_info.sector_info), nrows=1, sharey=True, figsize=(16,8))
fig.suptitle("Per kg H2 CO2 equiv replacement benefit", fontsize=size)
for i, sector in enumerate(scenario_info.sector_info):
    print(sector)
    gwp_benefits_per_h2 = single_year_numbers_check.get_gwp_values_per_hydrogen_used(sector)
    gwp_benefits_per_h2_just_CO2 = single_year_numbers_check.get_gwp_values_per_hydrogen_used(sector, just_CO2=True)
    gwp_benefits_per_h2.plot.bar(ax = axs[i], alpha=0.8)
    gwp_benefits_per_h2_just_CO2.plot.bar(ax = axs[i], alpha=0.2, hatch=".")
    axs[i].tick_params(axis='x', labelrotation=45)
    axs[i].set_title(title_dict[sector], fontsize=size*0.9, fontweight = "bold")
    axs[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
axs[0].set_ylabel("CO2 equivalent benefit per unit H2")
plt.tight_layout()
plt.savefig("per_h2_benefits.png")

# Figure S1
fig, axs = plt.subplots(ncols=len(scenario_info.sector_info), nrows=1, sharey=True, figsize=(16,8))
fig.suptitle("Per kg H2 CO2 equiv replacement benefit (GWP*)", fontsize=size)
for i, sector in enumerate(scenario_info.sector_info):
    print(sector)
    gwp_benefits_per_h2 = single_year_numbers_check.get_gwp_values_per_hydrogen_used(sector, star=True)
    gwp_benefits_per_h2.plot.bar(ax = axs[i], alpha=0.8)
    axs[i].tick_params(axis='x', labelrotation=45)
    axs[i].set_title(title_dict[sector], fontsize=size*0.9, fontweight = "bold")
    axs[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
    secax = axs[i].secondary_yaxis('right', functions=(lambda x: x*0.4, lambda x: x/0.4))
secax.set_ylabel('Mitigated warming (mK per GT H2)')
axs[0].set_ylabel("CO2 equivalent benefit per unit H2")
plt.tight_layout()
plt.savefig("per_h2_benefits_gwp_star.png")

# Figure 2
fig, axs = plt.subplots(ncols=len(scenario_info.sector_info), nrows=1, sharey=True, figsize=(16,8))
fig.suptitle("Percent loss of benefit from leak", fontsize=size)
for i, sector in enumerate(scenario_info.sector_info):
    benefit_loss = -1*single_year_numbers_check.get_benefit_loss_df(sector)
    benefit_loss.T.plot.bar(ax = axs[i], alpha=0.8)
    axs[i].tick_params(axis='x', labelrotation=45)
    axs[i].set_title(title_dict[sector], fontsize=size*0.9, fontweight = "bold")
    axs[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
axs[0].set_ylabel("Percent")
plt.tight_layout()
plt.savefig("benefits_loss.png")