import os
import torch
from transformers import AutoTokenizer, AutoModel
from torchvision import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def download_distilbert():
    print("--- Mengunduh DistilBERT Assets ---")
    model_name = "distilbert-base-multilingual-cased"
    save_path = os.path.join(MODELS_DIR, "DistilBERT")
    
    # Download Tokenizer dan Model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    tokenizer.save_pretrained(save_path)
    model.save_pretrained(save_path)
    print(f"DistilBERT disimpan di: {save_path}\n")

def download_efficientnet():
    print("--- Mengunduh EfficientNetV2-M Assets ---")
    save_path = os.path.join(MODELS_DIR, "EfficientNet")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Download Bobot Pre-trained (ImageNet1K_V1)
    weights = models.EfficientNet_V2_M_Weights.IMAGENET1K_V1
    model = models.efficientnet_v2_m(weights=weights)
    torch.save(model.state_dict(), os.path.join(save_path, "efficientnet_v2_m.pth"))
    print(f"EfficientNetV2-M disimpan di: {save_path}/efficientnet_v2_m.pth\n")

if __name__ == "__main__":
    try:
        download_distilbert()
        download_efficientnet()
        print("Semua aset berhasil diunduh!")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengunduh: {e}")