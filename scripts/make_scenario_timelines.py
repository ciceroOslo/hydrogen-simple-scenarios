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

smooth_timeline_blue = CubicSpline(scenario_info.dnv_scenario_timeline[0], np.array(scenario_info.dnv_scenario_timeline[1])*100)
smooth_timeline_green = CubicSpline(scenario_info.dnv_scenario_timeline[0], np.array(scenario_info.dnv_scenario_timeline[2])*100)

years = range(2020,2051)
plt.stackplot(years, smooth_timeline_blue(years),smooth_timeline_green(years), labels = ["Fossil-based with CCS", "Renewable electrolysis"])
plt.xlabel("Year")
plt.ylabel("H2 produced (Tg/yr)")
plt.title("Hydrogen production DNV")
plt.tight_layout()
plt.legend()
plt.show()