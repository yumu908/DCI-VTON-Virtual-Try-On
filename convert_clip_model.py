import os
import shutil
import torch
from safetensors.torch import load_file

def main():
    source_blob_dir = r"C:\Users\intel\.cache\huggingface\hub\models--openai--clip-vit-large-patch14\blobs"
    config_blob_name = "2c19f6666e0e163c7954df66cb901353fcad088e"
    model_blob_name = "a2bf730a0c7debf160f7a6b50b3aaf3703e7e88ac73de7a314903141db026dcb"
    
    target_dir = r"d:\projects\DCI-VTON-Virtual-Try-On\clip-vit-large-patch14"
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. Copy config
    src_config = os.path.join(source_blob_dir, config_blob_name)
    dst_config = os.path.join(target_dir, "config.json")
    print(f"Copying config from {src_config} to {dst_config}...")
    shutil.copy(src_config, dst_config)
    
    # 2. Convert and save pytorch_model.bin
    src_model = os.path.join(source_blob_dir, model_blob_name)
    dst_model = os.path.join(target_dir, "pytorch_model.bin")
    print(f"Loading safetensors from {src_model}...")
    state_dict = load_file(src_model)
    print(f"Saving pytorch state dict to {dst_model}...")
    torch.save(state_dict, dst_model)
    
    print("\nConversion successfully completed! Model is ready offline.")

if __name__ == "__main__":
    main()
