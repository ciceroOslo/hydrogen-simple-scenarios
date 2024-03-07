import pandas as pd
import matplotlib.pyplot as plt

import sys

#filepath = "/div/pdo/emissions/CEDS0521/TOTALS/"
filepath = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/"

# GWP_dict = {"H2": 11.6, "CO2": 1, "CO": 2.3, "CH4":27.9,  "NMVOC": 10.9, "NOx": -(42+56)/2}
GWP_dict = {"H2": 11.6, "CO2": 1, "CO": 2.3, "CH4": 27.9, "NMVOC": 10.9, "NOx": 0}
# H2: Sand et al 2023, CO, NMVOC and NOx global summer/winter average from Aamaas 2016, CH4 AR6
complist = GWP_dict.keys()

# AGWP_CO2 =

class COToHydrogenEmissionsConverter:

    # From supplementary of Paulot et al 2021
    # i n t e rna t i onal journal o f hydrogen energy 4 6 ( 2 0 2 1 ) 1 3 4 4 6e1 3 4 6 0
    co_h2_factors = {
        "Agr_transp": 0.0357,
        "Energy_ind": 0.0143,
        "Residential": 0.0217,
        "Waste": 0.005,
    }

    # From Atmos. Chem. Phys., 11, 4039–4072, 2011
    # www.atmos-chem-phys.net/11/4039/2011/
    # doi:10.5194/acp-11-4039-2011
    co_g_per_kg_dry_mass = {
        "Tropical Forest": 93,
        "Savanna": 63,
        "Agricultural Waste Burning": 102, # Crop residue
        "Pasture Maintenance": 135,
        "Boreal Forest": 127,
        "Temperate Forest": 89,
        "Extratropical Forest": 122,
        "Peat Burning": 182,
        "Chaparral": 67, # Californian shrublike ecosystem 
        "Open Cooking": 77,
        "Patsari Stoves": 42, # Particular stove type for wood
        "Charcoal Making": 255,
        "Charcoal Burning": 189, 
        "Dung Burning": 105,
        "Garbage Burning": 38,
    } 

    h2_g_per_kg_dry_matter_burnt ={
        "Tropical Forest": 3.36,
        "Savanna": 1.7,
        "Agricultural Waste Burning": 2.59, # Crop residue
        "Boreal Forest": 2.03, # Assumed equal to temperate
        "Temperate Forest": 2.03,
        "Extratropical Forest": 2.03,
        "Peat Burning": 1.2, # From Andreae according to Paulot
        "Garbage Burning": 0.091,
    }

    def __init__(self, just_CO2 = False, ignore_bb = False):

        self.just_CO2 = just_CO2
        self.ignore_bb = ignore_bb

    def get_co_to_h2_factor_burning_cmip6(self, sector):
        if self.just_CO2:
            return 0
        if self.ignore_bb:
            return 0
        if sector in self.h2_g_per_kg_dry_matter_burnt.keys():
            sector_here = sector
        elif sector == "Grassland Burning":
            sector_here = "Savanna"
        elif sector == "Forest Burning":
            sector_here = "Extratropical Forest"
        else:
            print(f"Why am I here with {sector}")
            sector_here = "Garbage Burning"
        return self.h2_g_per_kg_dry_matter_burnt[sector_here]/ self.co_g_per_kg_dry_mass[sector_here]


    def get_co_to_h2_factor(self, sector):
        if self.just_CO2:
            return 0
        if sector[0] == "5":
            return self.co_h2_factors["Waste"]
        if sector[0] == "3":
            return self.co_h2_factors["Agr_transp"]
        if sector[:3] == "1A3":
            return self.co_h2_factors["Agr_transp"]
        if sector[:4] == "1A4b":
            return self.co_h2_factors["Residential"]
        if sector[:4] == "1A4c":
            return self.co_h2_factors["Agr_transp"]
        return self.co_h2_factors["Energy_ind"]

    def get_co_to_h2_factor_cmip6(self, sector):
        if self.just_CO2:
            return 0
        if "Burning" in sector:
            return self.get_co_to_h2_factor_burning_cmip6(sector)
        if sector in self.co_h2_factors.keys():
            return self.co_h2_factors[sector]
        if "Energy" in sector or "Industrial" in sector:
            return self.co_h2_factors["Energy_ind"]
        if "Residential" in sector:
            return self.co_h2_factors["Residential"]
        return self.co_h2_factors["Agr_transp"]


