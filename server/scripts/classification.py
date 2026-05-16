import torch
import numpy as np
import os

# --- KONFIGURASI GLOBAL ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_model_instance = None

def load_model(path="models/model_klasifikasi.pt"):
    """
    Memuat model TorchScript (.pt). 
    Tidak memerlukan definisi kelas MultimodalMLP lagi.
    """
    global _model_instance
    if _model_instance is None:
        if os.path.exists(path):
            try:
                # Memuat model TorchScript secara langsung
                _model_instance = torch.jit.load(path, map_location=device)
                _model_instance.eval()
                print(f"[Classification] Model TorchScript berhasil dimuat dari: {path}")
            except Exception as e:
                print(f"[Error] Gagal memuat model TorchScript: {e}")
        else:
            print(f"[Peringatan] File {path} tidak ditemukan!")
            
    return _model_instance

def get_prediction(feat_text, feat_image, feat_html):
    """
    Melakukan Early Fusion dan Inferensi menggunakan model TorchScript.
    Urutan fitur: Teks (768), Gambar (1280), HTML (139).
    """
    model = load_model()
    if model is None:
        return 0, 0.0
    
    # 1. Early Fusion (Konkatenasi)
    # Urutan: Teks -> Gambar -> HTML
    combined = np.concatenate([feat_text, feat_image, feat_html])
    
    # 2. Konversi ke Tensor PyTorch [1, 2187]
    input_tensor = torch.from_numpy(combined).unsqueeze(0).to(device).float()
    
    # 3. Inferensi
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)
        
        pred_idx = torch.argmax(probabilities, dim=1).item()
        confidence = torch.max(probabilities).item()
        
    return pred_idx, confidence

# Tes fungsi jika file dijalankan secara mandiri
# if __name__ == "__main__":
#     # Dummy data untuk pengetesan dimensi
#     test_text = np.random.rand(768).astype(np.float32)
#     test_img = np.random.rand(1280).astype(np.float32)
#     test_html = np.random.rand(139).astype(np.float32)
    
#     p_idx, conf = get_prediction(test_text, test_img, test_html)
#     print(f"Test Result -> Class: {p_idx}, Confidence: {conf:.4f}")