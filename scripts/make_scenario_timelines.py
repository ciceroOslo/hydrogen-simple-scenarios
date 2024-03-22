import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
from scipy.interpolate import CubicSpline

size=22
params = {'legend.fontsize': 'large',
          'axes.labelsize': size,
          'axes.titlesize': size,
          'xtick.labelsize': size*0.75,
          'ytick.labelsize': size*0.75}

plt.rcParams.update(params)

sys.path.append(os.path.join(os.path.dirname(__file__), "../", "src"))

from hydrogen_simple_scenarios import get_emissions_functions, timeseries_functions, single_year_numbers_check, scenario_info

years = range(2020,2051)
smooth_timeline_blue = CubicSpline(scenario_info.dnv_scenario_timeline[0], np.array(scenario_info.dnv_scenario_timeline[1])*100)
smooth_timeline_green = CubicSpline(scenario_info.dnv_scenario_timeline[0], np.array(scenario_info.dnv_scenario_timeline[2])*100)

blue_hydrogen_timeline = smooth_timeline_blue(years)
green_hydrogen_timeline = smooth_timeline_green(years)
print(years)
print(blue_hydrogen_timeline)
print(green_hydrogen_timeline)

# Make table S2
df_to_make_dnv_table = pd.DataFrame(data = {"Blue H2 (Tg/yr)": blue_hydrogen_timeline, "Green H2 (Tg/yr)": green_hydrogen_timeline}, index = years)
df_to_make_dnv_table.to_csv("dnv_approximation_composition.csv", float_format='%.2f')


leak_rates = [0, 0.1]#, 0.01, 0.05, 0.1]

fig1, axs1 = plt.subplots(ncols=len(leak_rates)+1, nrows=1, sharey=True, figsize=(16,8))
fig1.suptitle("Hydrogen production and use breakdown", fontsize=size)
axs1[0].stackplot(years, blue_hydrogen_timeline,green_hydrogen_timeline, labels = ["Fossil-based with CCS", "Renewable electrolysis"])
axs1[0].set_ylabel("H2 produced (Tg/yr)")
axs1[0].set_title("DNV production", fontsize=size*0.9, fontweight = "bold")

fig2, axs2 = plt.subplots(ncols=len(leak_rates), nrows=1, sharey=True, figsize=(16,8))
fig2.suptitle("Mitigated carbon and warming", fontsize=size)

fig3, axs3 = plt.subplots(ncols=len(leak_rates), nrows=1, sharey=True, figsize=(16,8))
fig3.suptitle("Mitigated carbon and warming - just CO2", fontsize=size)

feedstock_total_TG = scenario_info.sector_info["current_hydrogen"][1]/1e3
steel_total_TG = scenario_info.sector_info["steel"][1]/1e3
ng_total_TG = scenario_info.sector_info["natural_gas"][1]/1e3
bg_total_TG = scenario_info.sector_info["total"][1]/1e3

sectors_list = [
    "Feedstock from blue", 
    "Natural gas", 
    "Feedstock from green", 
    "Steel", 
    "Generic energy"
]
sectors = {"Feedstock from blue": [
            get_emissions_functions.get_sector_column_total(scenario_info.sector_info["current_hydrogen"][0]), 
            feedstock_total_TG,
            scenario_info.blue_pes
            ], 
            "Natural gas": [
                get_emissions_functions.get_sector_column_total(scenario_info.sector_info["natural_gas"][0]),
                ng_total_TG,
                scenario_info.blue_pes
            ],
            "Feedstock from green": [
                  get_emissions_functions.get_sector_column_total(scenario_info.sector_info["current_hydrogen"][0]),
                  feedstock_total_TG,
                  scenario_info.green
            ],
            "Steel": [
                  get_emissions_functions.get_sector_column_total(scenario_info.sector_info["steel"][0]),
                  steel_total_TG,
                  scenario_info.green
            ],
                  
            "Generic energy": [
                get_emissions_functions.get_sector_column_total(scenario_info.sector_info["total"][0]),
                bg_total_TG,
                scenario_info.green
            ]
              }


