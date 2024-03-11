import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../", "src"))

from hydrogen_simple_scenarios import get_emissions_functions, timeseries_functions, single_year_numbers_check, scenario_info


gwp_benefits = single_year_numbers_check.get_gwp_values_df("steel")
benefit_loss = single_year_numbers_check.get_benefit_loss_df("steel")
gwp_benefits_per_h2 = single_year_numbers_check.get_gwp_values_per_hydrogen_used("steel")
print("--- Steel ---")
print(gwp_benefits_per_h2)


gwp_benefits_ng = single_year_numbers_check.get_gwp_values_df("natural_gas")
benefit_loss_ng = single_year_numbers_check.get_benefit_loss_df("natural_gas")
gwp_benefits_per_h2_ng = single_year_numbers_check.get_gwp_values_per_hydrogen_used("natural_gas")
print("--- Steel ---")
print(gwp_benefits)
print("--- Natural Gas ---")
print(gwp_benefits_ng)
print("--- Steel ---")
print(benefit_loss)
print("--- Natural Gas ---")
print(benefit_loss_ng)
print("--- Steel ---")
print(gwp_benefits_per_h2)
print("--- Natural Gas ---")
print(gwp_benefits_per_h2_ng)

print(scenario_info.sector_info)
print(scenario_info.h2_energy_to_mass_conv_factor )