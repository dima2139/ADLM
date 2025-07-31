import os
import glob
from tptbox import NII

# --- Configuration ---

# 1. Folder containing your original, native-resolution ground truth label files
GT_NATIVE_FOLDER = "/vol/miltank/users/balann/nnUNetFrame/dataset/nnUNet_raw/Dataset077_SPIDER/labelsTr"

#/vol/miltank/users/balann/nnUNetFrame/dataset/nnUNet_raw/Dataset077_SPIDER/imagesTr

# 2. Folder where the new, resampled ground truth files will be saved
GT_TARGET_FOLDER = "/vol/miltank/users/balann/SPIDER_077_Resampled/Dataset077_R1/labelsTr" # change path

# 3. The target resolution (spacing)
TARGET_SPACING = (3.3, 0.5, 0.5)

# --- Main Script ---

def main():
    """
    Loads ground truth segmentation files, resamples them to a target
    resolution, and saves the results to a new directory.
    """
    print(f"Resampling ground truth labels to target spacing: {TARGET_SPACING}")

    # Create the output directory if it doesn't exist
    os.makedirs(GT_TARGET_FOLDER, exist_ok=True)

    # Find all ground truth Nifti files
    gt_files = sorted(glob.glob(os.path.join(GT_NATIVE_FOLDER, '*.nii.gz')))
    
    if not gt_files:
        print(f"Warning: No .nii.gz files found in {GT_NATIVE_FOLDER}")
        return

    print(f"Found {len(gt_files)} ground truth files to process.")

    # Loop through each file
    for gt_path in gt_files:
        filename = os.path.basename(gt_path)
        print(f"Processing: {filename}")

        # 1. Load the native-resolution ground truth label.
        # It's CRITICAL to use seg=True to ensure nearest-neighbor interpolation.
        gt_nii_native = NII.load(gt_path, seg=True)

        # 2. Resample the label to the target spacing using the .rescale() method
        gt_nii_rescaled = gt_nii_native.rescale(TARGET_SPACING)

        # 3. Define the output path and save the new resampled label
        output_path = os.path.join(GT_TARGET_FOLDER, filename)
        gt_nii_rescaled.save(output_path)
        
        print(f"  > Saved resampled label to: {output_path}")

    print("\n\nGround truth resampling finished for all files!")

if __name__ == '__main__':
    main()
