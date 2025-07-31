import os
import nibabel as nib
import matplotlib.pyplot as plt

# ============================
# ===== USER CONFIGURATION ===
# ============================

# Base dataset folder (contains imagesTr and imagesTs)
output_split_folder = ''

# Save plots as PNG (set to True to enable)
save_plots = False
save_folder = ''

# ============================
# ===== SCRIPT BEGINS HERE ===
# ============================

def analyze_and_plot_for_folder(folder_path, plot_title, save_name=None):
    spacings_x, spacings_y, spacings_z = [], [], []

    print(f"\nAnalyzing files in: {folder_path}")

    for filename in os.listdir(folder_path):
        if filename.endswith((".nii", ".nii.gz")):
            image_path = os.path.join(folder_path, filename)
            try:
                img = nib.load(image_path)
                zooms = img.header.get_zooms()
                spacings_x.append(zooms[0])
                spacings_y.append(zooms[1])
                spacings_z.append(zooms[2])
            except Exception as e:
                print(f"Could not process {filename}: {e}")

    if not spacings_x:
        print("No valid NIfTI files found.")
        return

    print(f"Processed {len(spacings_x)} images.")
    
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(plot_title, fontsize=16)

    axs[0].hist(spacings_x, bins=20, color='skyblue', edgecolor='black')
    axs[0].set_title('Spacing Distribution (X-axis)')
    axs[0].set_xlabel('Voxel Spacing (mm)')
    axs[0].set_ylabel('Number of Images')

    axs[1].hist(spacings_y, bins=20, color='salmon', edgecolor='black')
    axs[1].set_title('Spacing Distribution (Y-axis)')
    axs[1].set_xlabel('Voxel Spacing (mm)')

    axs[2].hist(spacings_z, bins=20, color='lightgreen', edgecolor='black')
    axs[2].set_title('Spacing Distribution (Z-axis)')
    axs[2].set_xlabel('Voxel Spacing (mm)')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    if save_plots and save_name:
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, save_name)
        plt.savefig(save_path)
        print(f"Plot saved to: {save_path}")

    plt.show()


# Paths for training and testing images
train_images_folder = os.path.join(output_split_folder, 'imagesTr')
test_images_folder = os.path.join(output_split_folder, 'imagesTs')

# --- Run for Training Set ---
if os.path.exists(train_images_folder):
    analyze_and_plot_for_folder(
        train_images_folder,
        'Distribution of Voxel Spacings (Training Set)',
        save_name='train_voxel_spacing.png'
    )
else:
    print(f"Training folder not found at: {train_images_folder}")

# --- Run for Testing Set ---
if os.path.exists(test_images_folder):
    analyze_and_plot_for_folder(
        test_images_folder,
        'Distribution of Voxel Spacings (Testing Set)',
        save_name='test_voxel_spacing.png'
    )
else:
    print(f"Testing folder not found at: {test_images_folder}")
