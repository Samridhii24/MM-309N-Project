import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


# ===========================================================
# 📘 Load CSV files
# ===========================================================
ce_file = "Assignment-2 - Cohesive Energy (1).csv"
lp_file = "Assignment-2 - Lattice Parameter (1).csv"

ce = pd.read_csv(ce_file, header=1)
lp = pd.read_csv(lp_file, header=1)


# ===========================================================
# ⚙️ Data Cleaning and Composition Normalization
# ===========================================================
def clean_and_normalize(df):
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=["Al (%)", "Co (%)", "Fe (%)"])
    comp_sum = df[["Al (%)", "Co (%)", "Fe (%)"]].sum(axis=1)
    df["Al_frac"] = df["Al (%)"]/comp_sum
    df["Co_frac"] = df["Co (%)"]/comp_sum
    df["Fe_frac"] = df["Fe (%)"]/comp_sum
    return df

ce = clean_and_normalize(ce)
lp = clean_and_normalize(lp)


# ===========================================================
# 🧭 Geometry for Ternary Plot
# ===========================================================
sqrt3 = np.sqrt(3)
A = np.array([0.5, sqrt3/2]); B = np.array([0.0,0.0]); C = np.array([1.0,0.0])

def get_coords(df):
    xyz = np.vstack([df["Al_frac"].values, df["Co_frac"].values, df["Fe_frac"].values]).T
    coords = xyz[:,0][:,None]*A + xyz[:,1][:,None]*B + xyz[:,2][:,None]*C
    return coords[:,0], coords[:,1]

x_ce, y_ce = get_coords(ce)
x_lp, y_lp = get_coords(lp)


# ===========================================================
# 🧩 Universal Ternary Plot Function
# ===========================================================
def plot_ternary(values, x, y, title, cmap, cbar_label):
    num_points = 300
    xi = np.linspace(0,1,num_points)
    yi = np.linspace(0,np.sqrt(3)/2,num_points)
    Xi, Yi = np.meshgrid(xi, yi)
    mask = (Yi > np.sqrt(3)*np.minimum(Xi, 1 - Xi))
    Xi_masked = np.ma.masked_where(mask, Xi)
    Yi_masked = np.ma.masked_where(mask, Yi)
    interp = griddata((x, y), values, (Xi, Yi), method='cubic')

    fig, ax = plt.subplots(figsize=(9,8))
    tcf = ax.contourf(Xi_masked, Yi_masked, interp, levels=28, cmap=cmap)
    triangle_x = [B[0], C[0], A[0], B[0]]
    triangle_y = [B[1], C[1], A[1], B[1]]
    ax.plot(triangle_x, triangle_y, color="k", lw=1.8)
    ax.text(A[0], A[1]+0.05, "Al fraction", ha="center", va="bottom", fontsize=12)
    ax.text(B[0]-0.04, B[1]-0.03, "Co fraction", ha="right", va="top", fontsize=12)
    ax.text(C[0]+0.04, C[1]-0.03, "Fe fraction", ha="left", va="top", fontsize=12)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
    ax.set_xlim(-0.05,1.05); ax.set_ylim(-0.05,0.95)
    ax.set_title(title, fontsize=14, weight='bold')
    cbar = plt.colorbar(tcf, ax=ax, pad=0.12)
    cbar.set_label(cbar_label)
    ax.scatter(x, y, c='k', s=15)
    plt.tight_layout()
    plt.show()


# ===========================================================
# 🔥 Temperature-Specific Phase Stability Maps
# ===========================================================
fcc_cols = ["200", "400", "650"]
hcp_cols = ["200.1", "400.1", "650.1"]
dhcp_cols = ["200.2", "400.2", "650.2"]
temps = [200, 400, 650]

for i, T in enumerate(temps):
    fcc_col = fcc_cols[i]
    hcp_col = hcp_cols[i]
    dhcp_col = dhcp_cols[i]

    ce["ΔE_HCP_FCC"] = ce[hcp_col] - ce[fcc_col]
    plot_ternary(ce["ΔE_HCP_FCC"], x_ce, y_ce, f"ΔE = E_HCP − E_FCC | T = {T} K", "RdBu_r", "ΔE (eV/atom)")

    ce["ΔE_DHCP_FCC"] = ce[dhcp_col] - ce[fcc_col]
    plot_ternary(ce["ΔE_DHCP_FCC"], x_ce, y_ce, f"ΔE = E_DHCP − E_FCC | T = {T} K", "RdBu_r", "ΔE (eV/atom)")

    ce["ΔE_DHCP_HCP"] = ce[dhcp_col] - ce[hcp_col]
    plot_ternary(ce["ΔE_DHCP_HCP"], x_ce, y_ce, f"ΔE = E_DHCP − E_HCP | T = {T} K", "RdBu_r", "ΔE (eV/atom)")


