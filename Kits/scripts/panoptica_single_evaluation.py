import os
from panoptica import InputType, Panoptica_Evaluator, ConnectedComponentsInstanceApproximator, NaiveThresholdMatching
from panoptica.metrics import Metric
import SimpleITK as sitk
# Set your paths
prediction_path = "/vol/miltank/users/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/predictions_baseline/case_00504.nii.gz"
ground_truth_path = "/vol/miltank/users/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_raw/Dataset221_KiTS2023/labelsTs/case_00504.nii.gz"

# Load the images
ref_mask1 = sitk.ReadImage(prediction_path)
ref_mask = sitk.GetArrayFromImage(ref_mask1)
pred_masks1 = sitk.ReadImage(ground_truth_path)
pred_masks = sitk.GetArrayFromImage(pred_masks1)

'''
evaluator = Panoptica_Evaluator(
    expected_input=InputType.MATCHED_INSTANCE,
    decision_metric=Metric.IOU,
    decision_threshold=0.5,
)

metrics_to_compute = [
    Metric.DSC,
    Metric.HD95,
    Metric.ASSD,
]

evaluator = Panoptica_Evaluator(
    expected_input=InputType.SEMANTIC,
    instance_approximator=ConnectedComponentsInstanceApproximator(),
    
    instance_metrics=metrics_to_compute,
    instance_matcher=NaiveThresholdMatching(matching_metric=Metric.DSC, matching_threshold=0.1),
    global_metrics=metrics_to_compute,
    verbose=True,
    log_times=True,
)

evaluator.save_to_config("config_kits.yaml")
'''
evaluator = Panoptica_Evaluator.load_from_config("/u/home/wyou/Documents/panoptica/panoptica/configs/config_kits.yaml")
result = evaluator.evaluate(pred_masks, ref_mask)

for i,k in result.items():
   print(k)