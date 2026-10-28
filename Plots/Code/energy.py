import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpltern
import os

# === Load Excel sheet ===
file_path = r"C:\Users\ommka\OneDrive\Desktop\Vamsi Assignment\GRaphs\Energies\Assignment 2 Rough.xlsx"
save_dir = os.path.dirname(file_path)
df = pd.read_excel(file_path, sheet_name="Total Energies", header=None)

# === Find temperature blocks ===
temperatures = {}
for i, row in df.iterrows():
    if isinstance(row[5], str) and "Temperature:" in row[5]:
        temp_str = row[5].split(":")[1].strip()
        temperatures[temp_str] = i

print("Detected temperature sections:", list(temperatures.keys()))

# === Iterate over each temperature block ===
for temp, start_row in temperatures.items():
    data_start = start_row + 2
    next_temps = [r for r in temperatures.values() if r > start_row]
    data_end = min(next_temps, default=len(df)) - 1

    block = df.iloc[data_start:data_end, :14].dropna(how='all')
    block.columns = df.iloc[start_row + 1, :14].values

    for col in block.columns:
        try:
            block[col] = pd.to_numeric(block[col])
        except Exception:
            pass

    # Extract composition and energy columns
    t = block["Al (%)"].astype(float).values / 100
    l = block["Co (%)"].astype(float).values / 100
    r = block["Fe (%)"].astype(float).values / 100
    gamma_isf = block["γISF​"].astype(float).values
    gamma_esf = block["γESF​"].astype(float).values
    gamma_twin = block["γTwin​"].astype(float).values

    total = t + l + r
    if not np.allclose(total, 1):
        t /= total
        l /= total
        r /= total

    # === Plot ternary contour maps ===
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), subplot_kw=dict(projection='ternary'))
    props = [
        ("γISF (J/m²)", gamma_isf),
        ("γESF (J/m²)", gamma_esf),
        ("γTwin (J/m²)", gamma_twin)
    ]

    for ax, (label, vals) in zip(axes, props):
        vmin, vmax = np.nanmin(vals), np.nanmax(vals)
        levels = np.linspace(vmin, vmax, 8)
        cs = ax.tricontourf(t, l, r, vals, levels=levels, cmap='viridis')

        # === Axis labels along edges ===
        ax.taxis.set_label_text("Al", fontsize=12)
        ax.laxis.set_label_text("Co", fontsize=12)
        ax.raxis.set_label_text("Fe", fontsize=12)

        # Move labels from corners to edges (center)
        ax.taxis.set_label_position("tick1")
        ax.laxis.set_label_position("tick1")
        ax.raxis.set_label_position("tick1")

        # Center alignment along edges
        ax.taxis.label.set_horizontalalignment('center')
        ax.laxis.label.set_horizontalalignment('center')
        ax.raxis.label.set_horizontalalignment('center')

        # Set axis spine (triangle edge) colors
        for spine in ax.spines.values():
            spine.set_color("black")
            spine.set_linewidth(1.2)

        # Grid and tick formatting
        ax.tick_params(labelsize=9)
        ax.grid(True, color='gray', alpha=0.4)

        ax.set_title(f"{label} at {temp}", fontsize=12)
        cax = ax.inset_axes([1.05, 0.1, 0.05, 0.8], transform=ax.transAxes)
        cbar = fig.colorbar(cs, cax=cax)
        cbar.set_label(label, rotation=270, va='baseline')

    plt.suptitle(f"Stacking Fault Energies (J/m²) at {temp}", fontsize=14)
    plt.tight_layout()

    save_path = os.path.join(save_dir, f"SFE_{temp.replace(' ', '_')}.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved plot: {save_path}")

    plt.close(fig)

print("🎉 All ternary plots generated successfully with edge-centered axis labels (J/m²)!")

