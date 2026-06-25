import os
import tarfile
import shutil
import gdown

def setup_dirs():
    print("Setting up required directories...")
    os.makedirs("D:/projects/VITON-HD/test", exist_ok=True)
    os.makedirs("D:/projects/VITON-HD/train", exist_ok=True)

def download_and_extract(file_id, dest_folder):
    print(f"\nProcessing download to {dest_folder}...")
    temp_tar = "D:/projects/temp_warp.tar.gz"
    
    # Download
    gdown.download(id=file_id, output=temp_tar, quiet=False)
    
    # Extract
    print(f"Extracting to {dest_folder}...")
    os.makedirs(dest_folder, exist_ok=True)
    try:
        with tarfile.open(temp_tar, "r:gz") as tar:
            tar.extractall(path=dest_folder)
        print("Extraction complete.")
    except Exception as e:
        print(f"Error extracting: {e}")
        
    # Clean up temp file
    if os.path.exists(temp_tar):
        os.remove(temp_tar)

def main():
    setup_dirs()
    
    # File mappings (id -> target extraction directory)
    # Note: These tar files usually contain a folder or list of files.
    # Let's check how they extract.
    # We want the files to end up directly in D:/projects/VITON-HD/test/cloth-warp etc.
    
    # 1. cloth-warp-test.tar.gz -> D:/projects/VITON-HD/test (it probably extracts a folder named 'cloth-warp')
    download_and_extract("1Z1zDCqMijc8CbnEbAM52e_UQKWynlN4V", "D:/projects/VITON-HD/test")
    
    # 2. cloth-warp-mask-test.tar.gz -> D:/projects/VITON-HD/test
    download_and_extract("1wHHRes4tCA3Xf7FMewTnFa1rnMtnbC96", "D:/projects/VITON-HD/test")
    
    # 3. unpaired-cloth-warp.tar.gz -> D:/projects/VITON-HD/test
    download_and_extract("1TeozekPqUVqyTHZLGtZeaFuDrp55vJHu", "D:/projects/VITON-HD/test")
    
    # 4. unpaired-cloth-warp-mask.tar.gz -> D:/projects/VITON-HD/test
    download_and_extract("146fmnJZRp4BYApnjD-vSWP_PmX1rp6Kh", "D:/projects/VITON-HD/test")
    
    # 5. cloth-warp-train.tar.gz -> D:/projects/VITON-HD/train
    download_and_extract("1I6drHpQwHQuedP9XLf5KFWqT3HCw9ZRh", "D:/projects/VITON-HD/train")
    
    # 6. cloth-warp-mask-train.tar.gz -> D:/projects/VITON-HD/train
    download_and_extract("1eoUUnu3HjX8ntiN9Hr1Be43IH-ZTsJb-", "D:/projects/VITON-HD/train")
    
    print("\nAll pre-warped cloths successfully downloaded and extracted!")

if __name__ == "__main__":
    main()
