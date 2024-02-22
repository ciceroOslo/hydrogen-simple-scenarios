import pandas as pd
import matplotlib.pyplot as plt
import sys

filepath = "/div/pdo/emissions/CEDS0521/TOTALS/"

# GWP_dict = {"H2": 11.6, "CO2": 1, "CO": 2.3, "CH4":27.9,  "NMVOC": 10.9, "NOx": -(42+56)/2}
GWP_dict = {"H2": 11.6, "CO2": 1, "CO": 2.3, "CH4": 27.9, "NMVOC": 10.9, "NOx": 0}
# H2: Sand et al 2023, CO, NMVOC and NOx global summer/winter average from Aamaas 2016, CH4 AR6
complist = GWP_dict.keys()

# AGWP_CO2 =


def make_linear_replacement_timeseries(start_year=2024, end_year=2050, target_rep=0.5):
    years_here = range(start_year, end_year + 1)
    values = np.linspace(0, target_rep, num=len(years_here))
    return values


co_h2_factors = {
    "Agr_transp": 0.0357,
    "Energy_ind": 0.0143,
    "Residential": 0.0217,
    "Waste": 0.357,
}
just_CO2 = False


def get_co_to_h2_factor(sector):
    if just_CO2:
        return 0
    if sector[0] == "5":
        return co_h2_factors["Waste"]
    if sector[0] == "3":
        return co_h2_factors["Agr_transp"]
    if sector[:3] == "1A3":
        return co_h2_factors["Agr_transp"]
    if sector[:4] == "1A4b":
        return co_h2_factors["Residential"]
    if sector[:4] == "1A4c":
        return co_h2_factors["Agr_transp"]
    else:
        return co_h2_factors["Energy_ind"]

def get_co_to_h2_factor_cmip6(sector):
    if just_CO2:
        return 0
    if sector[0] == "5":
        return co_h2_factors["Waste"]
    if sector[0] == "3":
        return co_h2_factors["Agr_transp"]
    if sector[:3] == "1A3":
        return co_h2_factors["Agr_transp"]
    if sector[:4] == "1A4b":
        return co_h2_factors["Residential"]
    if sector[:4] == "1A4c":
        return co_h2_factors["Agr_transp"]
    else:
        return co_h2_factors["Energy_ind"]


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


def get_sector_column(sector, type_split="sector"):
    df_replacements = pd.DataFrame(0.0, columns=complist, index=[sector])
    for c, comp in enumerate(complist):
        if comp == "H2":
            data_emis = prepare_emis_df("CO", type_split, yr=2019)

        else:
            data_emis = prepare_emis_df(comp, type_split, yr=2019)
        if sector == "Total":
            if comp == "H2":
                # print(data_emis)
                for sector in data_emis.index:
                    df_replacements[comp][sector] = df_replacements[comp][
                        sector
                    ] + data_emis[sector] * get_co_to_h2_factor(sector)
            else:
                df_replacements[comp][sector] = data_emis.sum()
                continue
        if comp == "H2":
            df_replacements[comp][sector] = df_replacements[comp][sector] + data_emis[
                sector
            ] * get_co_to_h2_factor(sector)
        else:
            df_replacements[comp][sector] = (
                df_replacements[comp][sector] + data_emis[sector]
            )
    return df_replacements


def get_sector_column_total(sectors):
    if isinstance(sectors, str):
        df_repl = get_sector_column(sectors)
        df_repl.rename({sectors: "Total"}, inplace=True)
        return df_repl
    if isinstance(sectors, list):
        df_repl = get_sector_column_total(sectors[0])
        print(df_repl)
        # sys.exit(4)
        for i, sector in enumerate(sectors):
            print(sector)
            if i > 0:
                df_repl = df_repl + get_sector_column_total(sector)
        return df_repl
    if isinstance(sectors, dict):
        for i, (sector, factor) in enumerate(sectors.items()):
            if i == 0:
                df_repl = get_sector_column_total(sector) * factor
            else:
                df_repl = df_repl + get_sector_column_total(sector) * factor
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
