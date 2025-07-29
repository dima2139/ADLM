import os
from panoptica import InputType, Panoptica_Evaluator,Panoptica_Aggregator, ConnectedComponentsInstanceApproximator, NaiveThresholdMatching
from panoptica.metrics import Metric
import SimpleITK as sitk
import nibabel as nib
import numpy as np
# Set your paths
pred_dir = "./eval/output_h2_native_res"
gt_dir = "./eval/mask"


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

#evaluator = Panoptica_Evaluator(
#    expected_input=InputType.MATCHED_INSTANCE,
#    decision_metric=Metric.IOU,
#    decision_threshold=0.5,
#)

#metrics_to_compute = [
#    Metric.DSC,
#    Metric.HD95,
#    Metric.ASSD,
#]

#evaluator = Panoptica_Evaluator(
#    expected_input=InputType.SEMANTIC,
#    instance_approximator=ConnectedComponentsInstanceApproximator(),
    #
#    instance_metrics=metrics_to_compute,
#    instance_matcher=NaiveThresholdMatching(matching_metric=Metric.DSC, matching_threshold=0.1),
#    global_metrics=metrics_to_compute,
#    verbose=True,
#    log_times=True,
#)
evaluator = Panoptica_Aggregator(
    Panoptica_Evaluator.load_from_config("./eval/config_spider.yaml"),
    output_file = "./eval/panoptica_out/results_native_h2.tsv"
)

for pred, gt, case in PAIR:
    evaluator.evaluate(pred, gt, case)    
#evaluator.save_to_config("./../config_spider.yaml")

