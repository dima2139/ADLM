import os
import numpy as np
import nibabel as nib
from panoptica import (
    Panoptica_Aggregator,
    Panoptica_Evaluator,
    InputType,
    ConnectedComponentsInstanceApproximator,
    NaiveThresholdMatching,
)
from panoptica.metrics import Metric

# ============================
#        CONFIGURATION
# ============================

# Path to predictions and ground truths
PRED_DIR = ""
GT_DIR = ""

# Config file & output
PANOPTICA_CONFIG = ""
OUTPUT_TSV = ""

# ============================

# --- Collect valid case IDs ---
case_ids = sorted([
    f.replace(".nii.gz", "")
    for f in os.listdir(GT_DIR)
    if f.endswith(".nii.gz")
])

PAIR = []

for case_id in case_ids:
    pred_path = os.path.join(PRED_DIR, case_id + ".nii.gz")
    gt_path = os.path.join(GT_DIR, case_id + ".nii.gz")

    if not os.path.exists(pred_path):
        print(f"[Warning] Prediction for {case_id} not found, skipping.")
        continue

    # Load NIfTI files
    try:
        pred = nib.load(pred_path).get_fdata().astype(np.uint8)
        gt = nib.load(gt_path).get_fdata().astype(np.uint8)
    except Exception as e:
        print(f"[Error] Failed to load {case_id}: {e}")
        continue

    if pred.shape != gt.shape:
        print(f"[Error] Shape mismatch in {case_id}: pred {pred.shape}, gt {gt.shape}")
        continue

    PAIR.append((pred, gt, case_id))

print(f"✅ Loaded {len(PAIR)} valid prediction-ground truth pairs.")

# --- Run Evaluation using Panoptica Aggregator ---
evaluator = Panoptica_Aggregator(
    Panoptica_Evaluator.load_from_config(PANOPTICA_CONFIG),
    output_file=OUTPUT_TSV
)

print(f"\n🚀 Starting evaluation and writing results to: {OUTPUT_TSV}\n")

for pred, gt, case in PAIR:
    evaluator.evaluate(pred, gt, case)

print("\n✅ Panoptica evaluation complete.")
