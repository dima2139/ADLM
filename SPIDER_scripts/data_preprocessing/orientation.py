import nibabel as nib
import os
import shutil

# ============================
# ===== USER CONFIGURATION ===
# ============================

# Folder with original T2 images (.nii or .nii.gz)
original_data_folder = 'dataset/nnUNet_raw/'

# Folder to save reoriented images
cleaned_data_folder = ''

# Target orientation as a tuple (e.g., ('L', 'P', 'S'))
target_orientation_tuple = ('L', 'P', 'S')

# ============================
# ===== CHECK ORIENTATIONS ===
# ============================

def check_all_orientations(data_folder):
    """
    Checks the orientation of all .nii.gz files in a folder.
    """
    orientations = {}
    for filename in os.listdir(data_folder):
        if filename.endswith(".nii.gz"):
            image_path = os.path.join(data_folder, filename)
            try:
                img = nib.load(image_path)
                orientation = ''.join(nib.aff2axcodes(img.affine))  # Join tuple to string for easy counting
                if orientation not in orientations:
                    orientations[orientation] = 0
                orientations[orientation] += 1
            except Exception as e:
                print(f"Could not process {filename}: {e}")

    print("--- Orientation Summary ---")
    for orientation, count in orientations.items():
        print(f"Orientation: {orientation}, Count: {count}")

# Check orientations in original folder
check_all_orientations(original_data_folder)

# ============================
# ===== PROCESS IMAGES =======
# ============================

# Create output directory
os.makedirs(cleaned_data_folder, exist_ok=True)
print(f"Cleaned data will be saved in: {cleaned_data_folder}")

# Get all nii or nii.gz files
all_files = [f for f in os.listdir(original_data_folder) if f.endswith(('.nii', '.nii.gz'))]

for filename in all_files:
    input_path = os.path.join(original_data_folder, filename)
    output_path = os.path.join(cleaned_data_folder, filename)

    try:
        img = nib.load(input_path)
        current_orientation_tuple = nib.aff2axcodes(img.affine)

        if current_orientation_tuple == target_orientation_tuple:
            print(f"'{filename}' is already {target_orientation_tuple}. Copying...")
            shutil.copyfile(input_path, output_path)
        else:
            print(f"'{filename}' is {current_orientation_tuple}. Reorienting to {target_orientation_tuple}...")
            target_orientation_obj = nib.orientations.axcodes2ornt(target_orientation_tuple)
            current_orientation_obj = nib.orientations.axcodes2ornt(current_orientation_tuple)
            transform = nib.orientations.ornt_transform(current_orientation_obj, target_orientation_obj)

            reoriented_img_data = nib.orientations.apply_orientation(img.get_fdata(), transform)
            new_affine = img.affine.dot(nib.orientations.inv_ornt_aff(transform, img.shape))
            new_img = nib.Nifti1Image(reoriented_img_data, new_affine)

            nib.save(new_img, output_path)

    except Exception as e:
        print(f"ERROR processing '{filename}': {e}")

print("\n--- Processing Complete ---")
print(f"All images have been processed and saved in '{cleaned_data_folder}'.")

# ============================
# === VERIFY FINAL RESULTS ===
# ============================

# Check orientations in cleaned folder
check_all_orientations(cleaned_data_folder)
