
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
            'REMIND-MAGPIE_SSP5-Baseline':'ssp585'}

scen_out_2 = {'SSP4-34':'ssp434',
            'SSP4-60':'ssp460',
            'SSP1-19':'ssp119',
            'SSP1-26':'ssp126',
            'SSP2-45':'ssp245',
            'SSP3-70 (Baseline)':'ssp370',
            'SSP5-Baseline':'ssp585'}
scens_reverse = {v: k for k, v in scen_out_2.items()}