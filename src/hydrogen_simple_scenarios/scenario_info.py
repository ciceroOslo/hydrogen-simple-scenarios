
scens = ["119", "126", "245", "370", "434", "460", "534-over", "585"]
scens_colours = {'ssp119':"#1e9684", 
                 'ssp126':"#1d3354",
                 'ssp245':"#ead33d",
                 'ssp370':"#f21111", 
                 'ssp434':"#63bde5", 
                 'ssp460':"#e88831", 
                 'ssp534-over':"#9a6dc9", 
                 'ssp585':"#840b12"}

scens_colours_2 = {'SSP1-19':"#1e9684", 
                 'SSP1-26':"#1d3354",
                 'SSP2-45':"#ead33d",
                 'SSP3-70 (Baseline)':"#f21111", 
                 'SSP3-LowNTCF':"pink",
                 'SSP4-34':"#63bde5", 
                 'SSP4-60':"#e88831", 
                 'SSP5-34-OS':"#9a6dc9", 
                 'SSP5-85 (Baseline)':"#840b12"}

scen_out = {'GCAM4_SSP4-34':'ssp434',
            'GCAM4_SSP4-60':'ssp460',
            'IMAGE_SSP1-19':'ssp119',
            'IMAGE_SSP1-26':'ssp126',
            'MESSAGE-GLOBIOM_SSP2-45':'ssp245',
            'REMIND-MAGPIE_SSP5-Baseline':'ssp585',
            'REMIND-MAGPIE_SSP5-34-OS':'ssp534-over',
            "AIM/CGE_SSP3-Baseline": 'ssp370',
            }

scen_out_2 = {'SSP4-34':'ssp434',
            'SSP4-60':'ssp460',
            'SSP1-19':'ssp119',
            'SSP1-26':'ssp126',
            'SSP2-45':'ssp245',
            'SSP3-70 (Baseline)':'ssp370',
            'SSP5-85 (Baseline)':'ssp585',
            'SSP5-34-OS': 'ssp534-over'
            }
scens_reverse = {v: k for k, v in scen_out_2.items()}
scen_reverse_model = {v: k for k, v in scen_out.items()}


steel_sectors = {
    "1A2a_Ind-Comb-Iron-steel": 1,
    "2A2_Lime-production": 0.4,
    "2C_Metal-production": 0.75,
}
natural_gas = {
    "natural_gas": 1
}
# sector = '1A3di_International-shipping'
blue_opt = {"CO2": 1}  # kT CO2 per tonne Hydrogen
blue_pes = {"CO2": 3}
green = {"CO2": 0}

prod_methods = {
    "Blue_optimistic": blue_opt,
    "Blue_pessimistic": blue_pes,
    "Green": green,
}

# 1.8e tonnes steel per year
# 1 ton steel requires 50-60 kg H2
# (Bhaskar et al., 2020; Fischedick et al., 2014; Material Economics, 2019; Rechberger et al., 2020; Vogl et al., 2018) from steel report
# Carbon brief source lists 90 kg H2
# https://www.carboncommentary.com/blog/2020/11/4/how-much-hydrogen-will-be-needed-to-replace-coal-in-making-steel
h2_repl_need_total_steel = 1.8e9 * 5e-5
# TODO: Add natural gas h2_repl_need_total_natural_gas = 
sector_info ={
    "steel": [steel_sectors, h2_repl_need_total_steel]
}

leak_rates = [0, 0.01, 0.05, 0.1]

