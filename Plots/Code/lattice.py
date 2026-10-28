import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpltern

# Path to your Excel file
file_path = r"C:\Users\ommka\OneDrive\Desktop\Vamsi Assignment\GRaphs\Lattice Parameters\Lattice Parameters.xlsx"

# Load the sheet
df = pd.read_excel(file_path, sheet_name="Total Energies", header=None)

# Extract relevant columns
# Columns: Al (%), Co (%), Fe (%), Lattice parameter (200°C, 400°C, 650°C)
data = df.iloc[2:, [1, 2, 3, 5, 6, 7]]
data.columns = ["Al", "Co", "Fe", "200°C", "400°C", "650°C"]

# Convert numeric columns
for col in ["Al", "Co", "Fe", "200°C", "400°C", "650°C"]:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Remove missing rows
data = data.dropna()

# Ternary plots for each temperature
temps = ["200°C", "400°C", "650°C"]
fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw=dict(projection='ternary'))
fig.subplots_adjust(wspace=0.3)

for ax, temp in zip(axes, temps):
    t = data["Al"] / 100
    l = data["Co"] / 100
    r = data["Fe"] / 100
    v = data[temp]

    # tricontourf plot
    cs = ax.tricontourf(t, l, r, v, levels=10, cmap='viridis')
    ax.set_tlabel("Al (%)")
    ax.set_llabel("Co (%)")
    ax.set_rlabel("Fe (%)")
    ax.set_title(f"Lattice Parameter at {temp}")
    cax = ax.inset_axes([1.05, 0.1, 0.05, 0.8], transform=ax.transAxes)
    colorbar = fig.colorbar(cs, cax=cax)
    colorbar.set_label("Lattice Parameter (Å)", rotation=270, va='baseline')

plt.tight_layout()
plt.show()
