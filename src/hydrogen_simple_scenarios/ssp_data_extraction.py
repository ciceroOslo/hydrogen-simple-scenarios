"""
Module to extract data from ssp emissions data files
"""

import numpy as np
import pandas as pd

from .get_emissions_functions import COToHydrogenEmissionsConverter
from .scenario_info import (
    h2_energy_to_mass_conv_factor,
    scen_reverse_model,
    scens_reverse,
)

co_ssp_sectors_burning = ["Forest Burning", "Grassland Burning", "Peat Burning"]
co_ssp_sectors_AFOLU = co_ssp_sectors_burning + [
    "Agricultural Waste Burning",
    "Agriculture",
]
co_ssp_sectors_industrial = [
    "Aircraft",
    "Energy Sector",
    "Industrial Sector",
    "International Shipping",
    "Residential Commercial Other",
    "Transportation Sector",
    "Waste",
    "Solvents Production and Application",
]
co_ssp_sectors = co_ssp_sectors_AFOLU + co_ssp_sectors_industrial


def get_data_for_component_sector_region_ssp(
    file, scen, comp, sector="SUM", region="World", model="empty", filetype="SSP"
):  # pylint: disable=too-many-arguments
    """
    Get data from an SSP or RCMIP file for a specific scenario, component, sector and region

    Parameters
    ----------
    file : str
        Path to file to read data from
    scen : str
        Name of scenario
    comp : str
        Chemical component to read data for
    sector : str
        Sector to read data for, if the default SUM is sent, the sector sum is used
    region : str
        The region for which to read data
    model : str
        If the model used to run the scenario is needed to specify what to read
    filetype : str
        If filetype is SSP or RCMIP which has implications for parts of the formatting

    Returns
    -------
    pd.DataFrame
        With the emissions data according to specifications from specified file
    """
    tot_data = pd.read_csv(file)
    tot_data.columns = [col_name.upper() for col_name in tot_data.columns]
    sector_string = get_sector_string(comp, sector, filetype)
    if scen in scen_reverse_model:
        if sector.endswith("Energy"):
            scen_q = scen_reverse_model[scen].split("_")[1]
        else:
            scen_q = scens_reverse[scen]
        model = scen_reverse_model[scen].split("_")[0]
    else:
        scen_q = scen
    cut_data = tot_data.query(
        f"SCENARIO == '{scen_q}' and REGION == '{region}' and MODEL == '{model}'"
    )
    cut_data = cut_data.query(f"VARIABLE =='{sector_string}'")
    return cut_data


def get_sector_string(comp, sector="SUM", filetype="SSP"):
    """
    Get the sector and component specific string to pick out the correct part of the data

    Parameters
    ----------
    comp : str
        Chemical component to read data for
    sector : str
        Sector to read data for, if the default SUM is sent, the sector sum is used
    filetype : str
        If filetype is SSP or RCMIP which has implications for parts of the formatting

    Returns
    -------
    pd.DataFrame
        With the emissions data according to specifications from specified file
    """
    if filetype == "SSP":
        opening = "CMIP6 Emissions|"
    elif filetype == "RCMIP":
        opening = "Emissions|"
    else:
        opening = ""
    if sector == "SUM":
        return f"{opening}{comp}"
    if filetype == "RCMIP":
        if sector in co_ssp_sectors_AFOLU:
            return f"{opening}{comp}|MAGICC AFOLU|{sector}"
        return f"{opening}{comp}|MAGICC Fossil and Industrial|{sector}"
    if sector not in co_ssp_sectors:
        return f"{sector}|{comp}"
    return f"{opening}{comp}|{sector}"


def get_ts_component_sector_region_ssp(
    file, scen, comp, sector="SUM", region="World", model="empty", filetype="SSP"
):  # pylint: disable=too-many-arguments
    """
    Get the timeseries data for a component sector region and ssp

    Parameters
    ----------
    file : str
        Path to file to read data from
    scen : str
        Name of scenario
    comp : str
        Chemical component to read data for
    sector : str
        Sector to read data for, if the default SUM is sent, the sector sum is used
    region : str
        The region for which to read data
    model : str
        If the model used to run the scenario is needed to specify what to read
    filetype : str
        If filetype is SSP or RCMIP which has implications for parts of the formatting

    Returns
    -------
    pd.DataFrame
        With the emissions data according to specifications from specified file
    """
    converter = COToHydrogenEmissionsConverter()
    if filetype == "SSP":
        meta_len = 5
    elif filetype == "RCMIP":
        meta_len = 7
    else:
        meta_len = 0
    if comp != "H2":
        read_data = get_data_for_component_sector_region_ssp(
            file,
            scen,
            comp,
            sector=sector,
            region=region,
            model=model,
            filetype=filetype,
        )
        if read_data.shape[0] == 0:
            return np.zeros(read_data.shape[1] - meta_len)
        return read_data.iloc[0, meta_len:].to_numpy(dtype=float)
    if sector != "SUM":
        read_data = get_data_for_component_sector_region_ssp(
            file,
            scen,
            "CO",
            sector=sector,
            region=region,
            model=model,
            filetype=filetype,
        )
        if read_data.shape[0] == 0:
            return np.zeros(read_data.shape[1] - meta_len)
        return read_data.iloc[0, meta_len:].to_numpy(
            dtype=float
        ) * converter.get_co_to_h2_factor_cmip6(sector)
    timeseries = None
    for co_sector in co_ssp_sectors:
        co_df = get_data_for_component_sector_region_ssp(
            file,
            scen,
            "CO",
            sector=co_sector,
            region=region,
            model=model,
            filetype=filetype,
        )
        if co_df.shape[0] == 0:
            continue
        if timeseries is None:
            timeseries = co_df.iloc[0, meta_len:].to_numpy(
                dtype=float
            ) * converter.get_co_to_h2_factor_cmip6(co_sector)
        else:
            timeseries = timeseries + co_df.iloc[0, meta_len:].to_numpy(
                dtype=float
            ) * converter.get_co_to_h2_factor_cmip6(co_sector)
    return timeseries


def get_ts_hydrogen_energy_and_mass(file, scen, region="World", model="empty"):
    """
    Get the H2 energy and mass from an IAM-data file

    Parameters
    ----------
    file : str
        Path to file to read data from
    scen : str
        Name of scenario
    region : str
        The region for which to read data
    model : str
        If the model used to run the scenario is needed to specify what to read

    Returns
    -------
    list
        With the timeseries of energy in the fom of hydrogen, and amount of hydrogen
        that corresponds to
    """
    energy_ts = get_ts_component_sector_region_ssp(
        file,
        scen,
        comp="Hydrogen",
        sector="Secondary Energy",
        region=region,
        model=model,
    )
    mass_ts = energy_ts * h2_energy_to_mass_conv_factor
    return energy_ts, mass_ts


def get_years(file):
    """
    Get the series of years in an ssp csv-file

    Parameters
    ----------
    file : str
        Path to the file to be read from

    Returns
    -------
    pd.Series
        With the years contained in the file
    """
    years = pd.read_csv(file).columns[5:]
    return years


def get_unique_scenarios_and_models(file):
    """
    Get a list of unique scenario and model combinations in a file

    Parameters
    ----------
    file : str
        Path to the file to be read from

    Returns
    -------
    pd.Series
        With the years contained in the file
    """
    lists = pd.read_csv(file)[["MODEL", "SCENARIO"]].drop_duplicates()
    return lists.to_numpy()
