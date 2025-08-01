import os
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import seaborn as sns

# === CONFIGURATION ===
data_dir = "/u/home/wyou/Documents/panoptica_out"
tsv_files = glob(os.path.join(data_dir, "*.tsv"))
organs = ["kidney", "masses", "tumor"]
metrics = ["global_bin_dsc", "global_bin_assd", "global_bin_hd95"]

# === Load data ===
all_data = []

for file_path in tsv_files:
    filename = os.path.basename(file_path).replace(".tsv", "")
    input_type = "resampled" if "_target" in filename else "native"
    clean_name = filename.replace("all_", "").replace("_model_vox_target", "").replace("_model_vox", "")
    model_name = clean_name.strip()
    df = pd.read_csv(file_path, sep="\t")
    df["Model"] = model_name
    df["InputType"] = input_type
    all_data.append(df)

df_all = pd.concat(all_data, ignore_index=True)

# === Model name mapping (extend this mapping if needed) ===
model_name_map = {
    "OG_baseline": "0.8x0.8x0.8",
    "OG_highres1": "0.64x0.64x0.64",
    "OG_highres2": "0.53x0.53x0.53",
    "OG_lowres1": "1.06x1.06x1.06",
    "OG_lowres2": "1.6x1.6x1.6",
    "baseline": "3.0x0.8x0.8",
    "highres0_5": "2.25x0.7x0.7",
    "highres1": "1.5x0.6x0.6",
    "highres1_5": "1.25x0.5x0.5",
    "highres2": "1.0x0.4x0.4",
    "highres1_5_model_2000_vox": "1.5x0.6x0.6 (2000 epochs)",
}

# === Output per-organ comparison summary table ===
output_dir = "./panoptica_out_summary"
os.makedirs(output_dir, exist_ok=True)

for organ in organs:
    selected_cols = [f"{organ}-{m}" for m in metrics]
    col_rename = {
        f"{organ}-global_bin_dsc": "Dice",
        f"{organ}-global_bin_assd": "ASSD",
        f"{organ}-global_bin_hd95": "HD95"
    }
    df_subset = df_all[["Model", "InputType"] + selected_cols].copy()
    df_subset.rename(columns=col_rename, inplace=True)
    summary = df_subset.groupby(["Model", "InputType"])[["Dice", "ASSD", "HD95"]].mean().reset_index()
    summary["ModelLabel"] = summary["Model"].map(model_name_map).fillna(summary["Model"])
    summary.to_csv(os.path.join(output_dir, f"{organ}_summary.csv"), index=False)

# === Plot combined figures ===
plot_dir = "./panoptica_out_plots"
os.makedirs(plot_dir, exist_ok=True)

# Merge all organ summaries
all_summary = []
for organ in organs:
    summary = pd.read_csv(os.path.join(output_dir, f"{organ}_summary.csv"))
    summary["Organ"] = organ
    all_summary.append(summary)
df_all_summary = pd.concat(all_summary, ignore_index=True)

# Ensure ModelLabel is available
df_all_summary["ModelLabel"] = df_all_summary["Model"].map(model_name_map).fillna(df_all_summary["Model"])

# Filter out 2000-epoch models
df_all_summary_no_2000 = df_all_summary[~df_all_summary["Model"].str.contains("2000")]
df_all_summary_no_2000["ModelLabel"] = df_all_summary_no_2000["Model"].map(model_name_map).fillna(df_all_summary_no_2000["Model"])

# 1. Plot Dice per model (native / resampled separately, all organs)
for input_type in ["native", "resampled"]:
    df_plot = df_all_summary_no_2000[df_all_summary_no_2000["InputType"] == input_type]
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df_plot,
        x="ModelLabel",
        y="Dice",
        hue="Organ",
        palette="Set2",
        edgecolor="black"
    )
    plt.title(f"Dice by Model ({input_type}) - All Organs")
    plt.ylabel("Dice")
    plt.xlabel("Model")
    plt.ylim(0, 1.0)
    plt.legend(title="Organ")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, f"allorgans_model_resolution_{input_type}.png"))
    plt.close()

