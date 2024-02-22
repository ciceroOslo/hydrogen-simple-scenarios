import pandas as pd
import numpy as np

from .scenario_info import scens_reverse

def get_data_for_component_sector_region_ssp(file, scen, comp, sector = "SUM", region="World"):
    tot_data = pd.read_csv(file)
    scen_q = scens_reverse[scen]
    print(scen_q)
    print(tot_data['VARIABLE'].head(20))
    print(tot_data.columns)
    cut_data = tot_data.query(f"SCENARIO == '{scen_q}' and REGION == '{region}'")
    print(cut_data.shape)
    print(cut_data['VARIABLE'])

def get_sector_string(comp, sector = "SUM"):
    if sector == "SUM":
        return f"CMIP6 Emissions|{comp}"
    else:
        return f"CMIP6 Emissions|{sector}"
