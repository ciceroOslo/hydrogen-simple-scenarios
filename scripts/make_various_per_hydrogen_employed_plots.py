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

df_repl_steel = get_emissions_functions.get_sector_column_total(scenario_info.sector_info["steel"][0])
print(df_repl_steel)

df_repl_ng = get_emissions_functions.get_sector_column_total(scenario_info.sector_info["natural_gas"][0], type_split="fuel")
print(df_repl_ng)
df_repl_currh2 = get_emissions_functions.get_sector_column_total(scenario_info.sector_info["current_hydrogen"][0], type_split="fuel")
print(df_repl_currh2)

title_dict = {
    "steel": "Steel",
    "natural_gas": "Natural gas",
    "current_hydrogen": "H2 feedstock",
    "total": "Total"
}

fig, axs = plt.subplots(ncols=len(scenario_info.sector_info), nrows=1, sharey=True, figsize=(16,8))
fig.suptitle("Per kg H2 CO2 equiv replacement benefit", fontsize=size)
for i, sector in enumerate(scenario_info.sector_info):
    print(sector)
    gwp_benefits_per_h2 = single_year_numbers_check.get_gwp_values_per_hydrogen_used(sector)
    gwp_benefits_per_h2.plot.bar(ax = axs[i], alpha=0.8)
    axs[i].tick_params(axis='x', labelrotation=45)
    axs[i].set_title(title_dict[sector], fontsize=size*0.9, fontweight = "bold")
    axs[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
axs[0].set_ylabel("CO2 equivalent benefit per kg H2")
plt.tight_layout()
plt.savefig("per_h2_benefits.png")

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
df_concat = pd.concat([df_repl_steel, df_repl_ng, df_repl_currh2])


df_concat.index = ["Steel", "Natural gas", "Feedstock"]
print(df_concat)
print("Concatenated")

sys.exit(4)


gwp_benefits = single_year_numbers_check.get_gwp_values_df("steel")
benefit_loss = single_year_numbers_check.get_benefit_loss_df("steel")
gwp_benefits_per_h2 = single_year_numbers_check.get_gwp_values_per_hydrogen_used("steel")

gwp_benefits_ng = single_year_numbers_check.get_gwp_values_df("natural_gas")
benefit_loss_ng = single_year_numbers_check.get_benefit_loss_df("natural_gas")
gwp_benefits_per_h2_ng = single_year_numbers_check.get_gwp_values_per_hydrogen_used("natural_gas")

gwp_benefits_ind = single_year_numbers_check.get_gwp_values_df("current_hydrogen")
benefit_loss_ind = single_year_numbers_check.get_benefit_loss_df("current_hydrogen")
gwp_benefits_per_h2_ind = single_year_numbers_check.get_gwp_values_per_hydrogen_used("current_hydrogen")

print("--- Steel ---")
print(gwp_benefits)
print("--- Natural Gas ---")
print(gwp_benefits_ng)
print("--- Industry ---")
print(gwp_benefits_ind)
print("--- Steel ---")
print(benefit_loss)
print("--- Natural Gas ---")
print(benefit_loss_ng)
print("--- Industry ---")
print(benefit_loss_ind)
print("--- Steel ---")
print(gwp_benefits_per_h2)
print("--- Natural gas ---")
print(gwp_benefits_per_h2_ng)
print("--- Industry ---")
print(gwp_benefits_per_h2_ind)

print(scenario_info.sector_info)
print(scenario_info.h2_energy_to_mass_conv_factor )

fig, axs = plt.subplots(ncols=4, nrows=1, sharey=True)
fig.suptitle("Per kg H2 CO2 equiv replacement benefit")
gwp_benefits_per_h2.plot.bar(ax = axs[0], alpha=0.8)
gwp_benefits_per_h2_ind.plot.bar(ax = axs[2], alpha=0.8)
gwp_benefits_per_h2_ng.plot.bar(ax = axs[1], alpha=0.8)
axs[0].set_ylabel("CO2 equivalent benefit per kg H2")
axs[0].set_title("Steel")
axs[2].set_title("H2 feedstock")
axs[1].set_title("Natural gas")
for i in range(3):
    axs[i].tick_params(axis='x', labelrotation=45)
plt.tight_layout()
plt.savefig("per_h2_benefits.png")

fig, axs = plt.subplots(ncols=4, nrows=1, sharey=True)
benefit_loss.T.plot.bar(ax = axs[0], alpha=0.8)
benefit_loss_ind.T.plot.bar(ax = axs[2], alpha=0.8)
benefit_loss_ng.T.plot.bar(ax = axs[1], alpha=0.8)
axs[0].set_ylabel("Percent ")
axs[0].set_title("Steel")
axs[2].set_title("H2 feedstock")
axs[1].set_title("Natural gas")
for i in range(3):
    axs[i].tick_params(axis='x', labelrotation=45)
plt.tight_layout()
plt.savefig("benefits_loss.png")