for j, leak_rate in enumerate(leak_rates): 
    blue_avail = timeseries_functions.get_hydrogen_available(blue_hydrogen_timeline, leak_rate)
    green_avail = timeseries_functions.get_hydrogen_available(green_hydrogen_timeline, leak_rate)
    ts_feedstock_blue = np.zeros(len(years))
    ts_feedstock_green = np.zeros(len(years))
    ts_ng = np.zeros(len(years))
    ts_steel = np.zeros(len(years))
    ts_bg_energy = np.zeros(len(years))
    for i,year in enumerate(years):
        # First 50% of both blue and green go to saturating feedstock
        ts_feedstock_blue[i] = min(0.5 * blue_avail[i]/feedstock_total_TG, 0.5)
        ts_feedstock_green[i] = min(1-ts_feedstock_blue[i], 0.5 * green_avail[i]/feedstock_total_TG)
        # Rest of green to saturation of steel
        ts_steel[i] = min((green_avail[i] - ts_feedstock_green[i]*feedstock_total_TG)/steel_total_TG, 1) 
        # Rest of blue to saturation of natural gas
        ts_ng[i] = min((blue_avail[i] - ts_feedstock_blue[i]*feedstock_total_TG)/ng_total_TG, 1)
        # Whatever remains follows general background energy sector
        ts_bg_energy[i] = (
            (green_avail[i] - 
                ts_feedstock_green[i]*feedstock_total_TG - 
                ts_steel[i]*steel_total_TG)/bg_total_TG +
            (blue_avail[i] - 
                ts_feedstock_blue[i]*feedstock_total_TG - 
                ts_ng[i]*ng_total_TG)/bg_total_TG)
    axs1[j+1].stackplot(years, 
                     ts_feedstock_blue*feedstock_total_TG, 
                     ts_ng*ng_total_TG, 
                     ts_feedstock_green*feedstock_total_TG, 
                     ts_steel*steel_total_TG,
                     ts_bg_energy*bg_total_TG,
                     labels=sectors_list
                     )
    axs1[j+1].set_title(f"Leak rate {int(leak_rate*100)}%", fontsize=size*0.9, fontweight = "bold")

    # Now for the timeseries of GWP(*) and mitigated warming
    ts_list = [ts_feedstock_blue, 
               ts_ng, 
               ts_feedstock_green, 
               ts_steel, 
               ts_bg_energy]
    gwp_starish = np.zeros((len(ts_list), len(years)))
    gwp_just_co2 = np.zeros((len(ts_list), len(years)))
    for i, ts in enumerate(ts_list):
        emissions_ts = timeseries_functions.make_emission_ts(sectors[sectors_list[i]][0], ts, years)
        #print(emissions_ts)
        if leak_rate > 0:
            emissions_ts = timeseries_functions.add_leakage_ts(sectors[sectors_list[i]][0], ts, years, leak_rate, sectors[sectors_list[i]][1]*1e3)
        #print(emissions_ts)
        emissions_ts = timeseries_functions.add_prod_emissions_ts(emissions_ts, sectors[sectors_list[i]][1]*1e3, sectors[sectors_list[i]][2], years, ts)
        #print(emissions_ts)
        #sys.exit(4)
        gwp_starish[i,:], gwp_just_co2[i,:] = timeseries_functions.calc_GWP_star(emissions_ts, years) 
    axs2[j].stackplot(years, gwp_starish/1e6, labels = sectors_list)
    axs3[j].stackplot(years, gwp_just_co2/1e6, labels = sectors_list)
    #print(gwp_just_co2)
    #sys.exit(4)
    #axs2[j].stackplot(years, gwp_just_co2, alpha = 0.2)
    axs2[j].set_title(f"Leak rate {int(leak_rate*100)}%", fontsize=size*0.9, fontweight = "bold")
    secax2 = axs2[j].secondary_yaxis('right', functions=(lambda x: x*0.4, lambda x: x/0.4))
    axs3[j].set_title(f"Leak rate {int(leak_rate*100)}%", fontsize=size*0.9, fontweight = "bold")
    secax3 = axs3[j].secondary_yaxis('right', functions=(lambda x: x*0.4, lambda x: x/0.4))
secax2.set_ylabel('Mitigated warming (mK)')
secax3.set_ylabel('Mitigated warming (mK)')
for i in range(len(axs1)):
    axs1[i].legend(loc='center left')
    axs1[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
    axs1[i].set_xlabel("Year")
axs1[1].set_ylabel("H2 used (Tg/yr)")

for i in range(len(axs2)):
    axs2[i].legend(loc='center left')
    axs2[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
    axs2[i].set_xlabel("Year")
axs2[0].set_ylabel("Mitigated CO2 equivalents (GT CO2)")

for i in range(len(axs3)):
    axs3[i].legend(loc='center left')
    axs3[i].set_title(f"{chr(i+97)})", fontsize=size*0.75, loc='left')
    axs3[i].set_xlabel("Year")
axs3[0].set_ylabel("Mitigated CO2 (GT CO2)")
#plt.show()
fig1.savefig("dnv_scenario_approximation_and_use.png")
fig2.savefig("hydrogen_replacement_benefit.png")
fig3.savefig("hydrogen_replacement_benefit_justCO2.png")