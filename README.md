# hydrogen-simple-scenarios

Module for simple comparison of climate impacts of hydrogen replacements in various sectors.

Used for Sandstad, M., Krishnan, S., Myhre G., Sand M., and Skeie R. B.: "What to consider when considering climate effects of Hydrogen – towards an assessment framework" (2024), source files includes code for reading in emissions on CMIP6 or CEDS format per sector region and component, with simple information on selected sectors, functionality to calculate, sum and integrate GWP100, GWP20 and GWPstar for single year and timeseries of replacement.

script folder contains demonstration code and code that reproduces the figures in the paper and do some other things. ´make_ceds_anthro_for_simpleh2.py´ and ´make_emissions_for_simpleh2.py´ produces emission files of just anthropogenic emissions from ceds and for ssps respectively. ´make_gwp_replacement_plots.py´ demonstrates some replacement plots for steel. ´make_various_plots.py´ demonstrates reading and making a few plots for CO NOx and methane in various ssps. 

´make_sector_number_tables.py´ makes the numbers for Tab. 1  of the paper.
´make_various_per_hydrogen_employed_plots.py´ makes Figs 1, 2, S1, S2 and S3 of the paper
´make_scenario_timelines.py´ makes Figs 3, 4 and S4 of the paper.

The module also has tools to setup a pip environment that easily allows you to use the code. When having cloned the repositories you should be able to get that set up and ready to use using this sequence of commands while inside the top folder of the repository:

```
make first-venv
make clean
make virtual-environment
source venv/bin/activate
```

One Caveat to usage is input data. To make the code work CEDS input data of the kind available here: https://data.pnnl.gov/dataset/CEDS-4-21-21 and SSP input data available here https://tntcat.iiasa.ac.at/SspDb/dsd?Action=htmlpage&page=about needs to be available in an input data directory. Swap out all occurences in hte path of "/mnt/c/Users/masan/Downloads/Input_for_scenarios/" with the path where you keep your input data, and the code should work, as should the test suite for the code.