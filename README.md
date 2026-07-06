# Illegal Web Detection System 🚀

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c.svg)
![License](https://img.shields.io/badge/License-Academic-green.svg)

A **Multimodal Machine Learning** system for detecting illegal websites by combining **visual** and **textual** information. The system leverages **EfficientNetV2-M** for webpage screenshot analysis and **DistilBERT** for webpage text analysis, then deploys the trained model through a **browser extension** for real-time website detection.

---

 🎓 **Academic Project**
This repository contains the implementation of my undergraduate thesis conducted as a student of the **Information Systems** program at **Universitas Jambi**.

# 📖 Overview

Illegal websites often employ deceptive visual designs and persuasive textual content to attract users. Traditional detection methods that rely on only a single modality frequently suffer from limited accuracy and poor generalization.

## 📂 Project Organization

* **📊 Data Collection & Model Training** – The source code for data collection, preprocessing, model training, and evaluation is available on **[Google Drive](https://drive.google.com/drive/folders/1VfCR32NTM8lC74LW2qCrxWccYIHRffuV?usp=drive_link)**. The dataset used in this project is publicly available on **[Kaggle](https://www.kaggle.com/datasets/sahalmaghfud/illegal-web/data)**.

* **🌐 System Implementation** – This repository contains the implementation of the trained models, including the FastAPI backend and browser extension for real-time illegal website detection.

This project addresses these challenges by integrating multiple sources of information into a unified multimodal framework. It combines:

- 🖼️ **Visual Features** extracted from webpage screenshots using **EfficientNetV2-M**.
- 📝 **Textual Features** extracted from webpage content using **DistilBERT**.
- 🧠 **Feature Fusion** through a Multilayer Perceptron (MLP) classifier.
- 🌐 **Browser Extension** for automatic website detection during web browsing.
- ⚡ **FastAPI Backend** for serving trained deep learning models in real time.

---

# ✨ Features

- 🔍 Multimodal website classification using visual and textual information.
- 🖼️ Webpage screenshot analysis with **EfficientNetV2-M**.
- 📝 Webpage text analysis with **DistilBERT**.
- 🧠 Feature fusion using an **MLP classifier**.
- ⚡ FastAPI inference server.
- 🌐 Browser extension compatible with **Google Chrome** and **Microsoft Edge**.
- 📊 Website logging and reporting system.
- 🚫 Real-time illegal website detection.

---

# 🏗️ Project Architecture

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
                        (MLP Fusion)
                               ▼
                     Website Classification
```

---

# 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Deep Learning Framework | PyTorch |
| Visual Encoder | EfficientNetV2-M |
| Text Encoder | DistilBERT |
| Classifier | Multilayer Perceptron (MLP) |
| Browser Extension | JavaScript |

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/sahalmaghfud/illegal-web-detection.git

cd illegal-web-detection
```

---

## 2. Set Up the Backend

Navigate to the backend directory.

```bash
cd server
```

Install all required dependencies.

```bash
pip install -r requirements.txt
```

Download the pretrained models.

```bash
python3 download_models.py
```

Start the FastAPI server.

```bash
uvicorn main:app --reload
```

The server will be available at:

```text
http://127.0.0.1:8000
```

---

## 3. Install the Browser Extension

1. Open **Google Chrome** or **Microsoft Edge**.
2. Navigate to:

```text
chrome://extensions
```

3. Enable **Developer Mode**.
4. Click **Load unpacked**.
5. Select the following directory:

```text
extension/
```

6. The browser extension is now ready to use.

---

# 📈 Workflow

```text
Website
   │
   ▼
Capture Screenshot + Extract Text
   │
   ▼
EfficientNetV2-M + DistilBERT
   │
   ▼
Feature Fusion (MLP)
   │
   ▼
Website Classification
   │
   ▼
Prediction Result
   │
   ▼
Browser Extension Interface
```

---

# 📂 Project Structure

```text
illegal-web-detection/
│
├── extension/          # Browser extension source code
├── server/             # FastAPI backend
├── README.md
└── requirements.txt
```

---

---

### 🔗 Links

- 📄 **[Research Paper](https://jurnal.harapan.ac.id/index.php/Jikstra/article/view/1485/876)**
- 📊 **[Kaggle Dataset](https://www.kaggle.com/datasets/sahalmaghfud/illegal-web/data)**
- 💾 **[Google Drive](https://drive.google.com/drive/folders/1VfCR32NTM8lC74LW2qCrxWccYIHRffuV?usp=drive_link)** 

# ⭐ Support

If you find this project useful for your research or development, please consider giving it a **⭐ Star** on GitHub. Your support helps increase the project's visibility and encourages future improvements.
