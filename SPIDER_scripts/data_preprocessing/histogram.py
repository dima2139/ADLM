import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# ============================
# ===== USER CONFIGURATION ===
# ============================

# Path to the folder containing the cleaned/reoriented images
cleaned_folder = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/ALL_modified_renamed_images'

# ============================
# ===== SCRIPT BEGINS HERE ===
# ============================

def plot_voxel_spacing(data_folder):
    spacings_x = []
    spacings_y = []
    spacings_z = []

    print(f"Analyzing files in: {data_folder}")

    # Loop for all files
    for filename in os.listdir(data_folder):
        if filename.endswith((".nii", ".nii.gz")):
            image_path = os.path.join(data_folder, filename)
            try:
                # Load image and its header
                img = nib.load(image_path)
                header = img.header
                
                # Get voxel spacing (zooms)
                zooms = header.get_zooms()
                
                # The zooms tuple contains spacing for (X, Y, Z) axes
                spacings_x.append(zooms[0])
                spacings_y.append(zooms[1])
                spacings_z.append(zooms[2])

            except Exception as e:
                print(f"Could not process {filename}: {e}")

    if not spacings_x:
        print("No valid NIfTI files found or processed.")
        return

    print("\n--- Analysis Complete ---")
    print(f"Processed {len(spacings_x)} images.")
    
    # --- Histograms ---
    
    # Plot figure with 3 subplots
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Distribution of Voxel Spacings Across the Dataset', fontsize=16)

    # Histogram for X-axis spacing
    axs[0].hist(spacings_x, bins=20, color='skyblue', edgecolor='black')
    axs[0].set_title('Spacing Distribution (X-axis)')
    axs[0].set_xlabel('Voxel Spacing (mm)')
    axs[0].set_ylabel('Number of Images')

    # Histogram for Y-axis spacing
    axs[1].hist(spacings_y, bins=20, color='salmon', edgecolor='black')
    axs[1].set_title('Spacing Distribution (Y-axis)')
    axs[1].set_xlabel('Voxel Spacing (mm)')
  

    # Histogram for Z-axis spacing
    axs[2].hist(spacings_z, bins=20, color='lightgreen', edgecolor='black')
    axs[2].set_title('Spacing Distribution (Z-axis)')
    axs[2].set_xlabel('Voxel Spacing (mm)')

    # Improve layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# --- Run the analysis ---
plot_voxel_spacing(cleaned_folder)
