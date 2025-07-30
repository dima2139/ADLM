import os
from panoptica import InputType, Panoptica_Evaluator,Panoptica_Aggregator, ConnectedComponentsInstanceApproximator, NaiveThresholdMatching
from panoptica.metrics import Metric
import SimpleITK as sitk
import nibabel as nib
import numpy as np

pred_dir = "/vol/miltank/users/wyou/Documents/resamples/Kits_highres3"     # contains case_00001.nii.gz etc.
gt_dir = "/u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_raw/Dataset221_KiTS2023/labelsTs"     # contains case_00001.nii.gz etc.

# === Collect all case names from the ground truth folder ===
case_ids = sorted([
    f.replace(".nii.gz", "") 
    for f in os.listdir(gt_dir) 
    if f.endswith(".nii.gz")
])

# === Create PAIR ===
PAIR = []

for case_id in case_ids:
    pred_path = os.path.join(pred_dir, case_id + ".nii.gz")
    gt_path = os.path.join(gt_dir, case_id + ".nii.gz")

    if not os.path.exists(pred_path):
        print(f"[Warning] Prediction for {case_id} not found, skipping.")
        continue

    # Load prediction and GT
    pred_img = nib.load(pred_path)
    gt_img = nib.load(gt_path)

    pred = pred_img.get_fdata().astype(np.uint8)
    mask = gt_img.get_fdata().astype(np.uint8)

    # Optional: check shape match
    if pred.shape != mask.shape:
        print(f"[Error] Shape mismatch in {case_id}: pred {pred.shape}, gt {mask.shape}")
        continue

    PAIR.append((pred, mask, case_id))

print(f"Loaded {len(PAIR)} pairs for evaluation.")

evaluator = Panoptica_Aggregator(
    Panoptica_Evaluator.load_from_config("/u/home/wyou/Documents/panoptica/panoptica/configs/panoptica_evaluator_kits23.yaml"),
    output_file = "highres3_model.tsv"
)

for pred, gt, case in PAIR:
    evaluator.evaluate(pred, gt, case)    