# ===========================================================
# 🧱 Stacking Fault Energy Maps
# ===========================================================
sf_df = ce[["Al (%)", "Co (%)", "Fe (%)", "ISF", "ESF", "TWIN", "Al_frac", "Co_frac", "Fe_frac"]].copy()
x_sf, y_sf = get_coords(sf_df)

plot_ternary(sf_df["ISF"], x_sf, y_sf, "Intrinsic Stacking Fault Energy (ISF)", "viridis", "ISF (mJ/m²)")
plot_ternary(sf_df["ESF"], x_sf, y_sf, "Extrinsic Stacking Fault Energy (ESF)", "plasma", "ESF (mJ/m²)")
plot_ternary(sf_df["TWIN"], x_sf, y_sf, "Twin Boundary Energy (TWIN)", "cividis", "TWIN (mJ/m²)")


# ===========================================================
# 📐 Lattice Parameter Maps
# ===========================================================
plot_ternary(lp["FCC_avg"], x_lp, y_lp, "FCC Lattice Parameter Map", "coolwarm", "Lattice Parameter (Å)")
plot_ternary(lp["HCP_avg"], x_lp, y_lp, "HCP Lattice Parameter Map", "coolwarm", "Lattice Parameter (Å)")
plot_ternary(lp["DHCP_avg"], x_lp, y_lp, "DHCP Lattice Parameter Map", "coolwarm", "Lattice Parameter (Å)")


# ===========================================================
# 📊 Combine Stacking Fault + Lattice Maps into Subplots
# ===========================================================
def plot_ternary_subplot(values_list, titles, cmaps, cbar_labels, x, y, suptitle):
    sqrt3 = np.sqrt(3)
    A = np.array([0.5, sqrt3/2])
    B = np.array([0.0, 0.0])
    C = np.array([1.0, 0.0])
    triangle_x = [B[0], C[0], A[0], B[0]]
    triangle_y = [B[1], C[1], A[1], B[1]]

    num_points = 300
    xi = np.linspace(0, 1, num_points)
    yi = np.linspace(0, np.sqrt(3)/2, num_points)
    Xi, Yi = np.meshgrid(xi, yi)
    mask = (Yi > np.sqrt(3)*np.minimum(Xi, 1 - Xi))
    Xi_masked = np.ma.masked_where(mask, Xi)
    Yi_masked = np.ma.masked_where(mask, Yi)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for i, ax in enumerate(axes):
        interp = griddata((x, y), values_list[i], (Xi, Yi), method='cubic')
        tcf = ax.contourf(Xi_masked, Yi_masked, interp, levels=28, cmap=cmaps[i])
        ax.plot(triangle_x, triangle_y, color="k", lw=1.5)
        ax.text(A[0], A[1]+0.05, "Al fraction", ha="center", va="bottom", fontsize=10)
        ax.text(B[0]-0.04, B[1]-0.03, "Co fraction", ha="right", va="top", fontsize=10)
        ax.text(C[0]+0.04, C[1]-0.03, "Fe fraction", ha="left", va="top", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
        ax.set_xlim(-0.05,1.05); ax.set_ylim(-0.05,0.95)
        ax.set_title(titles[i], fontsize=12, weight='bold')
        cbar = plt.colorbar(tcf, ax=ax, pad=0.08)
        cbar.set_label(cbar_labels[i])
        ax.scatter(x, y, c='k', s=10)
    plt.suptitle(suptitle, fontsize=15, weight='bold')
    plt.tight_layout()
    plt.show()


# Combined subplot for stacking faults
plot_ternary_subplot(
    [sf_df["ISF"], sf_df["ESF"], sf_df["TWIN"]],
    ["Intrinsic SFE (ISF)", "Extrinsic SFE (ESF)", "Twin Boundary (TWIN)"],
    ["viridis", "plasma", "cividis"],
    ["ISF (mJ/m²)", "ESF (mJ/m²)", "TWIN (mJ/m²)"],
    x_sf, y_sf,
    "Stacking Fault Energy Maps (ISF, ESF, TWIN)"
)

# Combined subplot for lattice parameters
plot_ternary_subplot(
    [lp["FCC_avg"], lp["HCP_avg"], lp["DHCP_avg"]],
    ["FCC Lattice Parameter", "HCP Lattice Parameter", "DHCP Lattice Parameter"],
    ["coolwarm", "coolwarm", "coolwarm"],
    ["a (Å)", "a (Å)", "a (Å)"],
    x_lp, y_lp,
    "Lattice Parameter Maps (FCC, HCP, DHCP)"
)
