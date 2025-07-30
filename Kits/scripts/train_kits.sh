#!/bin/bash
#SBATCH --job-name=test
#SBATCH --output=logs/test_5.out
#SBATCH --error=logs/test_5.err
#SBATCH --time=3-24:00:00
#SBATCH --partition=asteroids
#SBATCH --qos=master
#SBATCH --gres=gpu:1
#SBATCH --mem=72G
#SBATCH --cpus-per-task=10
#SBATCH --mail-user=go73hay@mytum.de
#SBATCH --mail-type=ALL

# 加载环境
source ~/.bashrc
conda init bash
conda activate ADML

# 设置环境变量
export PYTHONPATH="/vol/miltank/users/wyou/Documents/nnUNet:$PYTHONPATH"
export nnUNet_raw="/u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_raw"
export nnUNet_preprocessed="/u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_preprocessed"
export nnUNet_results="/u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_trained_models"

# 解决多进程问题的关键设置
export CUDA_VISIBLE_DEVICES=0
export OMP_NUM_THREADS=2 # training 4
export MKL_NUM_THREADS=2 # training 4
export TORCH_MULTIPROCESSING_SHARING_STRATEGY=file_system
export CUDA_LAUNCH_BLOCKING=1
export NUM_THREADS=2
# 设置Python缓冲
export PYTHONUNBUFFERED=1

# 启动训练
#/u/home/wyou/.conda/envs/ADML/bin/nnUNetv2_train 211 3d_lowres 0
# nnUNetv2_plan_and_preprocess -d 221 --verify_dataset_integrity
# nnUNetv2_train 221 3d_lowres 0
# nnUNetv2_train 221 3d_fullres 1


#nnUNetv2_predict -d 221 -i /u/home/wyou/Documents/target_images_model_1 -o /u/home/wyou/Documents/predictions_target_model_1 -f all -c 3d_fullres --save_probabilities
#nnUNetv2_predict -d 221 -i /u/home/wyou/Documents/target_images_model_2 -o /u/home/wyou/Documents/predictions_target_model_2 -f all -c 3d_fullres --save_probabilities
#nnUNetv2_predict -d 221 -i /u/home/wyou/Documents/target_images_model_3 -o /u/home/wyou/Documents/predictions_target_model_3 -f all -c 3d_fullres --save_probabilities
#nnUNetv2_predict -d 221 -i /u/home/wyou/Documents/target_images_model_4 -o /u/home/wyou/Documents/predictions_target_model_4 -f all -c 3d_fullres --save_probabilities
nnUNetv2_predict -d 221 -i /u/home/wyou/Documents/target_images_model_5 -o /u/home/wyou/Documents/predictions_target_model_5 -f all -c 3d_fullres --save_probabilities

# nnUNetv2_evaluate_folder -d 221 -ref /u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_raw/Dataset221_KiTS2023/labelsTs/ -pred /u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/predictions_fold2/ -c 3d_fullres

#nnUNetv2_evaluate_folder \
# -djfile /u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_preprocessed/Dataset221_KiTS2023/dataset.json \
# -pfile /u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_preprocessed/Dataset221_KiTS2023/nnUNetPlans.json \
# /u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/nnUNet_raw/Dataset221_KiTS2023/labelsTs \
# /u/home/wyou/Documents/nnUNet/nnUNetFrame/dataset_221/predictions_baseline