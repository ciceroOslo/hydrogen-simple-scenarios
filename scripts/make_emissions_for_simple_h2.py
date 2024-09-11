import sys, os
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../", "src"))

from hydrogen_simple_scenarios import ssp_data_extraction

data_path = "/mnt/c/Users/masan/Downloads/Input_for_scenarios/"

ssp_file = f"{data_path}SSP_CMIP6_201811.csv"
rcmip_file = (
    f"{data_path}rcmip-emissions-annual-means-ssp370-lowNTCF-only-20191218T1423.csv"
)

ssps = [
    "ssp119",
    "ssp126",
    "ssp245",
    # "ssp370-lowNTCF",
    "ssp370",
    "ssp434",
    "ssp460",
    "ssp534-over",
    "ssp585",
]
species = ["BC", "OC", "NH3"]  # ["H2", "CO", "VOC", "NOx"]
years_ssp = ssp_data_extraction.get_years(ssp_file)
for comp in species:
    # get historical:
    scen = "ssp370-lowNTCF-aerchemmip"
    # First total:
    rcmip_data_total = ssp_data_extraction.get_ts_component_sector_region_ssp(
        rcmip_file, scen, comp, model="AIM/CGE", filetype="RCMIP"
    )
    rcmip_data_total = rcmip_data_total[: 2015 - 1750]
    print(len(rcmip_data_total))
    # Pick out burning sectors:
    rcmip_data_burning = None
    for sector in ssp_data_extraction.co_ssp_sectors_burning:
        print(sector)
        if rcmip_data_burning is None:
            rcmip_data_burning = ssp_data_extraction.get_ts_component_sector_region_ssp(
                rcmip_file,
                scen,
                comp,
                sector=sector,
                region="World",
                model="AIM/CGE",
                filetype="RCMIP",
            )
        else:
            rcmip_data_burning = (
                rcmip_data_burning
                + ssp_data_extraction.get_ts_component_sector_region_ssp(
                    rcmip_file,
                    scen,
                    comp,
                    sector=sector,
                    region="World",
                    model="AIM/CGE",
                    filetype="RCMIP",
                )
            )
        # print(rcmip_data_burning)
    # sys.exit(4)

    # Data no burning
    rcmip_no_burning = rcmip_data_total - rcmip_data_burning[: 2015 - 1750]

    # get ssp data
    for scen in ssps:
        print(scen)

        ssp_total = ssp_data_extraction.get_ts_component_sector_region_ssp(
            ssp_file, scen, comp, filetype="SSP"
        )
        ssp_burning = None
        for sector in ssp_data_extraction.co_ssp_sectors_burning:
            print(sector)
            if ssp_burning is None:
                ssp_burning = ssp_data_extraction.get_ts_component_sector_region_ssp(
                    ssp_file,
                    scen,
                    comp,
                    sector=sector,
                )
            else:
                ssp_burning = (
                    ssp_burning
                    + ssp_data_extraction.get_ts_component_sector_region_ssp(
                        ssp_file,
                        scen,
                        comp,
                        sector=sector,
                    )
                )
        ssp_no_burning = ssp_total - ssp_burning

        # Get linear interpolation for missing years
        ssp_tot_interp = np.append(
            rcmip_data_total, np.interp(range(2015, 2101), years_ssp, ssp_total)
        )
        print(rcmip_data_total[-1])
        print(ssp_tot_interp[0])
        ssp_noburn_interp = np.append(
            rcmip_no_burning, np.interp(range(2015, 2101), years_ssp, ssp_no_burning)
        )
        print(ssp_noburn_interp[2015 - 1750 - 5 : 2015 - 1750 + 5])
        # print out file
        df_tot = pd.DataFrame({"Years": range(1750, 2101), "Emis": ssp_tot_interp})
        df_noburn = pd.DataFrame(
            {"Years": range(1750, 2101), "Emis": ssp_noburn_interp}
        )
        df_tot.to_csv(f"{comp.lower()}_emis_{scen}.csv", index=False)
        df_noburn.to_csv(f"{comp.lower()}_emis_noburn_{scen}.csv", index=False)
