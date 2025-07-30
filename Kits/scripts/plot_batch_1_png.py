import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

df_base = pd.read_csv("/u/home/wyou/Documents/datatsv/baseline_model.tsv", sep="\t")
df_hr1 = pd.read_csv("/u/home/wyou/Documents/datatsv/highres1_model.tsv", sep="\t")
df_hr2 = pd.read_csv("/u/home/wyou/Documents/datatsv/highres2_model.tsv", sep="\t")

df_base["Resolution"] = "Baseline"
df_hr1["Resolution"] = "HighRes1"
df_hr2["Resolution"] = "HighRes2"

df_all = pd.concat([df_base, df_hr1, df_hr2], ignore_index=True)

sns.set(style="whitegrid")
structures = ["kidney", "masses", "tumor"]
metrics = {
    "DICE": "global_bin_dsc",
    "ASSD": "global_bin_assd",
    "HD95": "global_bin_hd95"
}

output_dir = "plots_resolution_comparison"
os.makedirs(output_dir, exist_ok=True)

fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(16, 10))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

for row_idx, struct in enumerate(structures):
    for col_idx, (metric_label, metric_suffix) in enumerate(metrics.items()):
        ax = axs[row_idx, col_idx]
        col_name = f"{struct}-{metric_suffix}"

        sns.boxplot(
            x="Resolution", y=col_name, data=df_all,
            palette="Set2", showfliers=True, ax=ax
        )
        sns.stripplot(
            x="Resolution", y=col_name, data=df_all,
            color='black', size=2, jitter=0.15, alpha=0.5, ax=ax
        )
        ax.set_title(f"{struct.capitalize()} - {metric_label}", fontsize=11)
        ax.set_xlabel("")
        ax.set_ylabel(metric_label)

plt.suptitle("Segmentation Metrics Comparison Across Resolutions", fontsize=16)

merged_fig_path = os.path.join(output_dir, "combined_metrics_comparison.png")
plt.savefig(merged_fig_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"✅ Saved combined plot: {merged_fig_path}")

summary_pretty = []

for struct in structures:
    for metric_label, metric_suffix in metrics.items():
        col = f"{struct}-{metric_suffix}"
        grouped = df_all.groupby("Resolution")[col].agg(['mean', 'std'])

        row = {
            "Structure": struct.capitalize(),
            "Metric": metric_label
        }

        for resolution in ["Baseline", "HighRes1", "HighRes2"]:
            if resolution in grouped.index:
                mean = grouped.loc[resolution, 'mean']
                std = grouped.loc[resolution, 'std']
                row[resolution] = f"{mean:.3f} ± {std:.3f}"
            else:
                row[resolution] = "N/A"

        summary_pretty.append(row)

df_summary_pretty = pd.DataFrame(summary_pretty)
df_summary_pretty = df_summary_pretty[["Structure", "Metric", "Baseline", "HighRes1", "HighRes2"]]

print("\n=== Summary Table (mean ± std) ===\n")
print(df_summary_pretty.to_string(index=False))

summary_csv_path = os.path.join(output_dir, "summary_metrics_pretty.csv")
df_summary_pretty.to_csv(summary_csv_path, index=False)
print(f"✅ Saved summary table: {summary_csv_path}")
