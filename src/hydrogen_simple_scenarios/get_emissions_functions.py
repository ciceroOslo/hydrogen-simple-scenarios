"""
Module to read and get emissions for compounds and scenario
"""

import numpy as np
import pandas as pd

from .scenario_info import INDUSTRIAL_USE_2019

# FILEPATH = "/div/pdo/emissions/CEDS0521/TOTALS/"
FILEPATH = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/"

# GWP_dict = {"H2": 11.6, "CO2": 1, "CO": 2.3, "CH4":27.9,  "NMVOC": 10.9, "NOx": -(42+56)/2}
GWP_dict = {"H2": 11.6, "CO2": 1, "CO": 2.3, "CH4": 27.9, "NMVOC": 10.5, "NOx": 0}
GWP20_dict = {
    "H2": 37.3,
    "CO2": 1,
    "CO": (7.6 + 8.2) / 2,
    "CH4": 81.2,
    "NMVOC": (38 + 35) / 2,
    "NOx": 0,
}
# H2: Sand et al 2023, CO, NMVOC and NOx global summer/winter average from Aamaas 2016, CH4 AR6
complist = GWP_dict.keys()


# AGWP_CO2 =


class COToHydrogenEmissionsConverter:
    """
    Class to convert CO emissions to Hydrogen emissions
    """

    # From supplementary of Paulot et al 2021
    # international journal of hydrogen energy 4 6 ( 2 0 2 1 ) 1 3 4 4 6e1 3 4 6 0
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
        "Agricultural Waste Burning": 102,  # Crop residue
        "Pasture Maintenance": 135,
        "Boreal Forest": 127,
        "Temperate Forest": 89,
        "Extratropical Forest": 122,
        "Peat Burning": 182,
        "Chaparral": 67,  # Californian shrublike ecosystem
        "Open Cooking": 77,
        "Patsari Stoves": 42,  # Particular stove type for wood
        "Charcoal Making": 255,
        "Charcoal Burning": 189,
        "Dung Burning": 105,
        "Garbage Burning": 38,
    }

    h2_g_per_kg_dry_matter_burnt = {
        "Tropical Forest": 3.36,
        "Savanna": 1.7,
        "Agricultural Waste Burning": 2.59,  # Crop residue
        "Boreal Forest": 2.03,  # Assumed equal to temperate
        "Temperate Forest": 2.03,
        "Extratropical Forest": 2.03,
        "Peat Burning": 1.2,  # From Andreae according to Paulot
        "Garbage Burning": 0.091,
    }

    def __init__(self, just_CO2=False, ignore_bb=False):
        """
        Initialise COToHydrogenEmissionsConverter object

        Parameters
        ----------
        just_CO2 : bool
            Whether to ignore all non-CO2 components in calculations
        ignore_bb : bool
            Whether to ignore biomass burning emissions in calculations
        """
        self.just_CO2 = just_CO2
        self.ignore_bb = ignore_bb

    def get_co_to_h2_factor_burning_cmip6(self, sector):
        """
        Get the CO to H2 factor for CMIP6 biomass burning sectors

        Parameters
        ----------
        sector : str
            Sector name

        Returns
        -------
        float
            The CO to H2 factor to use for the sector
        """
        if self.just_CO2 or self.ignore_bb:
            return 0
        if sector in self.h2_g_per_kg_dry_matter_burnt:
            sector_here = sector
        elif sector == "Grassland Burning":
            sector_here = "Savanna"
        elif sector == "Forest Burning":
            sector_here = "Extratropical Forest"
        else:
            print(f"Why am I here with {sector}")
            sector_here = "Garbage Burning"
        return (
            self.h2_g_per_kg_dry_matter_burnt[sector_here]
            / self.co_g_per_kg_dry_mass[sector_here]
        )

    def get_co_to_h2_factor(self, sector):
        """
        Get the CO to H2 factor for CEDS sectors

        Parameters
        ----------
        sector : str
            Sector name

        Returns
        -------
        float
            The CO to H2 factor to use for the sector
        """
        if self.just_CO2:
            factor = 0
        elif sector[0] == "5":
            factor = self.co_h2_factors["Waste"]
        elif sector[0] == "3" or sector[:3] == "1A3" or sector[:4] == "1A4c":
            factor = self.co_h2_factors["Agr_transp"]
        elif sector[:4] == "1A4b":
            factor = self.co_h2_factors["Residential"]
        else:
            factor = self.co_h2_factors["Energy_ind"]
        return factor

    def get_co_to_h2_factor_cmip6(self, sector):
        """
        Get the CO to H2 factor for CMIP6 sectors

        Parameters
        ----------
        sector : str
            Sector name

        Returns
        -------
        float
            The CO to H2 factor to use for the sector
        """
        if self.just_CO2:
            return 0
        if "Burning" in sector:
            return self.get_co_to_h2_factor_burning_cmip6(sector)
        if sector in self.co_h2_factors:
            return self.co_h2_factors[sector]
        if "Energy" in sector or "Industrial" in sector:
            return self.co_h2_factors["Energy_ind"]
        if "Residential" in sector:
            return self.co_h2_factors["Residential"]
        return self.co_h2_factors["Agr_transp"]


