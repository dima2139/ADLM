import os
import nibabel as nib
import matplotlib.pyplot as plt

def analyze_and_plot_for_folder(folder_path, plot_title):
    """
    Analyzes all NIfTI files in a folder and generates a histogram plot
    of their voxel spacings.
    """
    spacings_x, spacings_y, spacings_z = [], [], []

    print(f"\nAnalyzing files in: {folder_path}")

    # Loop through all files and collect spacing data
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
        print("No valid NIfTI files found in this folder.")
        return

    print(f"Processed {len(spacings_x)} images.")
    
    # --- Plotting the Histograms ---
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(plot_title, fontsize=16)

    # Histogram for X-axis
    axs[0].hist(spacings_x, bins=20, color='skyblue', edgecolor='black')
    axs[0].set_title('Spacing Distribution (X-axis)')
    axs[0].set_xlabel('Voxel Spacing (mm)')
    axs[0].set_ylabel('Number of Images')

    # Histogram for Y-axis
    axs[1].hist(spacings_y, bins=20, color='salmon', edgecolor='black')
    axs[1].set_title('Spacing Distribution (Y-axis)')
    axs[1].set_xlabel('Voxel Spacing (mm)')

    # Histogram for Z-axis
    axs[2].hist(spacings_z, bins=20, color='lightgreen', edgecolor='black')
    axs[2].set_title('Spacing Distribution (Z-axis)')
    axs[2].set_xlabel('Voxel Spacing (mm)')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# --- PLEASE UPDATE THESE PATHS ---

# 1. Path to the base folder where you created the split dataset
output_split_folder = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/Dataset077_SPIDER'

# --- Run the analysis for both Train and Test sets ---

# Define paths for the training and testing image folders
train_images_folder = os.path.join(output_split_folder, 'imagesTr')
test_images_folder = os.path.join(output_split_folder, 'imagesTs')

# Generate the plot for the TRAINING set
if os.path.exists(train_images_folder):
    analyze_and_plot_for_folder(
        train_images_folder, 
        'Distribution of Voxel Spacings (Training Set)'
    )
else:
    print(f"Training folder not found at: {train_images_folder}")

# Generate the plot for the TESTING set
if os.path.exists(test_images_folder):
    analyze_and_plot_for_folder(
        test_images_folder, 
        'Distribution of Voxel Spacings (Testing Set)'
    )
else:
    print(f"Testing folder not found at: {test_images_folder}")