import sys
import os
from panoptica import Panoptica_Statistic
from panoptica.panoptica_statistics import make_curve_over_setups

# === Load Panoptica TSV ===
tsv_path = ""
output_dir = ""
print(f"🔍 Loading statistics from: {tsv_path}")
stat_loaded = Panoptica_Statistic.from_file(tsv_path)

# === Give label to this setup (key will appear on x-axis) ===
statistics_dict = {
    "baseline<br>2.3x0.6x0.6": stat_loaded
}

# === Metric and Group Settings ===
metrics = [
    "sq_dsc", 
    "sq_assd", 
    "sq_hd95", 
    "global_bin_dsc", 
    "global_bin_assd", 
    "global_bin_hd95"
]
groups = ['ivd', 'spinal_canal', 'vertebra']

# === Output Directory ===
os.makedirs(output_dir, exist_ok=True)

# === Create plots ===
for metric in metrics:
    print(f"📊 Generating plot for: {metric}")
    fig = make_curve_over_setups(
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
    )
    
    output_path = os.path.join(output_dir, f"stats_21_07_{metric}.html")
    fig.write_html(output_path)
    print(f"✅ Saved plot: {output_path}")

print("\n✅ All metric plots saved.")
