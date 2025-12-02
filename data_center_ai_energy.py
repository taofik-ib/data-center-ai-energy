
"""
Data Center Energy Use in the AI Era
Generates figures showing total electricity use, emissions scenarios,
and AI vs non-AI energy use from 2015–2030.

Run:
    python data_center_ai_energy.py

Requires:
    pip install matplotlib pandas numpy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Make figures directory
FIG_DIR = Path("figures")
FIG_DIR.mkdir(exist_ok=True)

plt.rcParams["figure.figsize"] = (10, 6)

# ============================================================
# HISTORICAL IEA-BASED DATA (TWh)
# ============================================================

data_hist = {
    2015: 200,                 # ~200 TWh in 2015
    2018: 200,                 # ~200 TWh in 2018
    2020: (200 + 250) / 2,     # mid-point 200–250 TWh
    2021: (220 + 320) / 2,     # mid-point 220–320 TWh
    2022: (240 + 340) / 2,     # mid-point 240–340 TWh
    2024: 415                  # IEA estimate ~415 TWh
}

df_hist = (
    pd.Series(data_hist, name="twh")
    .reset_index()
    .rename(columns={"index": "year"})
    .sort_values("year")
    .reset_index(drop=True)
)

# ============================================================
# PROJECT TO 2030 BASED ON IEA DOUBLING SCENARIO
# ============================================================

start_year = 2024
end_year = 2030
years_proj = np.arange(start_year, end_year + 1)

target_2030_twh = 945   # IEA base-case ~doubling
growth_rate = (target_2030_twh / 415) ** (1 / (end_year - start_year)) - 1

proj_values = [data_hist[start_year]]
for _ in range(start_year + 1, end_year + 1):
    proj_values.append(proj_values[-1] * (1 + growth_rate))

df_proj = pd.DataFrame({
    "year": years_proj,
    "twh_base_case": proj_values
})

# Combine datasets
df_energy = pd.concat(
    [
        df_hist,
        df_proj[df_proj["year"] > df_hist["year"].max()].rename(columns={"twh_base_case": "twh"})
    ],
    ignore_index=True
)

years_all = df_energy["year"].values

# ============================================================
# CARBON INTENSITY (gCO₂/kWh)
# ============================================================

base_case_intensity_points  = {2015: 450, 2024: 380, 2030: 320}
clean_grid_intensity_points = {2015: 450, 2024: 350, 2030: 250}

def interpolate_intensity(years, anchor_dict):
    anchor_years = np.array(sorted(anchor_dict.keys()))
    anchor_vals = np.array([anchor_dict[y] for y in anchor_years])
    return np.interp(years, anchor_years, anchor_vals)

df_energy["intensity_base"]  = interpolate_intensity(years_all, base_case_intensity_points)
df_energy["intensity_clean"] = interpolate_intensity(years_all, clean_grid_intensity_points)

# ============================================================
# AI vs NON-AI ENERGY SHARE (Illustrative)
# ============================================================

ai_share_points = {2015: 0.00, 2020: 0.01, 2024: 0.07, 2030: 0.35}

def interpolate_share(years, anchor_dict):
    anchor_years = np.array(sorted(anchor_dict.keys()))
    anchor_vals  = np.array([anchor_dict[y] for y in anchor_years])
    return np.interp(years, anchor_years, anchor_vals)

df_energy["ai_share"] = interpolate_share(years_all, ai_share_points)
df_energy["ai_twh"]   = df_energy["twh"] * df_energy["ai_share"]
df_energy["non_ai_twh"] = df_energy["twh"] - df_energy["ai_twh"]

# ============================================================
# CO₂ EMISSIONS (MtCO₂)
# ============================================================

df_energy["mtco2_base"]  = df_energy["twh"] * df_energy["intensity_base"] / 1000.0
df_energy["mtco2_clean"] = df_energy["twh"] * df_energy["intensity_clean"] / 1000.0

df_energy["ai_mtco2"]      = df_energy["ai_twh"] * df_energy["intensity_base"] / 1000.0
df_energy["non_ai_mtco2"]  = df_energy["non_ai_twh"] * df_energy["intensity_base"] / 1000.0

# ============================================================
# PLOTS
# ============================================================

# TOTAL ENERGY
plt.figure()
plt.plot(df_energy["year"], df_energy["twh"], marker="o", label="Total Data-Centre Energy")
plt.xlabel("Year"); plt.ylabel("TWh"); plt.title("Global Data-Centre Energy Use")
plt.grid(True, linestyle=":"); plt.tight_layout()
plt.savefig(FIG_DIR / "energy_total.png", dpi=300)
plt.show()

# EMISSIONS
plt.figure()
plt.plot(df_energy["year"], df_energy["mtco2_base"], marker="o", color="tab:orange", label="Base Grid")
plt.plot(df_energy["year"], df_energy["mtco2_clean"], marker="o", linestyle="--", color="tab:blue", label="Clean Grid")
plt.xlabel("Year"); plt.ylabel("MtCO₂"); plt.title("CO₂ Emissions – Base vs Clean Grid")
plt.grid(True, linestyle=":"); plt.legend(); plt.tight_layout()
plt.savefig(FIG_DIR / "emissions_scenarios.png", dpi=300)
plt.show()

# AI VS NON-AI (TIME SERIES)
plt.figure()
plt.plot(df_energy["year"], df_energy["ai_twh"], marker="o", color="tab:red", label="AI Workloads")
plt.plot(df_energy["year"], df_energy["non_ai_twh"], marker="o", color="tab:green", label="Non-AI Workloads")
plt.xlabel("Year"); plt.ylabel("TWh"); plt.title("AI vs Non-AI Data-Centre Electricity Use")
plt.grid(True, linestyle=":"); plt.legend(); plt.tight_layout()
plt.savefig(FIG_DIR / "ai_vs_non_ai_timeseries.png", dpi=300)
plt.show()

# STACKED BAR
years_focus = [2024, 2030]
df_focus = df_energy[df_energy["year"].isin(years_focus)].set_index("year")

plt.figure(figsize=(6, 6))
x = np.arange(len(years_focus))
plt.bar(x, df_focus["non_ai_twh"], color="tab:green", label="Non-AI")
plt.bar(x, df_focus["ai_twh"], bottom=df_focus["non_ai_twh"], color="tab:red", label="AI")
plt.xticks(x, years_focus)
plt.ylabel("TWh"); plt.title("AI vs Non-AI Load (2024 vs 2030)")
plt.legend(); plt.tight_layout()
plt.savefig(FIG_DIR / "ai_vs_non_ai_2024_2030.png", dpi=300)
plt.show()

# PRINT TABLE
print(df_energy)

print("\nAll plots saved in:", FIG_DIR.resolve())
