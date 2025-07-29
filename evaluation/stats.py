import sys
import os
from panoptica import Panoptica_Statistic
from panoptica.panoptica_statistics import make_curve_over_setups


statlrn = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_native_lr.tsv")
statlrt = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_target_lr.tsv")
statlrd = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_diff_lr.tsv")


statbsn = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_native_bs.tsv")
statbst = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_target_bs.tsv")
statbsd = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_diff_bs.tsv")


stat3n = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_native_h3.tsv")
stat3t = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_target_h3.tsv")
stat3d = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_diff_h3.tsv")

stat4n = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_native_h4.tsv")
stat4t = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_target_h4.tsv")
stat4d = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_diff_h4.tsv")

stat5n = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_native_h5.tsv")
stat5t = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_target_h5.tsv")
stat5d = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_diff_h5.tsv")


stat6n = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_native_h6.tsv")
stat6t = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_target_h6.tsv")
stat6d = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_diff_h6.tsv")

stat7n = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_native_h7.tsv")
stat7t = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_target_h7.tsv")
stat7d = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_diff_h7.tsv")

stat8n = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_native_h8.tsv")
stat8t = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_target_h8.tsv")
stat8d = Panoptica_Statistic.from_file("/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/results_diff_h8.tsv")



statistics_dict = {
    #"baseline<br>2.3x0.6x0.6": stat1,
    #"highres2<br>1x0.4x0.4": stat2,
    #"highres3<br>2.3x0.4x0.4": stat3,
    "lowres_t<br>3x1.5x1.5": statlrt,
    "lowres_n<br>3x1.5x1.5": statlrn,
    #"lowres_d<br>3x1.5x1.5": statlrd,
    "baseline_t<br>2.3x0.6x0.6": statbst,
    "baseline_n<br>2.3x0.6x0.6": statbsn,
    #"baseline_d<br>2.3x0.6x0.6": statbsd,
    "highres3t<br>2.3x0.4x0.4": stat3t,
    "highres3n<br>2.3x0.4x0.4": stat3n,
    #"highres3d<br>2.3x0.4x0.4": stat3d,
    "highres4t<br>1x0.6x0.6": stat4t,
    "highres4n<br>1x0.6x0.6": stat4n,
    #"highres4d<br>1x0.6x0.6": stat4d,
    "highres5t<br>1.5x0.4x0.4": stat5t,
    "highres5n<br>1.5x0.4x0.4": stat5n,
    #"highres5d<br>1.5x0.4x0.4": stat5d,
    "highres6t<br>2x0.4x0.4": stat6t,
    "highres6n<br>2x0.4x0.4": stat6n,
    #"highres6d<br>2x0.4x0.4": stat6d,
    "highres7t<br>0.6x0.6x0.6": stat7t,
    "highres7n<br>0.6x0.6x0.6": stat7n,
    #"highres7d<br>0.6x0.6x0.6": stat7d,
    "highres8t<br>0.4x0.4x0.4": stat8t,
    "highres8n<br>0.4x0.4x0.4": stat8n,
    #"highres8d<br>0.4x0.4x0.4": stat8d,
}

#print(stat1.metricnames)
#print(stat1.groupnames)

metrics = ["sq_dsc", "sq_assd", "sq_hd95", "global_bin_dsc", "global_bin_assd", "global_bin_hd95"]  # or any metric name found in your TSVs
groups = ['ivd', 'spinal_canal', 'vertebra']  # optional: choose groups to compare
figs = []
for metric in metrics: 
    figs.append(make_curve_over_setups(
        statistics_dict=statistics_dict,
        metric=metric,
        groups=groups,
        plot_as_barchart=True,
        plot_std=True,
        figure_title=f"Comparison of {metric} across setups",
        xaxis_title="Model",
        yaxis_title=metric,
        height=800,
        width=1200,
    ))

for i in range(0, 6):
    figs[i].write_html(f"/vol/miltank/users/shchurov/data/dataset/nnUNet_results/Dataset101_SPIDER/eval/panoptica_out/html/stats_21_07_{metrics[i]}.html")
