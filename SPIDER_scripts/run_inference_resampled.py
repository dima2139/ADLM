import os
import glob
import subprocess
import tempfile
from tptbox import NII

# --- Configuration ---
INPUT_FOLDER = ""
OUTPUT_FOLDER_TARGET_RES = ""
OUTPUT_FOLDER_NATIVE_RES = ""

# --- Separated trainer and plans ---
TRAINER_NAME = "nnUNetTrainer"
PLANS_IDENTIFIER = "nnUNetPlans"

# ---Data and Target ---
DATASET_ID = "079"
TARGET_SPACING = (2.3, 0.6, 0.6)

def main():
    print(f"Starting inference with target spacing: {TARGET_SPACING}")
    os.makedirs(OUTPUT_FOLDER_TARGET_RES, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER_NATIVE_RES, exist_ok=True)

    image_files = sorted(glob.glob(os.path.join(INPUT_FOLDER, '*.nii.gz')))
    print(f"Found {len(image_files)} images to process.")

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_input_dir = os.path.join(tmpdir, "input")
        temp_output_dir = os.path.join(tmpdir, "output")
        os.makedirs(temp_input_dir)
        os.makedirs(temp_output_dir)
        print(f"Created temporary directory: {tmpdir}")

        for image_path in image_files:
            filename = os.path.basename(image_path)
            print(f"\nProcessing: {filename}")

            # 1. Load and rescale
            img_nii_native = NII.load(image_path, seg=False)
            img_nii_rescaled = img_nii_native.rescale(TARGET_SPACING)
            temp_input_path = os.path.join(temp_input_dir, filename)
            img_nii_rescaled.save(temp_input_path, make_parents=True)

            # 2. Run the command-line prediction
            print("  > Running nnUNetv2_predict via command line...")
            # ---command arguments ---
            command = [
                'nnUNetv2_predict',
                '-i', temp_input_dir,
                '-o', temp_output_dir,
                '-d', DATASET_ID,
                '-c', '3d_fullres',
                '-f', 'all',
                '-tr', TRAINER_NAME,
                '-p', PLANS_IDENTIFIER, # Added -p for plans
               # '--disable_tta'
            ]
            
            try:
                # leave the error handling in for now
                subprocess.run(command, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print("--- ERROR during nnUNetv2_predict ---")
                print(f"Command failed with exit code {e.returncode}")
                print("\n--- STDOUT ---")
                print(e.stdout)
                print("\n--- STDERR ---")
                print(e.stderr)
                return
            
            print("  > Prediction complete.")

            # 3. Load the segmentation result
            
            output_files = glob.glob(os.path.join(temp_output_dir, '*.nii.gz'))
            if not output_files:
                raise FileNotFoundError(f"nnU-Net did not produce an output file in {temp_output_dir}")
            temp_output_path = output_files[0] # Get the path of the first (and only) result file

            print(f"  > Loading prediction from: {temp_output_path}")
            seg_nii_target_res = NII.load(temp_output_path, seg=True)

            # 4. Save target-resolution segmentation
            output_path_target = os.path.join(OUTPUT_FOLDER_TARGET_RES, filename)
            seg_nii_target_res.save(output_path_target)
            print(f"  > Saved target resolution segmentation to: {output_path_target}")

            # 5. Resample back to native resolution
            seg_nii_native_res = seg_nii_target_res.resample_from_to(img_nii_native)

            # 6. Save final native-resolution segmentation
            output_path_native = os.path.join(OUTPUT_FOLDER_NATIVE_RES, filename)
            seg_nii_native_res.save(output_path_native)
            print(f"  > Saved final native resolution segmentation to: {output_path_native}")

            # 7. Clean up temporary files
            os.remove(temp_input_path)
            os.remove(temp_output_path)

    print("\n\nInference finished for all images!")

if __name__ == '__main__':
    main()
