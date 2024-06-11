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

from hydrogen_simple_scenarios import single_year_numbers_check, scenario_info

title_dict = {
    "steel": "Steel",
    "natural_gas": "Natural gas",
    "current_hydrogen": "H2 feedstock",
    "total": "Total energy"
}

def make_single_year_per_hydrogen_gwp_benefit_comparison(star = False, just_CO2 = False, gwp20=False):
    # Figure 1 (normal), S1 (just_CO2) or S2 (star):
    fig, axs = plt.subplots(ncols=len(scenario_info.sector_info), nrows=1, sharey=True, figsize=(16,8))
    #fig.suptitle("Per kg H2 CO2 equiv replacement benefit", fontsize=size)
    for i, sector in enumerate(scenario_info.sector_info):
        print(sector)
        gwp_benefits_per_h2 = single_year_numbers_check.get_gwp_values_per_hydrogen_used(sector, just_CO2= just_CO2, star= star, gwp20 =gwp20).reindex(["Green", "Blue_optimistic", "Blue_compliance"])
        gwp_benefits_per_h2 = gwp_benefits_per_h2.rename(columns = lambda x: f"{int(x*100)}%")
        print(gwp_benefits_per_h2)
        #gwp_benefits_per_h2_just_CO2 = single_year_numbers_check.get_gwp_values_per_hydrogen_used(sector, just_CO2=True)
        gwp_benefits_per_h2.plot.bar(ax = axs[i], alpha=0.8, legend = (i>=3))
        #gwp_benefits_per_h2_just_CO2.plot.bar(ax = axs[i], alpha=0.2, hatch=".")
        axs[i].tick_params(axis='x', labelrotation=45)
        axs[i].set_title(title_dict[sector], fontsize=size*0.9, fontweight = "bold")
        axs[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
        if star:
            secax = axs[i].secondary_yaxis('right', functions=(lambda x: x*0.4, lambda x: x/0.4))
    eqvi_str = ""
    if not just_CO2:
        eqvi_str = " equivalent"
    axs[0].set_ylabel(f"CO2{eqvi_str} benefit per unit H2")
    if star:
        secax.set_ylabel('Mitigated warming (mK per GT H2)')
    plt.tight_layout()
    fname_suffix = ""
    if star:
        fname_suffix = f"{fname_suffix}_gwpstar"
    if just_CO2:
        fname_suffix = f"{fname_suffix}_just_co2"
    if gwp20:
        fname_suffix = f"{fname_suffix}_gwp20"
    plt.savefig(f"per_h2_benefits{fname_suffix}.png")

# Making figures 1, S1 and S2:
make_single_year_per_hydrogen_gwp_benefit_comparison()
make_single_year_per_hydrogen_gwp_benefit_comparison(star=True)
make_single_year_per_hydrogen_gwp_benefit_comparison(just_CO2=True)
make_single_year_per_hydrogen_gwp_benefit_comparison(gwp20=True)

# Figure 2
fig, axs = plt.subplots(ncols=len(scenario_info.sector_info), nrows=1, sharey=True, figsize=(16,8))
for i, sector in enumerate(scenario_info.sector_info):
    benefit_loss = -1*single_year_numbers_check.get_benefit_loss_df(sector)
    benefit_loss.drop(benefit_loss.index[0], inplace=True)
    benefit_loss_to_plot = benefit_loss.T.reindex(["Green", "Blue_optimistic", "Blue_compliance"])
    
    print(benefit_loss_to_plot)
    benefit_loss_to_plot = benefit_loss_to_plot.rename(columns = lambda x: f"{int(x*100)}%")
    benefit_loss_to_plot.plot.bar(ax = axs[i], alpha=0.8, color = ["tab:orange",  "tab:green", "tab:red"], legend = (i>=3))
    axs[i].tick_params(axis='x', labelrotation=45)
    axs[i].set_title(title_dict[sector], fontsize=size*0.9, fontweight = "bold")
    axs[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
axs[0].set_ylabel("Percent loss of benefit from leak")
plt.tight_layout()
plt.savefig("benefits_loss.png")

annuual_natural_gas_2019_bcm = 4e3*0.85 #3976.2 billion cubic meters 2019 (Statista https://www.statista.com/statistics/265344/total-global-natural-gas-production-since-1998/)
#with 85-90% methane (Encyclopedia Britannica https://www.britannica.com/science/natural-gas/Composition-and-properties-of-natural-gas)
g_per_cubic_cm_methane = 0.0007168 #g per cubic centimeter
bcm_to_cubic_cms = 1.e9*1e6
annual_methane_per_year_Tg = annuual_natural_gas_2019_bcm*g_per_cubic_cm_methane*bcm_to_cubic_cms/1e12
ng_distr_emissions = 11.6583435344712 #CEDS Tg
ng_prod_emissions = 24.0092315386876 #CEDS Tg
print(f"Annual methane prod/use: {annual_methane_per_year_Tg }Tg, leaks in distribution: {ng_distr_emissions/annual_methane_per_year_Tg*100}% ")
print(f"Leaks in production: {ng_prod_emissions/annual_methane_per_year_Tg*100 }%, leaks total: {(ng_distr_emissions+ng_prod_emissions)/annual_methane_per_year_Tg*100}%")