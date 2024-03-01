import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

size=20
params = {'legend.fontsize': 'large',
          'axes.labelsize': size,
          'axes.titlesize': size,
          'xtick.labelsize': size*0.75,
          'ytick.labelsize': size*0.75}

plt.rcParams.update(params)

sys.path.append(os.path.join(os.path.dirname(__file__), "../", "src"))

from hydrogen_simple_scenarios import get_emissions_functions, scenario_info, ssp_data_extraction

data_path = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/SSP_CMIP6_201811.csv"

fig, axs = plt.subplots(nrows=1,ncols=2,squeeze=True,figsize=(18,10),sharey=False)

years = ssp_data_extraction.get_years(data_path) 
#Plot CO emissions:
for scen,colour in scenario_info.scens_colours.items():
    data_co = ssp_data_extraction.get_ts_component_sector_region_ssp(data_path, scen, "CO")
    axs[0].plot(years, data_co, color = colour, label = scenario_info.scens_reverse[scen])
    data_h2 = ssp_data_extraction.get_ts_component_sector_region_ssp(data_path, scen, "H2")
    axs[1].plot(years, data_h2, color = colour, label = scenario_info.scens_reverse[scen])

axs[0].set_ylabel('CO emissions [Tg CO/yr]')
for i, ax in enumerate(axs):
    ax.set_xlabel('Years')
    ax.set_ylim(bottom=0)
    axs[i].set_title(f"{chr(i+97)})", fontsize=20, loc='left')
axs[1].set_ylabel('H2 emissions [Tg H2/yr]')
axs[1].legend()

axs[0].set_title('CO emissions from SSP database')
axs[1].set_title('H2 emissions (scaled by CO)')
plt.suptitle('Anthropogenic and biomass burning emissions',fontsize=25)
plt.savefig("co_and_hydrogen_projections.png")
plt.clf()

data_path = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/SSP_IAM_V2_201811.csv"

fig, axs = plt.subplots(nrows=1,ncols=3,figsize=(22,8),sharey=False)
years = ssp_data_extraction.get_years(data_path)
print(years)
for values in ssp_data_extraction.get_unique_scenarios_and_models(data_path):
    data_energy, data_mass = ssp_data_extraction.get_ts_hydrogen_energy_and_mass(data_path, values[1], model=values[0])
    axs[0].plot(years, data_energy, color='lightgray')
    axs[1].plot(years, data_mass, color='lightgray')

for scen, colour in scenario_info.scens_colours.items():
    data_energy, data_mass = ssp_data_extraction.get_ts_hydrogen_energy_and_mass(data_path, scen)
    if not np.any(data_energy):
        continue
    axs[0].plot(years, data_energy, color = colour, label = scenario_info.scens_reverse[scen])
    axs[1].plot(years, data_mass, color = colour, label = scenario_info.scens_reverse[scen])
    axs[2].fill_between(years, data_mass*0.01, data_mass*0.1, color = colour, alpha = 0.2, label = scenario_info.scens_reverse[scen])
    axs[2].plot(years, data_mass*0.01, "--", color=colour)
    axs[2].plot(years, data_mass*0.1, "--", color=colour)

axs[0].set_ylabel('Energy Hydrogen [EJ/yr]')
axs[1].set_ylabel('Hydrogen [Tg/yr]')
axs[2].set_ylabel('Hydrogen leakages [Tg/yr]')
loc = mpl.ticker.MultipleLocator(base=2.0)
for i,ax in enumerate(axs):
    ax.set_xlabel('Years')
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=20)
    ax.xaxis.set_major_locator(loc)
    axs[i].set_title(f"{chr(i+97)})", fontsize=20, loc='left')

axs[0].set_title('Energy')
axs[1].set_title('Energy converted to mass')
axs[2].set_title('1-10% leakage rate')

plt.suptitle('Hydrogen Energy in SSP database',fontsize=25)
plt.savefig("hydrogen_energy_projectsions")
#plt.tight_layout()