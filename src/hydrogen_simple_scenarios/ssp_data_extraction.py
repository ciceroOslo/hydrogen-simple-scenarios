import pandas as pd
import numpy as np
import sys

from .scenario_info import scens_reverse, scen_reverse_model
from .get_emissions_functions import get_co_to_h2_factor_cmip6

co_ssp_sectors = ["Agricultural Waste Burning", "Aircraft", "Energy Sector", "Forest Burning", "Grassland Burning", "Industrial Sector", "International Shipping", "Peat Burning", "Residential Commercial Other", "Transportation Sector", "Waste"]

def get_data_for_component_sector_region_ssp(file, scen, comp, sector = "SUM", region="World", model="empty"):
    tot_data = pd.read_csv(file)
    sector_string = get_sector_string(comp, sector)
    if scen in scen_reverse_model:
        if "Energy" in sector:
            scen_q = scen_reverse_model[scen].split("_")[1]
        else:
            scen_q = scens_reverse[scen]
        model = scen_reverse_model[scen].split("_")[0]
    else:
        scen_q = scen    
    cut_data = tot_data.query(f"SCENARIO == '{scen_q}' and REGION == '{region}' and MODEL == '{model}'")
    cut_data = cut_data.query(f"VARIABLE =='{sector_string}'")
    return cut_data

def get_sector_string(comp, sector = "SUM"):
    if sector == "SUM":
        return f"CMIP6 Emissions|{comp}"
    elif "Energy" in sector:
        return f"{sector}|{comp}"
    else:
        return f"CMIP6 Emissions|{comp}|{sector}"

def get_ts_component_sector_region_ssp(file, scen, comp, sector = "SUM", region = "World", model = "empty"):
    if comp != "H2":
        read_data = get_data_for_component_sector_region_ssp(file, scen, comp, sector = sector, region=region, model=model)
        if read_data.shape[0] == 0:
            return np.zeros(read_data.shape[1]-5)
        return read_data.iloc[0, 5:].to_numpy(dtype=float)
    if sector != "SUM":
        return get_data_for_component_sector_region_ssp(file, scen, "CO", sector = sector, region=region).iloc[0, 5:].to_numpy(dtype=float) * get_co_to_h2_factor_cmip6(sector)
    timeseries = np.zeros(10)
    for sector in co_ssp_sectors:
        co_df = get_data_for_component_sector_region_ssp(file, scen, "CO", sector = sector, region=region) 
        if co_df.shape[0] == 0:
            continue
        timeseries = timeseries + co_df.iloc[0, 5:].to_numpy(dtype=float)*get_co_to_h2_factor_cmip6(sector)
    return timeseries

def get_ts_hydrogen_energy_and_mass(file, scen, region="World", model="empty"):
    energy_ts = get_ts_component_sector_region_ssp(file, scen, comp="Hydrogen", sector="Secondary Energy", region=region, model = model)
    
    #Convert to hydrogen mass: 
    # EJ -> KWh : 277777777777.78 
    # kWH-> kg H2 : 1 kg H2 = 33.3 kWh (Warwick)
    # kg H2 -> Tg H2: 1e-9
    conv_factor = 277777777777.78/33.3*1e-9
    mass_ts = energy_ts*conv_factor
    return energy_ts, mass_ts

def get_years(file):
    years = pd.read_csv(file).columns[5:]
    return years

def get_unique_scenarios_and_models(file):
    lists = pd.read_csv(file)[['MODEL', 'SCENARIO']].drop_duplicates()
    return lists.to_numpy()

