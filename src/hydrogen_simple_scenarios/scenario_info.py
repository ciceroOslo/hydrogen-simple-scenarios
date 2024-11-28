"""
Module that just contains lists and dictionaries to be used in the other modules
"""

scens = ["119", "126", "245", "370", "434", "460", "534-over", "585"]
scens_colours = {
    "ssp119": "#1e9684",
    "ssp126": "#1d3354",
    "ssp245": "#ead33d",
    "ssp370": "#f21111",
    "ssp434": "#63bde5",
    "ssp460": "#e88831",
    "ssp534-over": "#9a6dc9",
    "ssp585": "#840b12",
}

scens_colours_2 = {
    "SSP1-19": "#1e9684",
    "SSP1-26": "#1d3354",
    "SSP2-45": "#ead33d",
    "SSP3-70 (Baseline)": "#f21111",
    "SSP3-LowNTCF": "pink",
    "SSP4-34": "#63bde5",
    "SSP4-60": "#e88831",
    "SSP5-34-OS": "#9a6dc9",
    "SSP5-85 (Baseline)": "#840b12",
}

scen_out = {
    "GCAM4_SSP4-34": "ssp434",
    "GCAM4_SSP4-60": "ssp460",
    "IMAGE_SSP1-19": "ssp119",
    "IMAGE_SSP1-26": "ssp126",
    "MESSAGE-GLOBIOM_SSP2-45": "ssp245",
    "REMIND-MAGPIE_SSP5-Baseline": "ssp585",
    "REMIND-MAGPIE_SSP5-34-OS": "ssp534-over",
    "AIM/CGE_SSP3-Baseline": "ssp370",
}

scen_out_2 = {
    "SSP4-34": "ssp434",
    "SSP4-60": "ssp460",
    "SSP1-19": "ssp119",
    "SSP1-26": "ssp126",
    "SSP2-45": "ssp245",
    "SSP3-70 (Baseline)": "ssp370",
    "SSP5-85 (Baseline)": "ssp585",
    "SSP5-34-OS": "ssp534-over",
}
scens_reverse = {v: k for k, v in scen_out_2.items()}
scen_reverse_model = {v: k for k, v in scen_out.items()}


steel_sectors = {
    "1A2a_Ind-Comb-Iron-steel": [1, "sector"],
    "2A2_Lime-production": [0.4, "sector"],
    "2C_Metal-production": [0.75, "sector"],
}
natural_gas_sectors = {
    "natural_gas": [1, "fuel"],
    "1B2b_Fugitive-NG-distr": [1, "sector"],
    "1B2b_Fugitive-NG-prod": [1, "sector"],
}
coal_sectors = {"brown_coal": [1, "fuel"], "hard_coal": [1, "fuel"]}
total_sector = {
    "biomass": [1, "fuel"],
    "brown_coal": [1, "fuel"],
    "coal_coke": [1, "fuel"],
    "diesel_oil": [1, "fuel"],
    "hard_coal": [1, "fuel"],
    "heavy_oil": [1, "fuel"],
    "light_oil": [1, "fuel"],
    "natural_gas": [1, "fuel"],
    "process": [1, "fuel"],
}
#    "BHCCS": bhccs
# }
international_shipping_sectors = {"1A3di_International-shipping": [1, "sector"]}

# 1.8e9 tonnes steel per year
# 1 ton steel requires 50-60 kg H2
# (Bhaskar et al., 2020; Fischedick et al., 2014; Material Economics, 2019; Rechberger et al., 2020; Vogl et al., 2018) from steel report
# Carbon brief source lists 90 kg H2
# https://www.carboncommentary.com/blog/2020/11/4/how-much-hydrogen-will-be-needed-to-replace-coal-in-making-steel
H2_REPL_NEED_TOTAL_STEEL = 1.8e9 * 5e-5
# 50 kg = 5e-5 kT (CEDS emissions are in kT)

# Convert to hydrogen mass:
# EJ -> KWh : 277777777777.78
# kWH-> kg H2 : 1 kg H2 = 33.3 kWh (Warwick)
# kg H2 -> Tg H2: 1e-9
H2_ENERGY_TO_MASS_CONV_FACTOR = 277777777777.78 / 33.3 * 1e-9

# Ammonia has 18.6 MJ per kg (https://www.bv.com/perspectives/ammonia-fuel-vs-hydrogen-carrier/)
NH3_ENERGY_TO_MASS_CONV_FACTOR = 1 / (18.6e-12) * 1e-9

# TODO: Better number for this
# For now numbers from figure on page 94 of
# https://iea.blob.core.windows.net/assets/4ad26550-05c4-4495-9891-98e588cd0be8/NetZeroRoadmap_AGlobalPathwaytoKeepthe1.5CGoalinReach-2023Update.pdf
NH3_REPL_NEED_INT_SHIP = 11.5e3 * NH3_ENERGY_TO_MASS_CONV_FACTOR

# Natural gas energy demand 2019
# 3320 Mtoe according to Global_Energy_Review_2019 from iea
# 1 Mtoe = 0.041868 EJ
NATURAL_GAS_ENERGY_DEMAND_2019 = 0.041868 * 3320

