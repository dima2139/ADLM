#!/bin/bash
#SBATCH --job-name=nnunet_preprocess
#SBATCH --output=logs/preprocess_dataset100_2.out
#SBATCH --error=logs/preprocess_dataset100_2.err
#SBATCH --time=0-02:00:00
#SBATCH --partition=asteroids
#SBATCH --qos=master
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --mail-user=dmytro.shchurov@tum.de
#SBATCH --mail-type=ALL
#SBATCH --cpus-per-task=8

# Load environment and paths
source ~/.bashrc
source /u/home/shchurov/miniconda3/etc/profile.d/conda.sh
conda init bash
conda activate nn_UNet

export nnUNet_raw=/vol/miltank/users/shchurov/data/dataset/nnUNet_raw
export nnUNet_preprocessed=/vol/miltank/users/shchurov/data/dataset/nnUNet_preprocessed
export nnUNet_results=/vol/miltank/users/shchurov/data/dataset/nnUNet_results

# Run preprocessing for Dataset100 with 3d_fullres configuration
nnUNetv2_plan_and_preprocess -d 100 -c 3d_fullres