def prepare_emis_df(comp, split_type, yr=2019):
    filename = comp + "_global_CEDS_emissions_by_" + split_type + "_2021_04_21.csv"
    if split_type == "sector":
        data_emis = pd.read_csv(
            filepath + filename, delimiter=",", index_col=1, header=0, skiprows=0
        ).T
    else:
        data_emis = pd.read_csv(
            filepath + filename, delimiter=",", index_col=0, header=0, skiprows=0
        ).T
    # print(data_emis)
    # print(data_emis.index)
    data_emis = data_emis.drop(["em", "units"])

    data_emis.index.name = "Year"
    index = data_emis.index.values
    for i, year in enumerate(index):
        index[i] = year.split("X")[-1]
    data_emis.index = index.astype(int)
    data_emis_yr = data_emis.loc[2019]
    data_emis_yr.name = comp
    # print(data_emis_yr)
    return data_emis_yr


def get_sector_column(sector, type_split="sector", just_CO2 = False, ignore_bb = False):
    df_replacements = pd.DataFrame(0.0, columns=complist, index=[sector])
    converter = COToHydrogenEmissionsConverter(just_CO2 = just_CO2, ignore_bb = ignore_bb)
    for comp in complist:
        if comp == "H2":
            data_emis = prepare_emis_df("CO", type_split, yr=2019)

        else:
            data_emis = prepare_emis_df(comp, type_split, yr=2019)
        if sector == "Total":
            if comp == "H2":
                
                for sub_sector in data_emis.index:
                    df_replacements[comp][sector] = df_replacements[comp][
                        sector
                    ] + data_emis[sub_sector] * converter.get_co_to_h2_factor(sub_sector)
            else:
                df_replacements[comp][sector] = data_emis.sum()
        elif comp == "H2":
            df_replacements[comp][sector] = df_replacements[comp][sector] + data_emis[
                sector
            ] * converter.get_co_to_h2_factor(sector)
        else:
            df_replacements[comp][sector] = (
                df_replacements[comp][sector] + data_emis[sector]
            )
    return df_replacements


def get_sector_column_total(sectors, type_split="sector"):
    if isinstance(sectors, str):
        df_repl = get_sector_column(sectors, type_split=type_split)
        df_repl.rename({sectors: "Total"}, inplace=True)
        return df_repl
    if isinstance(sectors, list):
        df_repl = get_sector_column_total(sectors[0], type_split=type_split)
        print(df_repl)
        # sys.exit(4)
        for i, sector in enumerate(sectors):
            if i > 0:
                df_repl = df_repl + get_sector_column_total(sector, type_split=type_split)
        return df_repl
    if isinstance(sectors, dict):
        for i, (sector, factor) in enumerate(sectors.items()):
            if i == 0:
                df_repl = get_sector_column_total(sector, type_split=type_split) * factor
            else:
                df_repl = df_repl + get_sector_column_total(sector, type_split=type_split) * factor
        return df_repl


def add_leakage(df_repl, h2_total, leak_rate):
    df_with_leak = df_repl.copy()
    print(df_repl)
    df_with_leak["H2"] = df_with_leak["H2"] - leak_rate * h2_total
    print(df_with_leak)
    print(df_with_leak.values.flatten())
    if leak_rate > 0:
        print(h2_total)
        print(h2_total * leak_rate)
    return df_with_leak


def add_prod_emissions(df_repl, h2_total, emis_per_unit_h2):
    df_with_prod = df_repl.copy()
    for coemittant, emis in emis_per_unit_h2.items():
        df_with_prod[coemittant] = df_with_prod[coemittant] - h2_total * emis
    return df_with_prod
