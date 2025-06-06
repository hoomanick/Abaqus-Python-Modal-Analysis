# =================================================================
# SCRIPT: plot_modes.py (Version 2 - Corrected Labels)
# =================================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# --- Configuration ---
output_dir = 'modal_outputs'
modes_to_plot = [6, 32, 83]

print("--- Starting Visualization Script ---")

# --- 1. Plot Natural Frequencies (No Changes) ---
# ... (code is unchanged here) ...
freq_file = os.path.join(output_dir, 'natural_frequencies.txt')
try:
    data = np.loadtxt(freq_file, comments='#', delimiter=',')
    modes = data[:, 0].astype(int)
    frequencies = data[:, 1]
    plt.figure(figsize=(8, 6))
    bars = plt.bar(range(len(modes)), frequencies, color='skyblue', edgecolor='black')
    plt.xlabel('Mode Number', fontsize=12, weight='bold')
    plt.ylabel('Natural Frequency (Hz)', fontsize=12, weight='bold')
    plt.title('Extracted Natural Frequencies of Simply Supported Beam', fontsize=14, weight='bold')
    plt.xticks(range(len(modes)), modes)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f'{yval:.1f}', ha='center', va='bottom')
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'natural_frequencies_plot.png')
    plt.savefig(plot_path, dpi=300)
    plt.show()
except FileNotFoundError:
    print(f"ERROR: Could not find '{freq_file}'.")
except Exception as e:
    print(f"An error occurred while plotting frequencies: {e}")


# --- 2. Plot Mode Shapes ---
print("\nPlotting mode shapes...")
for mode_num in modes_to_plot:
    mode_file = os.path.join(output_dir, f'mode_{mode_num}_shape_data.txt')
    try:
        mode_data = np.loadtxt(mode_file, comments='#', delimiter=',')
        
        # Column 0 is now Z-coordinate (position), Column 1 is Y-displacement
        position = mode_data[:, 0]
        displacements = mode_data[:, 1]
        
        normalized_displacements = displacements / np.max(np.abs(displacements))

        plt.figure(figsize=(10, 4))
        plt.plot(position, normalized_displacements, 'o-', color='navy', markersize=4, linewidth=1.5, label=f'Mode {mode_num}')
        
        # *** CORRECTED X-AXIS LABEL ***
        plt.xlabel('Position along Z-axis (m)', fontsize=12, weight='bold')
        plt.ylabel('Normalized Y-Displacement', fontsize=12, weight='bold')
        plt.title(f'Mode Shape {mode_num}', fontsize=14, weight='bold')
        
        plt.axhline(0, color='black', linestyle='--', linewidth=0.75)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        
        plot_path = os.path.join(output_dir, f'mode_{mode_num}_shape_plot.png')
        plt.savefig(plot_path, dpi=300)
        plt.show()

    except FileNotFoundError:
        print(f"ERROR: Could not find '{mode_file}'.")
    except Exception as e:
        print(f"An error occurred while plotting Mode {mode_num}: {e}")

print("\n--- Visualization Script Finished ---")