import os
import shutil
import nibabel as nib
import numpy as np
from sklearn.model_selection import train_test_split
from collections import defaultdict

def verify_split_distribution(data_folder, file_list, set_name):
    """Helper function to print the distribution of spacings in a file list."""
    distribution = defaultdict(int)
    for filename in file_list:
        img_path = os.path.join(data_folder, filename)
        try:
            spacing_x = nib.load(img_path).header.get_zooms()[0]
            # Categorize into the same bins
            if spacing_x < 3.5:
                distribution['~3.3mm group'] += 1
            elif spacing_x < 4.5:
                distribution['~4.0mm group'] += 1
            else:
                distribution['~5.0mm group'] += 1
        except Exception as e:
            print(f"Warning: Could not read {filename} for verification. Error: {e}")
    
    print(f"\n--- {set_name} Distribution ---")
    total = sum(distribution.values())
    # Sort by group name for consistent order
    for group in sorted(distribution.keys()):
        count = distribution[group]
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"  {group}: {count} images ({percentage:.1f}%)")

def create_physical_split_with_verification(
    source_images_folder, 
    source_labels_folder, 
    output_base_folder,
    test_size=0.2, 
    random_state=42
):
    """
    Performs a stratified split, prints a detailed verification report, and
    physically copies images and labels into train and test directories.
    """
    
    # --- 1. Perform the Stratified Split ---
    
    filepaths = []
    spacings = []

    print(f"Analyzing files in: {source_images_folder} to determine strata...")

    for filename in os.listdir(source_images_folder):
        if filename.endswith((".nii", ".nii.gz")):
            image_path = os.path.join(source_images_folder, filename)
            try:
                img = nib.load(image_path)
                spacings.append(img.header.get_zooms()[0])
                filepaths.append(filename)
            except Exception as e:
                print(f"Could not process {filename}: {e}")

    bins = np.digitize(spacings, bins=[3.5, 4.5])
    
    train_filenames, test_filenames, _, _ = train_test_split(
        filepaths, 
        spacings,
        test_size=test_size, 
        random_state=random_state,
        stratify=bins
    )

    # --- 2. Print the Verification Report (as requested) ---

    print("\n--- Split Complete ---")
    print(f"Total images: {len(filepaths)}")
    print(f"Training set size: {len(train_filenames)} images")
    print(f"Testing set size: {len(test_filenames)} images")

    print("\nVerifying stratification...")
    verify_split_distribution(source_images_folder, train_filenames, "Training Set")
    verify_split_distribution(source_images_folder, test_filenames, "Testing Set")

    # --- 3. Create nnUNet style output directories ---

    dir_images_tr = os.path.join(output_base_folder, 'imagesTr')
    dir_labels_tr = os.path.join(output_base_folder, 'labelsTr')
    dir_images_ts = os.path.join(output_base_folder, 'imagesTs')
    dir_labels_ts = os.path.join(output_base_folder, 'labelsTs')

    os.makedirs(dir_images_tr, exist_ok=True)
    os.makedirs(dir_labels_tr, exist_ok=True)
    os.makedirs(dir_images_ts, exist_ok=True)
    os.makedirs(dir_labels_ts, exist_ok=True)
    
    print("\n\nCreating output directories...")
    print(f"- {dir_images_tr}")
    print(f"- {dir_labels_tr}")
    print(f"- {dir_images_ts}")
    print(f"- {dir_labels_ts}")

    # --- 4. Copy files to the new directories ---

    def copy_files(file_list, dest_img_dir, dest_lbl_dir):
        for filename in file_list:
            shutil.copyfile(
                os.path.join(source_images_folder, filename),
                os.path.join(dest_img_dir, filename)
            )
            label_path = os.path.join(source_labels_folder, filename)
            if os.path.exists(label_path):
                 shutil.copyfile(
                    label_path,
                    os.path.join(dest_lbl_dir, filename)
                )
            else:
                print(f"Warning: Label file not found for {filename}")

    print("\nCopying training files...")
    copy_files(train_filenames, dir_images_tr, dir_labels_tr)
    
    print("Copying testing files...")
    copy_files(test_filenames, dir_images_ts, dir_labels_ts)

    print("\n--- Process Complete ---")


# --- PLEASE UPDATE THESE PATHS ---

# 1. Path to your folder with the cleaned T2 images
cleaned_images_folder = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/ALL_modified_renamed_images'

# 2. !! IMPORTANT !! Path to the folder with your corresponding label files
labels_folder = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/ALL_modified_renamed_masks' # <-- VERIFY THIS PATH

# 3. Path to the main output folder where the new directories will be created
output_split_folder = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/Dataset077_SPIDER'


# --- Run the script ---
create_physical_split_with_verification(
    source_images_folder=cleaned_images_folder,
    source_labels_folder=labels_folder,
    output_base_folder=output_split_folder
)