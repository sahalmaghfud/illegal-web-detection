# Illegal Web Detection System 🚀

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c.svg)
![License](https://img.shields.io/badge/License-Academic-green.svg)

A **Multimodal Machine Learning** system for detecting illegal websites by combining **visual** and **textual** information. The system integrates **EfficientNetV2-M** for screenshot analysis and **DistilBERT** for webpage text analysis, then deploys the trained model through a **browser extension** for real-time website detection.

---

## 📖 Overview

Illegal websites often employ deceptive visual layouts and persuasive textual content to attract users. Relying on only one modality frequently leads to reduced detection performance.

This project addresses the problem by combining:

- 🖼️ **Visual Features** extracted from webpage screenshots using EfficientNetV2-M.
- 📝 **Textual Features** extracted from webpage content using DistilBERT.
- 🌐 **Browser Extension** that performs automatic detection while users browse the web.
- ⚡ **FastAPI Backend** that serves the trained deep learning models.

---

## ✨ Features

- 🔍 Multimodal website classification using visual and textual information.
- 🖼️ Screenshot analysis with **EfficientNetV2-M**.
- 📝 Text analysis with **DistilBERT**.
- ⚡ FastAPI inference server.
- 🌐 Browser Extension (Chrome/Edge).
- 📊 Logging and website reporting system.
- 🚫 Real-time illegal website detection.

---

## 🏗️ Project Architecture

```text
                        Browser Extension
                               │
                               ▼
                    Capture Website Information
                 (Screenshot + Extracted Web Text)
                               │
                               ▼
                        FastAPI Backend
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
      EfficientNetV2-M                  DistilBERT
      (Visual Features)             (Text Features)
               └───────────────┬───────────────┘
                               ▼
                    Multimodal Classifier
                               ▼
                     Website Classification
```
---

## 🛠 Technology Stack

| Component | Technology |
|------------|------------|
| Backend | FastAPI |
| Deep Learning | PyTorch |
| Visual Model | EfficientNetV2-M |
| Text Model | DistilBERT |
| Browser Extension | JavaScript |
| Database | JSON |
| API | REST |

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY_NAME.git

cd REPOSITORY_NAME
```

---

## 2. Install Backend

Masuk ke folder server.

```bash
cd server
```

Install seluruh dependency.

```bash
pip install -r requirements.txt
```

Download model yang diperlukan.

```bash
python download_models.py
```

Jalankan FastAPI.

```bash
uvicorn main:app --reload
```

Server akan berjalan di

```
http://127.0.0.1:8000
```

---

## 3. Install Browser Extension

1. Buka Chrome atau Microsoft Edge.
2. Masuk ke:

```
chrome://extensions
```

3. Aktifkan **Developer Mode**.
4. Klik **Load unpacked**.
5. Pilih folder:

```
extension/
```

6. Extension siap digunakan.

---

# 📊 Dataset

The dataset was compiled independently and contains:

- **20,447 unique domains**
- Website screenshots
- Extracted webpage text
- Multiple website categories for illegal website detection

---

# 🤖 Deep Learning Models

## Visual Model

- EfficientNetV2-M
- Input: Website screenshots
- Output: Visual embedding

---

## Text Model

- DistilBERT
- Input: Webpage text
- Output: Text embedding

---

## Multimodal Fusion

The visual and textual embeddings are concatenated and passed through a Multi-Layer Perceptron (MLP) classifier to produce the final website category prediction.

---

# 📈 Workflow

```text
Website
   │
   ▼
Extract Screenshot + Text
   │
   ▼
EfficientNetV2-M + DistilBERT
   │
   ▼
Feature Fusion
   │
   ▼
MLP Classifier
   │
   ▼
Prediction
   │
   ▼
Browser Extension
```

---

# 📜 Publications & Citation

If you use this repository, dataset, or methodology in your research, please cite:

### APA

> Maghfud, S. (2026). *Multimodal Learning Menggunakan EfficientNetV2 dan DistilBERT untuk Deteksi Website Ilegal dan Implementasinya pada Browser Extension*. Universitas Jambi.

### BibTeX

```bibtex
@article{maghfud2026multimodal,
  title={Multimodal Learning Menggunakan EfficientNetV2 dan DistilBERT untuk Deteksi Website Ilegal dan Implementasinya pada Browser Extension},
  author={Maghfud, Sahal},
  year={2026},
  publisher={Universitas Jambi}
}
```

---

# 📄 License

This repository is intended for academic and research purposes.

Please cite the corresponding publication if you use this work in your research.

---

# 👨‍💻 Author

**Sahal Maghfud**

Faculty of Science and Technology

Universitas Jambi

---

⭐ If you find this project useful, please consider giving it a **Star** on GitHub.
