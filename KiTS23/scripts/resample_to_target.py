import os
import glob
from TPTBox import NII

def resample_dataset(input_folder, target_spacing, seg=True):
    # Check and construct the output folder path
    if "nnUNet_raw" not in input_folder:
        raise ValueError("Expected 'nnUNet_raw' in the input folder path to compute output path.")

    output_folder = input_folder.replace("nnUNet_raw", "nnUNet_raw_resampled")
    output_folder = os.path.normpath(output_folder)
    print("Resolved output path:", output_folder)

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all NIfTI files in the input folder
    nii_files = sorted(glob.glob(os.path.join(input_folder, "*.nii.gz")))
    print(f"Found {len(nii_files)} images to resample to spacing {target_spacing}\n")

    for img_path in nii_files:
        filename = os.path.basename(img_path)
        try:
            # Load NIfTI with appropriate segmentation flag
            nii = NII.load(img_path, seg=seg)
            print(f"{filename}: original spacing = {nii.spacing}")

            # Resample image
            nii_rescaled = nii.rescale(target_spacing)

            # Save to output path
            output_path = os.path.normpath(os.path.join(output_folder, filename))
            nii_rescaled.save(output_path)
            print(f"Saved resampled image to: {output_path}\n")

        except Exception as e:
            print(f"Failed to resample: {filename}")
            print(e)

    print("All images resampled and saved to:", output_folder)

