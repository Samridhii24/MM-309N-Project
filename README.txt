====================================================================
README — Assignment 2: Mini Project
====================================================================
Course: MM309N – Computational Methods for Materials  
Instructor: Dr. Venkata Vamsi Koruprolu  
Student: Samridhi  
Group: 2 — Al–Co–Fe System  
Department of MEMS, IIT Indore  
Date of Submission: 4th November 2025
====================================================================

PROJECT TITLE:
Effect of Alloying and Temperature on Fault Energies in Al–Co–Fe System

--------------------------------------------------------------------
1. OBJECTIVE
--------------------------------------------------------------------
The objective of this assignment is to study the influence of alloying (Al, Co, Fe) and temperature (200 K, 400 K, 650 K) on lattice parameters, cohesive energies, and stacking fault energies (SFEs) using atomistic simulations.

The project compares results from two theoretical models:
• DMLF (Diffuse Multi-Layer Fault Model)
• ANNNI (Axial Next-Nearest Neighbor Ising Model)

--------------------------------------------------------------------
2. SIMULATION OVERVIEW
--------------------------------------------------------------------
• Simulation Engine: LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator)
• Potential Type: Embedded Atom Method (EAM) potential from NIST repository
• Structures Simulated: FCC, HCP, and DHCP
• Temperatures Studied: 200 K, 400 K, 650 K
• Ensemble: NPT (constant number of atoms, pressure, and temperature)
• Timestep: 1 fs
• Simulation Duration: 100 ps per configuration
• Relaxation Method: Conjugate Gradient + NPT equilibration
• Visualization Tool: OVITO
• Post-Processing: Python (matplotlib, mpltern)

--------------------------------------------------------------------
3. FILE STRUCTURE
--------------------------------------------------------------------
Assignment-2_Samridhi_Group-2/
│
├── Report.pdf                       → Final report generated via LaTeX
│
├── Code/                            → Python scripts used for data processing and plotting
│   ├── all_codes.py                 → Complete analysis script (end-to-end execution)
│   ├── energy.py                    → Generates cohesive energy and SFE plots
│   └── lattice.py                   → Plots lattice parameter variation with composition
│
├── Figures/                         → All figures and visualizations used in the report
│   ├── Fig-1_Benchmarking.jpg
│   ├── Fig-2(a)_fcc_front.png
│   ├── Fig-2(b)_hcp_front.png
│   ├── Fig-2(c)_dhcp_front.png
│   ├── Fig-3(a)_SFE_200K.png
│   ├── Fig-3(b)_SFE_400K.png
│   ├── Fig-3(c)_SFE_650K.png
│   ├── Fig-4(a)_ESF_DMLF_vs_ANNNI.png
│   ├── Fig-4(b)_ISF_DMLF_vs_ANNNI.png
│   ├── Fig-4_DMLF_vs_ANNNI_at_diff_compositions_and_temp.png
│   ├── Fig-5_Phase_Stabilities_btw_diff_phases_at_diff_temp.png
│   ├── Twin_DMLF_vs_ANNNI.png
│   └── Variation_of_Lattice_Parameter_with_composition.png
│
├── MEAM File/                       → Interatomic potential files used in LAMMPS
│   ├── AlCoFe.meam
│   └── library.meam
│
├── Simulation_FCC/                  → FCC structure input and results
│   ├── com1 ... com21               → Input composition data files
│   ├── AlCoFe                       → MEAM potential reference
│   └── library                      → MEAM library reference
│
├── Simulation_HCP/                  → HCP structure input and results
│   ├── com1 ... com21
│   ├── AlCoFe
│   └── library
│
├── Simulation_DHCP/                 → DHCP structure input and results
│   ├── com1 ... com21
│   ├── AlCoFe
│   └── library
│
├── Tables/                          → Processed tabular data and computed results
│   ├── Table-1_Cohesive_Energy_and_Lattice_Parameter.pdf
│   ├── Table-2_SFE_DMLF.pdf
│   └── Table-3_SFE_ANNNI.pdf
│
└── README.txt                       → (This file)

--------------------------------------------------------------------
4. WORKFLOW DESCRIPTION
--------------------------------------------------------------------
Step 1: Structure Preparation  
    • Built FCC, HCP, and DHCP supercells using literature lattice parameters.  
    • Randomly distributed Al–Co–Fe atoms across lattice sites to simulate the ternary system.  

Step 2: Energy Minimization and Equilibration  
    • Energy minimization performed using the conjugate gradient algorithm.  
    • Each structure equilibrated under NPT ensemble at 200 K, 400 K, and 650 K.  
    • System relaxed to zero pressure with stable energy convergence.  

Step 3: Data Extraction  
    • Extracted cohesive energy, lattice constant, and temperature-pressure data.  
    • Averaged over last 20 ps of equilibrium phase.  

Step 4: SFE Computation  
    • Used DMLF model equations for γISF, γESF, and γTwin.  
    • Compared with ANNNI model predictions for each temperature.  

Step 5: Post-Processing and Visualization  
    • Processed LAMMPS output data using Python (`energy.py`, `lattice.py`).  
    • Generated ternary maps and comparison plots using `mpltern` and `matplotlib`.  
    • Visualized atomic structures using OVITO.  

Step 6: Report Compilation  
    • Results compiled and formatted in LaTeX using Overleaf (Report.tex).  

--------------------------------------------------------------------
5. OUTPUTS AND INTERPRETATION
--------------------------------------------------------------------
• Al-rich alloys: higher lattice parameters, lower SFEs.  
• Fe- and Co-rich alloys: stronger bonding, higher SFEs.  
• Increasing temperature stabilizes FCC stacking by increasing γISF.  
• DMLF and ANNNI models converge at 650 K → thermal phase stabilization.

--------------------------------------------------------------------
6. HOW TO REPRODUCE RESULTS
--------------------------------------------------------------------
1. Open LAMMPS input files under `Simulation_FCC/`, `Simulation_HCP/`, and `Simulation_DHCP/`.  
2. Run simulations using:
