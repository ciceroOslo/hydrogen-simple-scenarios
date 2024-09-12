import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../", "src"))

from hydrogen_simple_scenarios import get_emissions_functions, timeseries_functions

sectors = {
    "1A2a_Ind-Comb-Iron-steel": [1, "sector"],
    "2A2_Lime-production": [0.4, "sector"],
    "2C_Metal-production": [0.75, "sector"],
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


df_repl = get_emissions_functions.get_sector_column_total(sectors)
print(df_repl)

years = range(2024, 2051)
timeseries = {
    "cut_all": [np.ones(len(years)), "tab:green", 0],
    "linear_to_zero": [
        timeseries_functions.make_linear_replacement_timeseries(target_rep=1),
        "tab:blue",
        1,
    ],
    "linear_to_half": [
        timeseries_functions.make_linear_replacement_timeseries(target_rep=0.5),
        "tab:orange",
        2,
    ],
    "half": [0.5 * np.ones(len(years)), "tab:red", 3],
}

wait = 2030 - years[0]
timeseries_2030 = {
    "cut_all": [
        np.concatenate((np.zeros(wait), np.ones(len(years) - wait))),
        "tab:green",
        0,
    ],
    "linear_to_zero": [
        np.concatenate(
            (
                np.zeros(wait),
                timeseries_functions.make_linear_replacement_timeseries(
                    start_year=2030, target_rep=1
                ),
            )
        ),
        "tab:blue",
        1,
    ],
    "linear_to_half": [
        np.concatenate(
            (
                np.zeros(wait),
                timeseries_functions.make_linear_replacement_timeseries(
                    start_year=2030, target_rep=0.5
                ),
            )
        ),
        "tab:orange",
        2,
    ],
    "half": [
        np.concatenate((np.zeros(wait), 0.5 * np.ones(len(years) - wait))),
        "tab:red",
        3,
    ],
}

wait = 2040 - years[0]
timeseries_2040 = {
    "cut_all": [
        np.concatenate((np.zeros(wait), np.ones(len(years) - wait))),
        "tab:green",
        0,
    ],
    "linear_to_zero": [
        np.concatenate(
            (
                np.zeros(wait),
                timeseries_functions.make_linear_replacement_timeseries(
                    start_year=2040, target_rep=1
                ),
            )
        ),
        "tab:blue",
        1,
    ],
    "linear_to_half": [
        np.concatenate(
            (
                np.zeros(wait),
                timeseries_functions.make_linear_replacement_timeseries(
                    start_year=2040, target_rep=0.5
                ),
            )
        ),
        "tab:orange",
        2,
    ],
    "half": [
        np.concatenate((np.zeros(wait), 0.5 * np.ones(len(years) - wait))),
        "tab:red",
        3,
    ],
}

all_ts = [timeseries, timeseries_2030, timeseries_2040]

# 1.8e tonnes steel per year
# 1 ton steel requires 50-60 kg H2
# (Bhaskar et al., 2020; Fischedick et al., 2014; Material Economics, 2019; Rechberger et al., 2020; Vogl et al., 2018) from steel report
# Carbon brief source lists 90 kg H2
# https://www.carboncommentary.com/blog/2020/11/4/how-much-hydrogen-will-be-needed-to-replace-coal-in-making-steel
h2_repl_need = 1.8e9 * 5e-5  # tonne* 50kg per tonne

leak_rates = [0, 0.01, 0.1]

x = np.arange(len(timeseries.keys()))
width = 0.25
alphas = [0.8, 0.7, 0.6]

hyd_per_mit_carbon_dict = {}
scen_index = [
    "Replace now no_leak",
    "Replace now leak_1p",
    "Replace now leak_10p",
    "Delay to 2030 no_leak",
    "Delay to 2030 leak 1p",
    "Delay to 2030 leak 10p",
    "Delay to 2040 no leak",
    "Delay to 2040 leak 1p",
    "Delay to 2040 leak 10p",
]

for name_prod, prod_method in prod_methods.items():
    fig, axs = plt.subplots(3, 2)
    fig.suptitle(f"{name_prod} Steel")
    print(f"Timeseries_2040.keys {timeseries_2040.keys()}")

    hydrogen_per_mitigated_carbon = np.zeros((len(scen_index), len(timeseries_2040)))

    for row_num, timeseries_del in enumerate(all_ts):
        for scen_i, (scen, values) in enumerate(timeseries_del.items()):
            ts = values[0]
            col = values[1]
            # print(len(years))
            # print(len(ts))
            # print(row_num)
            # axs[row_num, 0].plot(years, ts*100, color=col, label=scen)
            # axs[row_num, 0].set_ylabel("%")
            # axs[row_num, 0].set_xlabel("Year")
            multiplier = 0
            placement = x[values[2]]
            for lr in leak_rates:
                replaced_emis = timeseries_functions.add_leakage_ts(
                    df_repl, ts, years, lr, h2_repl_need
                )
                replaced_emis = timeseries_functions.add_prod_emissions_ts(
                    replaced_emis, h2_repl_need, prod_method, years, ts
                )
                GWP = timeseries_functions.calc_gwp(replaced_emis, years)
                print(f"GWP: {GWP} for leak rate {lr} in exp")
                hydrogen_per_mitigated_carbon[row_num * 3 + multiplier, scen_i] = (
                    GWP
                    / timeseries_functions.get_hydrogen_used(
                        ts, lr, h2_repl_need
                    )
                )
                offset = width * multiplier
                rects = axs[row_num, 0].bar(
                    placement + offset,
                    GWP,
                    width,
                    color=col,
                    label=f"Leak rate {lr}",
                    alpha=alphas[multiplier],
                )
                rects = axs[row_num, 1].bar(
                    placement + offset,
                    GWP * 1.65e-9,
                    width,
                    color=col,
                    label=f"Leak rate {lr}",
                    alpha=alphas[multiplier],
                )
                multiplier += 1

        axs[row_num, 0].set_ylim([0, 5.5e7])
        axs[row_num, 0].set_ylabel("kt CO2 equiv")
        axs[row_num, 0].set_title("Mitigated CO2")
        axs[row_num, 1].set_ylim([0, 0.1])
        axs[row_num, 1].set_ylabel("K avoided")
        axs[row_num, 1].set_title("Mitigated warming")
    # axs[row_num,0].legend()
    # axs[row_num, 1].legend()
    # axs[0, 0].set_title("Start replacement now")
    # axs[1, 0].set_title("Delay action to 2030")
    # axs[2, 0].set_title("Delay action to 2040")

    hydrogen_per_mitigated_carbon_df = pd.DataFrame(
        hydrogen_per_mitigated_carbon,
        index=scen_index,
        columns=timeseries_2040.keys(),
    )
    axs[0, 0].set_xticks([])
    axs[1, 0].set_xticks([])

    axs[2, 0].set_xticks(x + width, timeseries.keys(), rotation=45)

    axs[0, 1].set_xticks([])
    axs[1, 1].set_xticks([])

    axs[2, 1].set_xticks(x + width, timeseries.keys(), rotation=45)
    plt.tight_layout()
    plt.savefig(f"{name_prod}_steel_replacement_simple_scenarios_w_temp_CO2_CH4.png")
    print(hydrogen_per_mitigated_carbon)
    plt.clf()
    hyd_per_mit_carbon_dict[name_prod] = hydrogen_per_mitigated_carbon_df.copy()
plt.clf()

fig, axs = plt.subplots(2)
x = np.arange(len(prod_methods.keys()))
multiplier = 0
colors = {
    "Blue_optimistic": "deepskyblue",
    "Blue_pessimistic": "navy",
    "Green": "forestgreen",
}
for method in prod_methods:
    placement = x[multiplier // len(prod_methods.keys())]
    for lr in leak_rates:
        offset = width * multiplier
        # print(hyd_per_mit_carbon_dict[method])
        # print(type(hyd_per_mit_carbon_dict[method]))
        # print(lr)
        carbon_per_H2_here = hyd_per_mit_carbon_dict[method].iloc[
            multiplier % len(prod_methods.keys()), 0
        ]
        carbon_per_H2_noleak = hyd_per_mit_carbon_dict[method].iloc[0, 0]
        percent_offset = (
            (carbon_per_H2_noleak - carbon_per_H2_here) / carbon_per_H2_noleak * 100
        )
        print(percent_offset)
        rects = axs[0].bar(
            placement + offset,
            carbon_per_H2_here,
            width,
            color=colors[method],
            label=f"{method} with leak rate {lr} ",
            alpha=alphas[multiplier % len(prod_methods.keys())],
        )
        rects2 = axs[1].bar(
            placement + offset,
            percent_offset,
            width,
            color=colors[method],
            label=f"{method} with leak rate {lr} ",
            alpha=alphas[multiplier % len(prod_methods.keys())],
        )
        multiplier = multiplier + 1
axs[0].set_title("Mitigated carbon per unit of hydrogen employed")
axs[0].set_ylabel("kT CO2 equiv / kT H2")
axs[0].set_xticks(x + width * (x * 3 + 1), prod_methods, rotation=45)
axs[1].set_title("Percent penalty for H2 leakage of 0, 0.01 and 0.1")
axs[1].set_ylabel("%")
axs[1].set_xticks(x + width * (x * 3 + 1), prod_methods, rotation=45)
plt.tight_layout()
plt.savefig("Mitigated_CO2_per_hydrogen_used_CO2_CH4.png")
# plt.show()
