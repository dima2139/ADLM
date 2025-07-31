import os
import shutil

# --- Configuration ---
images_folder = ''  # <--- IMPORTANT: Change this to your actual image folder path
masks_folder = ''    # <--- IMPORTANT: Change this to your actual mask folder path
start_new_prefix = 501 # This will be the starting number for the '901', '902', etc. sequence

# --- Function to extract base name and extension ---
def split_filename(filename):
    base_name = os.path.basename(filename)
    name_without_ext, ext = os.path.splitext(base_name)
    if name_without_ext.endswith('.nii'): # Handle .nii.gz
        name_without_ext, nifti_ext = os.path.splitext(name_without_ext)
        ext = nifti_ext + ext
    return name_without_ext, ext

# --- Main Renaming Logic ---
def rename_files_v2(images_folder, masks_folder, start_new_prefix):
    image_files = sorted([f for f in os.listdir(images_folder) if f.endswith('.nii.gz')])
    mask_files = sorted([f for f in os.listdir(masks_folder) if f.endswith('.nii.gz')])

    # Create dictionaries for faster lookup
    images_map = {split_filename(f)[0]: f for f in image_files}
    masks_map = {split_filename(f)[0]: f for f in mask_files}

    # Extract and sort unique original prefixes (e.g., 107, 110, 118)
    original_prefixes = sorted(list(set(split_filename(f)[0].split('_')[0] for f in image_files)))

    # Map original prefixes to new sequential prefixes (e.g., 107 -> 901, 110 -> 902)
    prefix_mapping = {}
    current_new_prefix = start_new_prefix
    for original_prefix in original_prefixes:
        prefix_mapping[original_prefix] = current_new_prefix
        current_new_prefix += 1

    renamed_count = 0

    print(f"Starting file renaming process (Version 2)...")
    print(f"Original Prefix Mappings: {prefix_mapping}")

    # Process files based on their original prefix, then suffix
    for original_prefix in sorted(prefix_mapping.keys()):
        new_prefix = prefix_mapping[original_prefix]
        new_suffix_counter = 1 # Reset suffix for each new prefix

        # Find all files belonging to this original_prefix
        files_for_this_prefix = sorted([
            base_name for base_name in images_map.keys()
            if base_name.startswith(f"{original_prefix}_")
        ])

        for old_base_name in files_for_this_prefix:
            if old_base_name in masks_map:
                old_image_full_path = os.path.join(images_folder, images_map[old_base_name])
                old_mask_full_path = os.path.join(masks_folder, masks_map[old_base_name])

                # Generate new filename parts
                new_prefix_str = str(new_prefix)
                new_suffix_str = f"{new_suffix_counter:04d}" # Formats to 0001, 0002, etc.

                new_base_name = f"{new_prefix_str}_{new_suffix_str}"
                
                # Get the original extension (e.g., .nii.gz)
                _, ext = split_filename(images_map[old_base_name])

                new_image_full_path = os.path.join(images_folder, new_base_name + ext)
                new_mask_full_path = os.path.join(masks_folder, new_base_name + ext)

                try:
                    # Rename image
                    shutil.move(old_image_full_path, new_image_full_path)
                    print(f"Renamed image: {os.path.basename(old_image_full_path)} -> {os.path.basename(new_image_full_path)}")

                    # Rename mask
                    shutil.move(old_mask_full_path, new_mask_full_path)
                    print(f"Renamed mask:  {os.path.basename(old_mask_full_path)} -> {os.path.basename(new_mask_full_path)}")
                    
                    new_suffix_counter += 1
                    renamed_count += 1

                except Exception as e:
                    print(f"Error renaming files for base name {old_base_name}: {e}")
            else:
                print(f"Warning: No corresponding mask found for image: {images_map[old_base_name]} (Skipping)")

    print(f"\nFinished renaming. Renamed {renamed_count} pairs of files.")

# --- Run the renaming function ---
if __name__ == "__main__":
    # !!! IMPORTANT: Before running, uncomment the line below and replace with your actual paths.
    # Be very careful and test on a copy of your data first!
    rename_files_v2(images_folder, masks_folder, start_new_prefix)
    print("WARNING: The renaming function is commented out by default. Please read the script, set your paths, and uncomment 'rename_files_v2(...)' to run.")
    print("It is highly recommended to test this script on a *copy* of your data first to prevent accidental data loss.")