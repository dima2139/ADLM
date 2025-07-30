import os
import glob
from TPTBox import NII

# === CONFIGURATION ===
#INPUT_FOLDER = "/vol/miltank/users/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_raw/Dataset221_KiTS2023/imagesTs"
INPUT_FOLDER = "/vol/miltank/users/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_raw/Dataset221_KiTS2023/labelsTs"

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_1"
#TARGET_SPACING = (3.0, 0.8, 0.8)  # z, y, x (or however TPTBox defines it)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_2"
#TARGET_SPACING = (2.25, 0.7, 0.7)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_3"
#TARGET_SPACING = (1.5, 0.6, 0.6)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_4"
#TARGET_SPACING = (1.25, 0.5, 0.5)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_5"
#TARGET_SPACING = (1.0, 0.4, 0.4)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_6"
#TARGET_SPACING = (0.8, 0.8, 0.8)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_7"
#TARGET_SPACING = (0.64, 0.64, 0.64)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_8"
#TARGET_SPACING = (0.53, 0.53, 0.53)

OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_9"
TARGET_SPACING = (1.06, 1.06, 1.06)  # z, y, x (or however TPTBox defines it)

OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_10"
TARGET_SPACING = (1.6, 1.6, 1.6)  # z, y, x (or however TPTBox defines it)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_images_model_8"
#TARGET_SPACING = (3.0, 0.8, 0.8)  # z, y, x (or however TPTBox defines it)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_2"
#TARGET_SPACING = (2.25, 0.7, 0.7)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_3"
#TARGET_SPACING = (1.5, 0.6, 0.6)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_4"
#TARGET_SPACING = (1.25, 0.5, 0.5)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_5"
#TARGET_SPACING = (1.0, 0.4, 0.4)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_6"
#TARGET_SPACING = (0.8, 0.8, 0.8)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_7"
#TARGET_SPACING = (0.64, 0.64, 0.64)

#OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_8"
#TARGET_SPACING = (0.53, 0.53, 0.53)

OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_9"
TARGET_SPACING = (1.06, 1.06, 1.06)  # z, y, x (or however TPTBox defines it)

OUTPUT_FOLDER = "/vol/miltank/users/wyou/Documents/target_labels_model_10"
TARGET_SPACING = (1.6, 1.6, 1.6)  # z, y, x (or however TPTBox defines it)

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Get list of all .nii.gz files
nii_files = sorted(glob.glob(os.path.join(INPUT_FOLDER, "*.nii.gz")))
print(f"Found {len(nii_files)} images to resample to spacing {TARGET_SPACING}\n")

for img_path in nii_files:
    filename = os.path.basename(img_path)

    try:
        # Load the image
        #nii = NII.load(img_path, seg=False)
        nii = NII.load(img_path, seg=True)# seg=False for image, seg=True for label/mask

        # Print original spacing
        original_spacing = nii.spacing
        print(f"{filename}: original spacing = {original_spacing}")

        # Resample to target spacing
        nii_rescaled = nii.rescale(TARGET_SPACING)

        # Save result
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        nii_rescaled.save(output_path)

        print(f"Saved resampled image to: {output_path}\n")

    except Exception as e:
        print(f"Failed to resample: {filename}")
        print(e)

print("All images resampled and saved to:", OUTPUT_FOLDER)
