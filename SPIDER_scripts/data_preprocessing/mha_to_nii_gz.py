import os
import SimpleITK as sitk
import shutil

input_dir = "C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/T2_masks"
output_labelsTr = "C:/ADLM/Datasets/SPIDER_FULL_FINAL/10159290/T2_masks_nii.gz" # Optional

# Map modality name to nnUNet index
modality_map = {
    "t1": "0000",
    "t2": "0001"
}

os.makedirs(output_labelsTr, exist_ok=True)

# Loop through all .mha files and convert + rename
for file in os.listdir(input_dir):
    if file.endswith(".mha"):
        # Example: 1_t1.mha → 1_0000.nii.gz
        base = file.replace(".mha", "")  # '1_t1'
        case_id_str, modality = base.split("_")  # '1', 't1'
        case_id = f"{int(case_id_str)}"  
        modality_idx = modality_map.get(modality.lower())

        if modality_idx is None:
            print(f"Skipping unknown modality in file: {file}")
            continue

        # Read MHA and convert to NIfTI
        img = sitk.ReadImage(os.path.join(input_dir, file))
        out_path = os.path.join(output_labelsTr, f"{case_id}_{modality_idx}.nii.gz") # change here
        sitk.WriteImage(img, out_path)
        print(f"Converted and saved: {file} -> {case_id}_{modality_idx}.nii.gz")