# 2. Epoch comparison (all organs)
epoch_models = []
for model in df_all_summary["Model"].unique():
    if "2000" in model:
        base = model.replace("_2000", "")
        if base in df_all_summary["Model"].values:
            epoch_models.append((base, model))

for base, model_2000 in epoch_models:
    df_epoch = df_all_summary[df_all_summary["Model"].isin([base, model_2000])]
    df_epoch["ModelLabel"] = df_epoch["Model"].map(model_name_map).fillna(df_epoch["Model"])
    if df_epoch.empty:
        continue
    plt.figure(figsize=(8, 6))
    sns.barplot(
        data=df_epoch,
        x="ModelLabel",
        y="Dice",
        hue="Organ",
        palette="Set1",
        edgecolor="black"
    )
    plt.title(f"Dice: {model_name_map.get(base, base)} vs {model_name_map.get(model_2000, model_2000)} (All Organs)")
    plt.ylabel("Dice")
    plt.xlabel("Model")
    plt.ylim(0, 1.0)
    plt.legend(title="Organ")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, f"allorgans_epoch_compare_{base}.png"))
    plt.close()

# 3. Native vs Resampled comparison (all organs)
df_plot = df_all_summary_no_2000.copy()
plt.figure(figsize=(12, 6))
sns.barplot(
    data=df_plot,
    x="ModelLabel",
    y="Dice",
    hue="InputType",
    palette="Set1",
    edgecolor="black"
)
plt.title("Dice: Native vs Resampled (All Organs)")
plt.ylabel("Dice")
plt.xlabel("Model")
plt.ylim(0, 1.0)
plt.legend(title="Input Type")
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, "allorgans_native_vs_resampled.png"))
plt.close()

# 4. Epoch comparison with two specific models (all organs)
epoch_models = ["highres1_5", "highres1_5_model_2000_vox"]
df_epoch = df_all_summary[df_all_summary["Model"].isin(epoch_models)]
df_epoch["ModelLabel"] = df_epoch["Model"].map(model_name_map).fillna(df_epoch["Model"])
if len(df_epoch["Model"].unique()) < 2:
    print("Only one model found. Cannot perform epoch comparison plot. Make sure both models exist.")
else:
    plt.figure(figsize=(8, 6))
    sns.barplot(
        data=df_epoch,
        x="ModelLabel",
        y="Dice",
        hue="Organ",
        palette="Set1",
        edgecolor="black"
    )
    plt.title("Dice: 1000 vs 2000 Epochs (All Organs, highres1_5_model)")
    plt.ylabel("Dice")
    plt.xlabel("Model")
    plt.ylim(0, 1.0)
    plt.legend(title="Organ")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, "allorgans_epoch_compare_highres1_5.png"))
    plt.close()

# ========== Generate Excel summaries ==========

# 1. Full summary of Dice for all models and organs
df_all_summary.to_excel(os.path.join(plot_dir, "allorgans_allmodels_dice.xlsx"), index=False)

# 2. Dice summary without 2000-epoch models
df_all_summary_no_2000.to_excel(os.path.join(plot_dir, "allorgans_allmodels_no2000_dice.xlsx"), index=False)

# 3. Native vs Resampled comparison
native_vs_resampled = df_all_summary_no_2000.pivot_table(
    index=["ModelLabel", "Organ"], columns="InputType", values="Dice"
).reset_index()
native_vs_resampled.to_excel(os.path.join(plot_dir, "allorgans_native_vs_resampled_detail.xlsx"), index=False)

# 4. Epoch comparison detail
epoch_models = ["highres1_5", "highres1_5_model_2000_vox"]
df_epoch = df_all_summary[df_all_summary["Model"].isin(epoch_models)]
df_epoch["ModelLabel"] = df_epoch["Model"].map(model_name_map).fillna(df_epoch["Model"])
df_epoch.to_excel(os.path.join(plot_dir, "allorgans_epoch_compare_detail.xlsx"), index=False)

print("All figures and tables have been generated and saved to:", plot_dir)
print("All model names:", df_all_summary['Model'].unique())
