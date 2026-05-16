import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
import os

# --- KONFIGURASI ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_tokenizer = None
_text_model = None

def load_text_assets():
    """Memuat Tokenizer dan Model DistilBERT satu kali ke memori"""
    global _tokenizer, _text_model
    
    path = "models/DistilBERT"
    model_name = "distilbert-base-multilingual-cased"
    
    if _tokenizer is None or _text_model is None:
        if os.path.exists(path):
            # Memuat dari folder lokal (offline mode)
            _tokenizer = AutoTokenizer.from_pretrained(path)
            _text_model = AutoModel.from_pretrained(path).to(device)
            print(f"[Text] DistilBERT dimuat dari folder lokal: {path}")
        else:
            # Download jika folder lokal belum ada
            _tokenizer = AutoTokenizer.from_pretrained(model_name)
            _text_model = AutoModel.from_pretrained(model_name).to(device)
            print(f"[Text] Folder lokal tidak ditemukan, mendownload {model_name}...")
            
        _text_model.eval()
        
    return _tokenizer, _text_model

def extract_text_features(text):
    """Mengubah teks menjadi vektor 768 dimensi (CLS Token)"""
    tokenizer, model = load_text_assets()
    
    # Tokenisasi
    inputs = tokenizer(
        text, 
        return_tensors="pt", 
        truncation=True, 
        padding=True, 
        max_length=512
    ).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        # Ambil [CLS] token (vektor fitur utama kalimat)
        last_hidden_state = outputs.last_hidden_state
        cls_feature = last_hidden_state[:, 0, :]
        
    return cls_feature.squeeze().cpu().numpy()

# Jalankan pemuatan saat import
load_text_assets()