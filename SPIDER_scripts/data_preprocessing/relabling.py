import numpy as np
import SimpleITK as sitk
import os

# Define the input and output directories
input_labels_dir = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/T2SPACE_masks_reoriented'
output_labels_dir = 'C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/T2SPACE_masks_reoriented_relabeled'

# Create the output directory if it doesn't exist
os.makedirs(output_labels_dir, exist_ok=True)

def relabel_spider_mask(input_path, output_path):
    # Load the image
    image = sitk.ReadImage(input_path)
    mask = sitk.GetArrayFromImage(image)

    # Create a new mask with the same shape, initialized to 0 (background)
    new_mask = np.zeros_like(mask, dtype=np.uint8)

    # Apply the new labeling scheme
    # Vertebrae (original values 1-25 and 101-125) -> new value 1
    new_mask[(mask >= 1) & (mask <= 25)] = 1
    new_mask[(mask >= 101) & (mask <= 125)] = 1

    # Spinal Canal (original value 100) -> new value 2
    new_mask[mask == 100] = 2

    # Intervertebral Discs (original values 201-225) -> new value 3
    new_mask[(mask >= 201) & (mask <= 225)] = 3

    # Create a new SimpleITK image from the relabeled numpy array
    new_image = sitk.GetImageFromArray(new_mask)
    new_image.CopyInformation(image)  # Preserve metadata like spacing and origin

    # Save the new label file
    sitk.WriteImage(new_image, output_path)

# Iterate over all label files in the input directory
for filename in os.listdir(input_labels_dir):
    if filename.endswith(('.nii.gz', '.png', '.mha')): # Adjust for your file format
        input_path = os.path.join(input_labels_dir, filename)
        output_path = os.path.join(output_labels_dir, filename)
        relabel_spider_mask(input_path, output_path)

print("Relabeling complete.")