# Coal energy demand 2019
# 156.72 EJ 2019 * (1 - 1/7.5)
# Total number from consumption here:
# https://www.energyinst.org/__data/assets/pdf_file/0004/1055542/EI_Stat_Review_PDF_single_3.pdf
# Factor to exclude coal coke, very rough using numbers from Table 1 here:
# https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/08/coal-information-2019_0f028ad4/4a69d8c8-en.pdf
# 1 Mtoe = 0.041868 EJ
COAL_ENERGY_DEMAND_2019 = 156.72 * (1 - 1 / 7.5)

# Wikipedia https://en.wikipedia.org/wiki/World_energy_supply_and_consumption
# Number seems to have come from
# https://yearbook.enerdata.net/total-energy/world-consumption-statistics.html
# 1 Mtoe = 0.041868 EJ
TOTAL_ENERGY_DEMAND_2019 = 0.041868 * 14400
# https://www.statista.com/statistics/1199339/global-hydrogen-production-and-consumption-by-sector/
# This is from gas reformation and not as chemical process by-product.
# 69 MT = 69 Tg # CEDS emissions is in kT
INDUSTRIAL_USE_2019 = 69e3

# https://www.iea.org/reports/ammonia-technology-roadmap/executive-summary
# 185 MT = 185 Tg
INDUSTRIAL_USE_2020_NH3 = 185e3

sector_info = {
    "steel": [steel_sectors, H2_REPL_NEED_TOTAL_STEEL, "H2"],
    "natural_gas": [
        natural_gas_sectors,
        NATURAL_GAS_ENERGY_DEMAND_2019 * H2_ENERGY_TO_MASS_CONV_FACTOR * 1e3,
        "H2",
    ],
    "current_hydrogen": ["native_hydrogen_mid", INDUSTRIAL_USE_2019, "H2"],
    "total": [
        total_sector,
        TOTAL_ENERGY_DEMAND_2019 * H2_ENERGY_TO_MASS_CONV_FACTOR * 1e3,
        "H2",
    ],
}

sector_info_ammonia = {
    "international_shipping": [
        international_shipping_sectors,
        NH3_REPL_NEED_INT_SHIP,
        "NH3",
    ],
    "current_ammonia": ["native_ammonia_mid", INDUSTRIAL_USE_2020_NH3, "NH3"],
    "natural_gas_ammonia": [
        natural_gas_sectors,
        NATURAL_GAS_ENERGY_DEMAND_2019 * NH3_ENERGY_TO_MASS_CONV_FACTOR * 1e3,
        "NH3",
    ],
    "coal_ammonia": [
        coal_sectors,
        NATURAL_GAS_ENERGY_DEMAND_2019 * NH3_ENERGY_TO_MASS_CONV_FACTOR * 1e3,
        "NH3",
    ],
    "total_ammonia": [
        total_sector,
        TOTAL_ENERGY_DEMAND_2019 * NH3_ENERGY_TO_MASS_CONV_FACTOR * 1e3,
        "NH3",
    ],
}

sector_info_all = {**sector_info, **sector_info_ammonia}


leak_rates = {
    "H2": [0, 0.01, 0.05, 0.1],
    # "NH3":[0, 0.01, 0.05, 0.1],
    "NH3": [
        0,
        {"total": 0.007, "H2": 0.002, "N2O": 0, "name": "HB-min"},
        {"total": 0.044, "H2": 0.018, "N2O": 0.004, "name": "HB-mid"},
        {"total": 0.09, "H2": 0.04, "N2O": 0.01, "name": "HB-max"},
    ],
}

# TODO: Figure out how to add "1B2b_Fugitive-NG-prod" sector to
# the blue production sectors...
# 2019 CH4 in "1B2b_Fugitive-NG-prod" (only emission from this sector)
CH4_BLUE = 21.55 / (NATURAL_GAS_ENERGY_DEMAND_2019 * H2_ENERGY_TO_MASS_CONV_FACTOR)
blue_opt = {"CO2": 1, "CH4": CH4_BLUE}  # kT CO2 per ton Hydrogen
blue_pes = {"CO2": 3.8, "CH4": CH4_BLUE}
green = {"CO2": 0}
bhccs = {"CO2": -10.0}


def _rescale_dictionary_items(dictionary, scale_factor):
    new_dict = dictionary.copy()
    for name, item in new_dict.items():
        new_dict[name] = item * scale_factor
    return new_dict


# TODO: Add ammonia specific production methods

prod_methods = {
    "H2": {
        "Blue_optimistic": blue_opt,
        "Blue_compliance": blue_pes,
        "Green": green,
    },
    "NH3": {
        "Blue_optimistic": _rescale_dictionary_items(
            blue_opt, (INDUSTRIAL_USE_2019 * 0.9) / INDUSTRIAL_USE_2020_NH3
        ),
        "Blue_compliance": _rescale_dictionary_items(
            blue_pes, (INDUSTRIAL_USE_2019 * 0.9) / INDUSTRIAL_USE_2020_NH3
        ),
        "Green": green,
    },
}

dnv_scenario_timeline = [
    [2020, 2025, 2030, 2035, 2040, 2045, 2050],
    [0.0, 0.01, 0.06, 0.18, 0.37, 0.59, 0.65],
    [0.0, 0.02, 0.16, 0.47, 0.77, 1.17, 1.72],
]
