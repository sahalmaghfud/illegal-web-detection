import torch
from transformers import AutoTokenizer, AutoModel
import os
import csv 
import re
import ftfy

# --- KONFIGURASI ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_tokenizer = None
_text_model = None
_slang_dict = None

def load_text_assets():
    """Memuat Tokenizer, Model DistilBERT, dan Kamus Slang tanpa Pandas"""
    global _tokenizer, _text_model, _slang_dict
    
    path = "models/DistilBERT"
    model_name = "distilbert-base-multilingual-cased"
    slang_csv_path = 'scripts/colloquial-indonesian-lexicon.csv'
    
    # 1. Memuat Kamus Slang menggunakan modul csv bawaan
    if _slang_dict is None:
        if os.path.exists(slang_csv_path):
            try:
                with open(slang_csv_path, mode='r', encoding='utf-8') as f:
                    # Mengasumsikan kolom pertama 'slang' dan kedua 'formal'
                    # DictReader otomatis memetakan kolom berdasarkan header di baris pertama
                    reader = csv.DictReader(f)
                    _slang_dict = {row['slang'].lower(): row['formal'] for row in reader}
                print(f"[Text] Kamus slang dimuat: {len(_slang_dict)} entri.")
            except Exception as e:
                print(f"[Error] Gagal membaca CSV: {e}")
                _slang_dict = {}
        else:
            _slang_dict = {}
            print(f"[Warning] File CSV tidak ditemukan. Normalisasi dilewati.")

    # 2. Memuat Model & Tokenizer (tetap efisien dengan variabel global)
    if _tokenizer is None or _text_model is None:
        if os.path.exists(path):
            _tokenizer = AutoTokenizer.from_pretrained(path)
            _text_model = AutoModel.from_pretrained(path).to(device)
        else:
            _tokenizer = AutoTokenizer.from_pretrained(model_name)
            _text_model = AutoModel.from_pretrained(model_name).to(device)
        _text_model.eval()
        
    return _tokenizer, _text_model, _slang_dict

def preprocess_text(text):
    if not isinstance(text, str): return ""
    
    text = ftfy.fix_text(text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Normalisasi Slang
    words = text.split()
    normalized_words = [_slang_dict.get(w.lower(), w) for w in words]
    return " ".join(normalized_words)

def extract_text_features(text):
    tokenizer, model, _ = load_text_assets()
    clean_text = preprocess_text(text)
    
    inputs = tokenizer(
        clean_text, 
        return_tensors="pt", 
        truncation=True, 
        padding=True, 
        max_length=512
    ).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        cls_feature = outputs.last_hidden_state[:, 0, :]
        
    return cls_feature.squeeze().cpu().numpy()

# Inisialisasi awal
load_text_assets()