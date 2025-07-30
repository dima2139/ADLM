import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ================== 文件读取 ==================
# 请将这三个文件名替换为你实际使用的文件名
df_base = pd.read_csv("/u/home/wyou/Documents/datatsv/baseline_model.tsv", sep="\t")
df_hr1 = pd.read_csv("/u/home/wyou/Documents/datatsv/highres1_model.tsv", sep="\t")
df_hr2 = pd.read_csv("/u/home/wyou/Documents/datatsv/highres2_model.tsv", sep="\t")

df_base["Resolution"] = "Baseline"
df_hr1["Resolution"] = "HighRes1"
df_hr2["Resolution"] = "HighRes2"

df_all = pd.concat([df_base, df_hr1, df_hr2], ignore_index=True)

# ================== 设置 ==================
sns.set(style="whitegrid")
structures = ["kidney", "masses", "tumor"]
metrics = {
    "DICE": "global_bin_dsc",
    "ASSD": "global_bin_assd",
    "HD95": "global_bin_hd95"
}

# 保存图像目录
output_dir = "plots_resolution_comparison"
os.makedirs(output_dir, exist_ok=True)

# ================== 绘图并保存 ==================
for struct in structures:
    fig, axs = plt.subplots(1, 3, figsize=(14, 4))
    for i, (metric_label, metric_suffix) in enumerate(metrics.items()):
        col_name = f"{struct}-{metric_suffix}"
        sns.boxplot(
            x="Resolution", y=col_name, data=df_all,
            palette="Set2", showfliers=True, ax=axs[i]
        )
        sns.stripplot(
            x="Resolution", y=col_name, data=df_all,
            color='black', size=2, jitter=0.15, alpha=0.5, ax=axs[i]
        )
        axs[i].set_title(f"{struct.capitalize()} - {metric_label}")
        axs[i].set_xlabel("Resolution")
        axs[i].set_ylabel(metric_label)

    plt.suptitle(f"{struct.capitalize()} Segmentation Metrics", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # 保存为 PNG 文件
    fig_path = os.path.join(output_dir, f"{struct}_metrics_comparison.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"✅ Saved: {fig_path}")

# ================== 可选：生成均值 ± 标准差表格 ==================
summary_list = []
for struct in structures:
    for metric_label, metric_suffix in metrics.items():
        col = f"{struct}-{metric_suffix}"
        summary = df_all.groupby("Resolution")[col].agg(['mean', 'std']).reset_index()
        summary["Structure"] = struct
        summary["Metric"] = metric_label
        summary_list.append(summary)

summary_df = pd.concat(summary_list, ignore_index=True)
summary_df = summary_df[['Structure', 'Metric', 'Resolution', 'mean', 'std']]
summary_df.columns = ['Structure', 'Metric', 'Resolution', 'Mean', 'StdDev']

# 保存统计表为 CSV（可选）
summary_df.to_csv(os.path.join(output_dir, "summary_table.csv"), index=False)
print("✅ Saved summary table as summary_table.csv")