def prepare_emis_df(comp, type_split, year=2019, file_suffix="_2021_04_21.csv"):
    """
    Prepare an emissions DataFrame to hold emissions

    Parameters
    ----------
    comp : str
        Name of the component, can be any of available components
    type_split : str
        What type of split of sectors the sector
        are to be taken from (i.e. sector or fuel)
    year : int
        Year to get data for
    file_suffix : str
        Last part of filename, which will allow user to choose between different emisison data versions

    Returns
    -------
    pd.DataFrame
        DataFrame of emissions for the year, split in sectors per the given typesplit using a file
        version given by the file_suffix
    """
    if file_suffix.startswith("_v2024"):
        file_middle = "_CEDS_global_emissions_by_"
    else:
        file_middle = "_global_CEDS_emissions_by_"

    filename = comp + file_middle + type_split + file_suffix
    if type_split == "sector":
        data_emis = pd.read_csv(
            FILEPATH + filename, delimiter=",", index_col=1, header=0, skiprows=0
        ).T
    else:
        data_emis = pd.read_csv(
            FILEPATH + filename, delimiter=",", index_col=0, header=0, skiprows=0
        ).T
    data_emis = data_emis.drop(["em", "units"])

    data_emis.index.name = "Year"
    index = data_emis.index.values
    for i, year_name in enumerate(index):
        index[i] = year_name.split("X")[-1]
    data_emis.index = index.astype(int)
    data_emis_yr = data_emis.loc[year]
    data_emis_yr.name = comp
    return data_emis_yr


def get_native_hydrogen_sector_column(sector, df_replacements):
    """
    Get CO2 emissions for native hydrogen sector

    Parameters
    ----------
    sector : str
        Name of sector, should start with native_hydrogen, and can be low, high or mean
        CO2 equivalent emissions per hydrogen use
    df_replacements: pd.DataFrame
        Dataframe to fill in the CO2 equivalent emissions from the native hydrogen use into

    Returns
    -------
    pd.DataFrame
        With single row of emissions for the year and sector, now filled in with native hydrogen
        emissions for the chosen per hydrogen CO2 equivalent emissions.
    """
    per_hydrogen_co2 = [17.21, 10.09]
    if sector == "native_hydrogen_high":
        df_replacements.at[sector, "CO2"] = INDUSTRIAL_USE_2019 * per_hydrogen_co2[0]
    elif sector == "native_hydrogen_low":
        df_replacements.at[sector, "CO2"] = INDUSTRIAL_USE_2019 * per_hydrogen_co2[1]
    else:
        df_replacements.at[sector, "CO2"] = INDUSTRIAL_USE_2019 * np.mean(
            per_hydrogen_co2
        )
    return df_replacements


def get_sector_column(
    sector,
    type_split="sector",
    just_CO2=False,
    ignore_bb=False,
    year=2019,
    file_suffix="_2021_04_21.csv",
):  # pylint: disable=too-many-arguments
    """
    Get emissions for all components for a specific sector

    Parameters
    ----------
    sector : str
        Name of sector, can be single sector or Total for a sum of all sectors
    type_split : str
        What type of split of sectors the sector or sectors
        are to be taken from (i.e. sector or fuel)
    just_CO2 : bool
        Whether to consider just CO2 emissions, or other also other short lived forcers
    ignore_bb : bool
        Wheter to omit biomass burning emissions
    year : int
        Year to get data for
    file_suffix : str
        Last part of filename, which will allow user to choose between different emisison data versions

    Returns
    -------
    pd.DataFrame
        With single row of emissions for the year, sector and each compound in each column
    """
    df_replacements = pd.DataFrame(0.0, columns=complist, index=[sector])
    if sector.startswith("native_hydrogen"):
        return get_native_hydrogen_sector_column(sector, df_replacements)

    for comp in complist:
        df_replacements[comp][sector] = get_sector_column_single_comp(
            comp,
            sector,
            type_split=type_split,
            just_CO2=just_CO2,
            ignore_bb=ignore_bb,
            year=year,
            file_suffix=file_suffix,
        )
    return df_replacements


