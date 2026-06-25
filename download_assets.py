import os
import zipfile
import shutil
import gdown

def setup_dirs():
    print("Setting up required directories...")
    os.makedirs("models/vgg", exist_ok=True)
    os.makedirs("checkpoints", exist_ok=True)

def download_file(file_id, output_path, expected_size=None):
    print(f"\nDownloading/checking: {output_path}...")
    
    # Check if file exists and has non-zero size
    if os.path.exists(output_path):
        current_size = os.path.getsize(output_path)
        if current_size > 0:
            if expected_size and abs(current_size - expected_size) < 1024 * 1024: # within 1MB
                print(f"Skipping {output_path} (already fully downloaded, size match: {current_size} bytes)")
                return True
            elif not expected_size:
                print(f"Skipping {output_path} (already exists, size: {current_size} bytes)")
                return True
            else:
                print(f"File exists but size ({current_size} bytes) does not match expected ({expected_size} bytes). Resuming/redownloading...")

    try:
        # Use resume=True so that interrupted downloads can continue from where they stopped
        gdown.download(id=file_id, output=output_path, resume=True, quiet=False)
        return True
    except Exception as e:
        print(f"Warning: Failed to download/verify {output_path} with ID {file_id}: {e}")
        return False

def download_vgg():
    vgg_path = "models/vgg/vgg19_conv.pth"
    # vgg19_conv.pth is about 160,198,540 bytes
    download_file("1rvow8jStPt8t2prDcSRlnf8yzXhrYeGo", vgg_path, expected_size=160198540)

def download_pretrained_model():
    print("\nDownloading pretrained DCI-VTON model files individually...")
    
    # 1. viton512.ckpt (~5.3GB / 5321322766 bytes)
    download_file("1q8udsotB-JfroOmXI1P28m5ykEbrmh4Y", "checkpoints/viton512.ckpt", expected_size=5321322766)
    
    # 2. viton512_v2.ckpt (optional secondary model)
    download_file("177zXMarfVU6K_F-vtuC5fawNKThOu3ai", "checkpoints/viton512_v2.ckpt")
    
    # 3. warp_viton.pth
    download_file("1EY52bIpxMdf7YBRhkqaIx7aYx1F87E8n", "checkpoints/warp_viton.pth")

def download_viton_hd_dataset():
    zip_path = "../VITON-HD.zip"
    dest_dir = "D:/projects"
    
    if not os.path.exists(os.path.join(dest_dir, "VITON-HD/train/image")) or len(os.listdir(os.path.join(dest_dir, "VITON-HD/train/image"))) < 1000:
        print("\nDataset not fully downloaded/extracted. Proceeding with download...")
        success = download_file("1tLx8LRp-sxDp0EcYmYoV_vXdSc-jJ79w", zip_path)
        
        if success and os.path.exists(zip_path):
            print("\nExtracting VITON-HD dataset...")
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    namelist = zip_ref.namelist()
                    has_viton_hd_prefix = all(name.startswith("VITON-HD/") or name.startswith("VITON-HD\\") for name in namelist if name.strip())
                    
                    if has_viton_hd_prefix:
                        print("Zip contains 'VITON-HD/' folder root. Extracting to D:/projects...")
                        zip_ref.extractall(dest_dir)
                    else:
                        print("Zip does not contain 'VITON-HD/' folder root. Extracting to D:/projects/VITON-HD...")
                        zip_ref.extractall(os.path.join(dest_dir, "VITON-HD"))
                print("VITON-HD dataset extracted successfully.")
            except Exception as e:
                print(f"Error extracting dataset zip file: {e}")
        else:
            print("Skipping dataset extraction due to download failure.")
    else:
        print("\nVITON-HD dataset seems already downloaded and extracted.")

def download_pre_warped_cloths():
    print("\nDownloading pre-warped cloth images and masks...")
    temp_dir = "D:/projects/pre_warped_temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    target_viton_hd = "D:/projects/VITON-HD"
    test_warp_dir = os.path.join(target_viton_hd, "test/cloth-warp")
    
    if not os.path.exists(test_warp_dir) or len(os.listdir(test_warp_dir)) < 100:
        try:
            print("Downloading folder from Google Drive...")
            gdown.download_folder(id="15cBiA0AoSCLSkg3ueNFWSw4IU3TdfXbO", output=temp_dir, quiet=False)
            
            print("\nOrganizing pre-warped cloth files...")
            for root, dirs, files in os.walk(temp_dir):
                for d in dirs:
                    if d in ['train', 'test']:
                        src_path = os.path.join(root, d)
                        dest_path = os.path.join(target_viton_hd, d)
                        print(f"Merging {src_path} into {dest_path}...")
                        
                        for sub_root, sub_dirs, sub_files in os.walk(src_path):
                            rel_path = os.path.relpath(sub_root, src_path)
                            target_sub_dir = os.path.join(dest_path, rel_path) if rel_path != "." else dest_path
                            os.makedirs(target_sub_dir, exist_ok=True)
                            for file in sub_files:
                                src_file = os.path.join(sub_root, file)
                                dest_file = os.path.join(target_sub_dir, file)
                                shutil.copy2(src_file, dest_file)
                                
            # Clean up temp folder
            shutil.rmtree(temp_dir)
            print("Cleaned up temporary directories.")
        except Exception as e:
            print(f"Error handling pre-warped cloths: {e}")
    else:
        print("Pre-warped cloth files already exist.")

if __name__ == "__main__":
    setup_dirs()
    download_vgg()
    download_pretrained_model()
    download_viton_hd_dataset()
    download_pre_warped_cloths()
    print("\nAll assets downloaded and organized successfully!")
