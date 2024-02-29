import pandas as pd
import numpy as np
import sys

from .scenario_info import scens_reverse

co_ssp_sectors = ["Agricultural Waste Burning", "Energy Sector", "Forest Burning", "Grassland Burning", "Industrial Sector", "Residential Commercial Other", "Transportation Sector", "Waste"]

def get_data_for_component_sector_region_ssp(file, scen, comp, sector = "SUM", region="World"):
    tot_data = pd.read_csv(file)
    scen_q = scens_reverse[scen]
    sector_string = get_sector_string(comp, sector)
    cut_data = tot_data.query(f"SCENARIO == '{scen_q}' and REGION == '{region}'")
    cut_data = cut_data.query(f"VARIABLE =='{sector_string}'")

    return cut_data

def get_sector_string(comp, sector = "SUM"):
    if sector == "SUM":
        return f"CMIP6 Emissions|{comp}"
    else:
        return f"CMIP6 Emissions|{comp}|{sector}"