def get_sector_column_single_comp(
    comp,
    sector,
    type_split="sector",
    just_CO2=False,
    ignore_bb=False,
    year=2019,
    file_suffix="_2021_04_21.csv",
):  # pylint: disable=too-many-arguments
    """
    Get emissions single component

    Parameters
    ----------
    comp : str
        Name of the component, can be any of available components
    sector : str
        Name of sector, can be single sector or Total for a sum of all sectors
    type_split : str
        What type of split of sectors the sector or sectors
        are to be taken from (i.e. sector or fuel)
    just_CO2 : bool
        Whether to consider just CO2 emissions, or other also other short lived forcers
    ignore_bb : bool
        Wheter to omit biomass burning emissions
    year : int
        Year to get data for
    file_suffix : str
        Last part of filename, which will allow user to choose between different emisison data versions

    Returns
    -------
    float
        The emissions for the year, sector and compound combination
    """
    if comp == "H2":
        data_emis = prepare_emis_df(
            "CO", type_split, year=year, file_suffix=file_suffix
        )
        converter = COToHydrogenEmissionsConverter(
            just_CO2=just_CO2, ignore_bb=ignore_bb
        )
    else:
        data_emis = prepare_emis_df(
            comp, type_split, year=year, file_suffix=file_suffix
        )
    if sector == "Total":
        sum_tot = 0
        if comp == "H2":
            for sub_sector in data_emis.index:
                sum_tot = sum_tot + data_emis[
                    sub_sector
                ] * converter.get_co_to_h2_factor(sub_sector)
            return sum_tot
        return data_emis.sum()
    if comp == "H2":
        return data_emis[sector] * converter.get_co_to_h2_factor(sector)

    return data_emis[sector]


def get_sector_column_total(sectors, type_split="sector", just_CO2=False):
    """
    Get a total sector column

    Parameters
    ----------
    sectors : str, list or dict
        The sectors to be summed. If str a total single sector is
        assumed. If a list, a list of sector names from which
        all sectors have the whole sector added is assumed.
        If a dict, the dict should have sector names as keys,
        and ratio of sector to be considered as values
    type_split : str
        What type of split of sectors the sector or sectors
        are to be taken from (i.e. sector or fuel)
    just_CO2 : bool
        Whether to consider just CO2 emissions, or other also other short lived forcers

    Returns
    -------
    pd.DataFrame
            Dataframe contining emissions per emissions species
            for the sector in the year 2019
    """
    if isinstance(sectors, str):
        df_repl = get_sector_column(sectors, type_split=type_split, just_CO2=just_CO2)
        df_repl.rename({sectors: "Total"}, inplace=True)
        return df_repl
    if isinstance(sectors, list):
        df_repl = get_sector_column_total(
            sectors[0], type_split=type_split, just_CO2=just_CO2
        )
        for i, sector in enumerate(sectors):
            if i > 0:
                df_repl = df_repl + get_sector_column_total(
                    sector, type_split=type_split, just_CO2=just_CO2
                )
        return df_repl
    if isinstance(sectors, dict):
        for i, (sector, info) in enumerate(sectors.items()):
            if i == 0:
                df_repl = (
                    get_sector_column_total(
                        sector, type_split=info[1], just_CO2=just_CO2
                    )
                    * info[0]
                )
            else:
                df_repl = (
                    df_repl
                    + get_sector_column_total(
                        sector, type_split=info[1], just_CO2=just_CO2
                    )
                    * info[0]
                )
        return df_repl
    raise TypeError("Sector must be str, list or dict")


def add_leakage(df_repl, h2_total, leak_rate):
    """
    Add H2 leakage to sector

    Parameters
    ----------
    df_repl : pd.DataFrame
        Dataframe of emissions to add leaks to
    h2_total : float
        Total Hydrogen needed to repl
    leak_rate : float
        Leak rate of hydrogen, should be in range 0-1

    Returns
    -------
        pd.DataFrame
            Dataframe of emissions mitigated minus H2 emissions
    """
    df_with_leak = df_repl.copy()
    df_with_leak["H2"] = df_with_leak["H2"] - leak_rate * h2_total
    return df_with_leak


def add_prod_emissions(df_repl, h2_total, emis_per_unit_h2):
    """
    Add H2 leakage to sector

    Parameters
    ----------
    df_repl : pd.DataFrame
        Dataframe of emissions to add leaks to
    h2_total : float
        Total Hydrogen needed to repl
    emis_per_unit_h2 : dict
        Emissions of various species in the production of h2
        per unit of H2 used/produced

    Returns
    -------
        pd.DataFrame
            Dataframe of emissions mitigated minus H2 production emissions
    """
    df_with_prod = df_repl.copy()
    for coemittant, emis in emis_per_unit_h2.items():
        df_with_prod[coemittant] = df_with_prod[coemittant] - h2_total * emis
    return df_with_prod
