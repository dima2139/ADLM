import os
import shutil
import nibabel as nib
import numpy as np
from sklearn.model_selection import train_test_split
from collections import defaultdict

# ==============================
#      USER CONFIGURATION
# ==============================

# 1. Folder with cleaned T2 images
cleaned_images_folder = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/ALL_modified_renamed_images'

# 2. Folder with masks (labels)
labels_folder = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/ALL_modified_renamed_masks'

# 3. Output folder where nnUNet format will be created
output_split_folder = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/Dataset077_SPIDER'

# ==============================


def verify_split_distribution(data_folder, file_list, set_name):
    """Prints spacing group distribution for verification."""
    distribution = defaultdict(int)
    for filename in file_list:
        img_path = os.path.join(data_folder, filename)
        try:
            spacing_x = nib.load(img_path).header.get_zooms()[0]
            if spacing_x < 3.5:
                distribution['~3.3mm group'] += 1
            elif spacing_x < 4.5:
                distribution['~4.0mm group'] += 1
            else:
                distribution['~5.0mm group'] += 1
        except Exception as e:
            print(f"⚠️ Could not read {filename}: {e}")
    
    print(f"\n📊 {set_name} Distribution:")
    total = sum(distribution.values())
    for group in sorted(distribution):
        count = distribution[group]
        print(f"  {group:<16} : {count:>3} images ({(count / total * 100):.1f}%)")


def create_physical_split_with_verification(
    source_images_folder,
    source_labels_folder,
    output_base_folder,
    test_size=0.2,
    random_state=42
):
    # --- Step 1: Load & Bin ---
    filepaths, spacings = [], []

    print(f"\n📁 Analyzing images in: {source_images_folder}")
    for filename in sorted(os.listdir(source_images_folder)):
        if filename.endswith((".nii", ".nii.gz")):
            image_path = os.path.join(source_images_folder, filename)
            try:
                img = nib.load(image_path)
                spacings.append(img.header.get_zooms()[0])
                filepaths.append(filename)
            except Exception as e:
                print(f"❌ Could not load {filename}: {e}")

    bins = np.digitize(spacings, bins=[3.5, 4.5])

    train_filenames, test_filenames, _, _ = train_test_split(
        filepaths,
        spacings,
        test_size=test_size,
        random_state=random_state,
        stratify=bins
    )

    print("\n✅ Stratified Split Complete")
    print(f"🔹 Total  : {len(filepaths)} images")
    print(f"🔸 Train  : {len(train_filenames)} images")
    print(f"🔸 Test   : {len(test_filenames)} images")

    # --- Step 2: Verify Distribution ---
    verify_split_distribution(source_images_folder, train_filenames, "Training Set")
    verify_split_distribution(source_images_folder, test_filenames, "Testing Set")

    # --- Step 3: Prepare Output Directories ---
    dir_images_tr = os.path.join(output_base_folder, 'imagesTr')
    dir_labels_tr = os.path.join(output_base_folder, 'labelsTr')
    dir_images_ts = os.path.join(output_base_folder, 'imagesTs')
    dir_labels_ts = os.path.join(output_base_folder, 'labelsTs')

    os.makedirs(dir_images_tr, exist_ok=True)
    os.makedirs(dir_labels_tr, exist_ok=True)
    os.makedirs(dir_images_ts, exist_ok=True)
    os.makedirs(dir_labels_ts, exist_ok=True)

    print("\n📦 Creating output directories:")
    print(f" - {dir_images_tr}")
    print(f" - {dir_labels_tr}")
    print(f" - {dir_images_ts}")
    print(f" - {dir_labels_ts}")

    # --- Step 4: Copy Data ---
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
                print(f"⚠️ Label missing for: {filename}")

    print("\n📤 Copying files...")
    copy_files(train_filenames, dir_images_tr, dir_labels_tr)
    copy_files(test_filenames, dir_images_ts, dir_labels_ts)

    print("\n🎉 Done! Dataset is ready for nnUNet.")
    print(f"🧪 Test files: {len(test_filenames)} | 🏋️ Train files: {len(train_filenames)}")


# === Run the Split ===
create_physical_split_with_verification(
    source_images_folder=cleaned_images_folder,
    source_labels_folder=labels_folder,
    output_base_folder=output_split_folder
)
