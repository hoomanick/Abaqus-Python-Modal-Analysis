# =================================================================
# SCRIPT: extract_modal_data.py (Version 8 - Using User-Verified Coordinates)
# PURPOSE: Extracts mode shapes based on a user-defined path.
# =================================================================

from odbAccess import *
import os
import re

# --- Configuration ---
odb_path = 'Job-Beam-Modal.odb'
step_name = 'Step-1-Freq-Analysis'
output_dir = 'modal_outputs'

# --- Setup ---
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
print(f"Opening ODB file: {odb_path}")
odb = openOdb(path=odb_path)

try:
    freq_step = odb.steps[step_name]
    print(f"Successfully accessed Step: '{step_name}'")

    # --- Frequency Extraction (No Changes) ---
    frequencies_data = []
    for frame in freq_step.frames:
        description = frame.description
        if 'Mode' in description and 'Freq' in description:
            mode_match = re.search(r'Mode\s+(\d+)', description)
            freq_match = re.search(r'Freq\s*=\s*([\d.E+-]+)', description)
            if mode_match and freq_match:
                mode_num = int(mode_match.group(1))
                frequency = float(freq_match.group(1))
                frequencies_data.append((mode_num, frequency))
    freq_file_path = os.path.join(output_dir, 'natural_frequencies.txt')
    with open(freq_file_path, 'w') as f:
        f.write("# Mode, Frequency\n")
        for mode, freq in frequencies_data:
            f.write(f"{mode}, {freq:.6f}\n")
    print(f"\nSuccessfully extracted and saved {len(frequencies_data)} natural frequencies.")

    # --- Mode Shape Extraction ---
    print("\nExtracting mode shapes...")
    instance = odb.rootAssembly.instances.values()[0]
    print(f"Accessing nodes from instance: '{instance.name}'")

    for frame in freq_step.frames:
        if 'Mode' in frame.description:
            mode_num = int(re.search(r'Mode\s+(\d+)', frame.description).group(1))
            print(f"  Processing Mode {mode_num}...")
            
            displacement_field = frame.fieldOutputs['UT']
            mode_shape_data = []
            
            # *** DEFINITIVE FILTER USING YOUR VERIFIED COORDINATES ***
            target_x = 0.040          # The web face plane you identified.
            target_y = 0.0775185      # The real Y-coordinate you found.
            tolerance = 1e-5          # We can use a tight tolerance.

            for vp in displacement_field.values:
                node_label = vp.nodeLabel
                node = instance.getNodeFromLabel(node_label)
                x_coord, y_coord, z_coord = node.coordinates
                
                # Apply the filter using the exact coordinates you found
                if abs(x_coord - target_x) < tolerance and abs(y_coord - target_y) < tolerance:
                    position = z_coord
                    displacement_component = vp.data[1] # U2 (Y-displacement)
                    mode_shape_data.append((position, displacement_component))

            if not mode_shape_data:
                print(f"    WARNING: Still no nodes found for Mode {mode_num}.")
                continue

            mode_shape_data.sort(key=lambda item: item[0])

            mode_file_path = os.path.join(output_dir, f'mode_{mode_num}_shape_data.txt')
            with open(mode_file_path, 'w') as f:
                f.write("# Z-Coordinate, Y-Displacement\n")
                for pos, disp in mode_shape_data:
                    f.write(f"{pos:.6e}, {disp:.6e}\n")
            print(f"    --> Found {len(mode_shape_data)} nodes. Saved to {mode_file_path}")

finally:
    odb.close()
    print("\nExtraction complete. ODB file closed.")