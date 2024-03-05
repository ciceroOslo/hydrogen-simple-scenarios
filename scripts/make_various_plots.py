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

def plot_co_emissions_and_scaled_hydrogen():

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

datapath_simpleh2 = os.path.join(os.path.dirname("__file__"), "..", "..", "simpleH2", "input")
def make_nox_co_ratio_and_ch4_plot(scenarios):
    fig, axs = plt.subplots(nrows=1,ncols=2,squeeze=True,figsize=(18,10),sharey=False)
    for scen, colour in scenario_info.scens_colours.items():
        if scen not in scenarios:
            continue
        data_co = pd.read_csv(os.path.join(datapath_simpleh2, f"co_emis_noburn_{scen}.csv"))
        data_nox = pd.read_csv(os.path.join(datapath_simpleh2, f"nox_emis_noburn_{scen}.csv"))
        data_ch4 = pd.read_csv(os.path.join(datapath_simpleh2, f"ch4_conc_{scen}.csv"))
        axs[0].plot(data_ch4["Years"].to_numpy(), data_ch4["Emis"].to_numpy(), color=colour, label = scenario_info.scens_reverse[scen])
        axs[1].plot(data_co["Years"].to_numpy(), data_nox["Emis"].to_numpy()/data_co["Emis"].to_numpy(), color=colour, label = scenario_info.scens_reverse[scen])
    
    for i,ax in enumerate(axs):
        ax.set_xlabel('Years')
        ax.set_xlim(left=1970, right=2050)
        #ax.set_ylim(bottom=0)
        ax.legend(fontsize=20)
        #ax.xaxis.set_major_locator(loc)
        axs[i].set_title(f"{chr(i+97)})", fontsize=20, loc='left')
    axs[0].set_ylabel("Methane concentration [ppb]")
    axs[1].set_ylabel("NOx/CO")
    axs[0].set_title('Methane concentration', fontweight="bold")
    axs[1].set_title('NOx/CO emissions', fontweight="bold")
    plt.savefig("methane_and_nox_co_scenarios.png")

data_path_iam = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/SSP_IAM_V2_201811.csv"
def make_hydrogen_energy_plot(): 

    fig, axs = plt.subplots(nrows=1,ncols=3,figsize=(22,8),sharey=False)
    years = ssp_data_extraction.get_years(data_path)
    print(years)
    for values in ssp_data_extraction.get_unique_scenarios_and_models(data_path_iam):
        data_energy, data_mass = ssp_data_extraction.get_ts_hydrogen_energy_and_mass(data_path_iam, values[1], model=values[0])
        axs[0].plot(years, data_energy, color='lightgray')
        axs[1].plot(years, data_mass, color='lightgray')

    for scen, colour in scenario_info.scens_colours.items():
        data_energy, data_mass = ssp_data_extraction.get_ts_hydrogen_energy_and_mass(data_path_iam, scen)
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

##cenarios = ["ssp119", "ssp434", "ssp585"]
make_hydrogen_energy_plot()
#make_nox_co_ratio_and_ch4_plot(scenarios)