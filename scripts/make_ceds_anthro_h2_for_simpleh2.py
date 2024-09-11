import numpy as np
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../", "src"))

from hydrogen_simple_scenarios import get_emissions_functions

species = ["H2"]
ceds_version = "ceds21"
endyear = 2019
years = range(1750, endyear + 1)

for comp in species:
    data = np.zeros(len(years))
    for i, year in enumerate(years):
        data[i] = get_emissions_functions.get_sector_column_single_comp(
            comp, "Total", ignore_bb=True, year=year, file_suffix="_2021_04_21.csv"
        )
    arr_out = np.array([years, data / 1e3])
    print(arr_out)
    np.savetxt(
        f"{comp.lower()}_anthro_{ceds_version}.csv",
        arr_out.T,
        fmt=["%d", "%6.8f"],
        delimiter=",",
    )
