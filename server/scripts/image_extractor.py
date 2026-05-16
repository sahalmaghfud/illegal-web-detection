import torch
import torch.nn as nn
from torchvision import models, transforms
import os

# --- KONFIGURASI ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_image_model = None

# Transformasi gambar sesuai Gambar 20 di skripsi Anda (Resize 480x480)
preprocess = transforms.Compose([
    transforms.Resize((480, 480)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_visual_model():
    """Memuat EfficientNetV2-M satu kali ke memori"""
    global _image_model
    if _image_model is None:
        # 1. Inisialisasi arsitektur
        _image_model = models.efficientnet_v2_m().to(device)
        
        # 2. Muat bobot lokal (Pastikan file ada di path ini)
        weight_path = "models/EfficientNet/efficientnet_v2_m.pth"
        if os.path.exists(weight_path):
            _image_model.load_state_dict(torch.load(weight_path, map_location=device))
            print(f"[Image] EfficientNetV2-M dimuat dari {weight_path}")
        else:
            # Fallback jika file lokal tidak ada (akan mendownload otomatis)
            _image_model = models.efficientnet_v2_m(weights=models.EfficientNet_V2_M_Weights.IMAGENET1K_V1).to(device)
            print("[Image] Bobot lokal tidak ditemukan, mendownload dari ImageNet...")
        
        # 3. Buang layer klasifikasi terakhir (Hanya ambil fitur 1280 dim)
        _image_model.classifier = nn.Identity()
        _image_model.eval()
        
    return _image_model

def extract_image_features(pil_image):
    """Mengubah gambar menjadi vektor 1280 dimensi"""
    model = load_visual_model()
    
    # Preprocessing
    img_t = preprocess(pil_image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        features = model(img_t)
    
    return features.squeeze().cpu().numpy()

# Jalankan pemuatan saat import
load_visual_model()