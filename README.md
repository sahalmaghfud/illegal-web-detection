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

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/sahalmaghfud/illegal-web-detection.git

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
python3 download_models.py
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

⭐ If you find this project useful, please consider giving it a **Star** on GitHub.
