import os
import glob
import csv
from TPTBox import NII

# === CONFIGURATION ===
ORIGINAL_FOLDER = "/vol/miltank/users/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_raw/Dataset221_KiTS2023/imagesTs"
PRED_FOLDER = "/vol/miltank/users/wyou/Documents/results/Kits2023/all_highres0_5_model/inference_output"
OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/new"
CSV_LOG = os.path.join(OUTPUT_FOLDER, "spacing_change_log.csv")

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Gather prediction files
pred_files = sorted(glob.glob(os.path.join(PRED_FOLDER, "*.nii.gz")))
print(f"Found {len(pred_files)} prediction files to process.\n")

# Prepare CSV log
with open(CSV_LOG, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["case", "original_spacing", "predicted_spacing", "ratio_z", "ratio_y", "ratio_x"])

    # Process each file
    for pred_path in pred_files:
        filename = os.path.basename(pred_path)
        base = os.path.splitext(os.path.splitext(filename)[0])[0]
        original_filename = base + "_0000.nii.gz"
        original_path = os.path.join(ORIGINAL_FOLDER, original_filename)

        if not os.path.exists(original_path):
            print(f"Original image not found, skipping: {filename}")
            continue

        print(f"Resampling prediction: {filename}")
        
        try:
            # Load images
            nii_orig = NII.load(original_path, seg=False)
            nii_pred_target = NII.load(pred_path, seg=True)

            # Get spacing info
            spacing_orig = nii_orig.spacing
            spacing_pred = nii_pred_target.spacing

            # Compute spacing ratios
            ratio = tuple(round(o / p, 4) for o, p in zip(spacing_orig, spacing_pred))

            # Resample
            nii_pred_native = nii_pred_target.resample_from_to(nii_orig)

            # Save resampled prediction
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            nii_pred_native.save(output_path)
            print(f"Saved resampled prediction to: {output_path}\n")

            # Log info
            writer.writerow([
                filename,
                spacing_orig,
                spacing_pred,
                ratio[0], ratio[1], ratio[2]
            ])

        except Exception as e:
            print(f"Failed to process: {filename}")
            print(e)

print("All predictions successfully resampled and saved in:", OUTPUT_FOLDER)
print("Spacing change log saved to:", CSV_LOG)
