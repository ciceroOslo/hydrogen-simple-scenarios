import sys, os
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../", "src"))

from hydrogen_simple_scenarios import get_emissions_functions


def calc_gwp_star_annual_ts(emis_ts, component="CH4"):
    gwp_star_ts = np.zeros(len(emis_ts))
    gwp100 = get_emissions_functions.GWP_dict[component]
    for y, value in enumerate(emis_ts):
        gwp = 4 * emis_ts[y] * gwp100
        if y >= 20:
            gwp = gwp - 3.75 * emis_ts[y - 20] * gwp100
        gwp_star_ts[y] = gwp
    return gwp_star_ts


def calc_gwp_annual_ts(emis_ts, component="CH4"):
    gwp100 = get_emissions_functions.GWP_dict[component]
    gwp_ts = emis_ts * gwp100
    return gwp_ts


def accumulated_ts(annual_gwp):
    return np.cumsum(annual_gwp)


emis_const_emis = 4 * np.ones(200)
emis_const_emis[0] = 0
emis_step_change_to_fall = np.zeros(200)
emis_step_change_to_fall[1:51] = 4
emis_step_change_to_fall[51:100] = -4 / 50 * np.arange(49) + 4

ts_list = [emis_const_emis, emis_step_change_to_fall]

fig, ax = plt.subplots(nrows=2, ncols=3, sharex=True)
for i, ts in enumerate(ts_list):
    # Emissions plots:
    ax[i, 0].plot(range(200), ts)
    # GWP annual plots:
    ax[i, 1].plot(range(200), calc_gwp_annual_ts(ts) / 1e3, label="GWP")
    ax[i, 1].plot(range(200), calc_gwp_star_annual_ts(ts) / 1e3, label="GWP*")
    # Accumulated plots:
    ax[i, 2].plot(range(200), accumulated_ts(calc_gwp_annual_ts(ts)) / 1e3, label="GWP")
    ax[i, 2].plot(
        range(200), accumulated_ts(calc_gwp_star_annual_ts(ts)) / 1e3, label="GWP*"
    )
    ax[i, 1].legend()
    ax[i, 2].legend()
ax[0, 0].set_title("CH4 emissions")
ax[0, 1].set_title("CO2 eq. emissions")
ax[0, 2].set_title("CH4 warming,\n cum CO2 eq emissions")
plt.tight_layout()
plt.show()
