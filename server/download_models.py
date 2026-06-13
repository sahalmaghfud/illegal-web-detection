import os
import torch
import requests
from transformers import AutoTokenizer, AutoModel
from torchvision import models

# --- KONFIGURASI PATH ---
# Lokasi root (tempat skrip ini dijalankan)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Folder untuk aset pendukung (CSV, dll)
SCRIPT_DIR = os.path.join(BASE_DIR, "scripts")
# 2. Folder untuk aset model AI
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Path spesifik untuk Kamus Slang
SLANG_CSV_PATH = os.path.join(SCRIPT_DIR, "colloquial-indonesian-lexicon.csv")

# Pastikan kedua folder utama tersedia
os.makedirs(SCRIPT_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

def download_slang_lexicon():
    """Mengunduh Kamus Alay/Slang ke folder ./scripts"""
    print("--- Mengunduh Kamus Slang (CSV) ---")
    url = "https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        with open(SLANG_CSV_PATH, 'wb') as f:
            f.write(response.content)
        print(f" Kamus slang disimpan di: {SLANG_CSV_PATH}\n")
    except Exception as e:
        print(f" Gagal mengunduh CSV: {e}")

def download_distilbert():
    """Mengunduh DistilBERT ke folder ./models/DistilBERT"""
    print("--- Mengunduh DistilBERT Assets ---")
    model_name = "distilbert-base-multilingual-cased"
    save_path = os.path.join(MODELS_DIR, "DistilBERT")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    tokenizer.save_pretrained(save_path)
    model.save_pretrained(save_path)
    print(f" DistilBERT disimpan di: {save_path}\n")

def download_efficientnet():
    """Mengunduh EfficientNetV2-M ke folder ./models/EfficientNet"""
    print("--- Mengunduh EfficientNetV2-M Assets ---")
    save_path = os.path.join(MODELS_DIR, "EfficientNet")
    os.makedirs(save_path, exist_ok=True)
    
    weights = models.EfficientNet_V2_M_Weights.IMAGENET1K_V1
    model = models.efficientnet_v2_m(weights=weights)
    
    # Simpan bobot model (.pth)
    torch.save(model.state_dict(), os.path.join(save_path, "efficientnet_v2_m.pth"))
    print(f" EfficientNetV2-M disimpan di: {save_path}/efficientnet_v2_m.pth\n")

if __name__ == "__main__":
    try:
        download_slang_lexicon()   
        download_distilbert()      
        download_efficientnet()   
        print("Selesai! Struktur './scripts' dan './models' siap digunakan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")