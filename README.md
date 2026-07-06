# Illegal Web Detection System 🚀

Sistem deteksi situs web ilegal berbasis **Multimodal Machine Learning**. Proyek ini menggabungkan analisis fitur **Visual** (menggunakan arsitektur *EfficientNetV2 Medium*) dan **Tekstual** (menggunakan *IndoBERT/DistilBERT*) untuk mengklasifikasikan dan mendeteksi domain ilegal secara otomatis melalui ekstensi peramban (*browser extension*).

---

## 📌 Fitur Utama
* **Analisis Multimodal**: Menggabungkan konten teks dan visual dari halaman web untuk akurasi deteksi yang lebih tinggi.
* **Klasifikasi Gambar**: Menggunakan **EfficientNetV2 Medium** untuk mengenali tata letak atau elemen visual situs ilegal.
* **Klasifikasi Teks**: Menggunakan **IndoBERT / DistilBERT** untuk menganalisis konten teks berbahasa Indonesia dan mengekstrak fitur semantik.
* **Ekstensi Browser**: Implementasi langsung pada peramban untuk mendeteksi dan memblokir akses situs ilegal secara *real-time*.

---

## 📂 Struktur Repositori

Secara garis besar, proyek ini dibagi menjadi dua bagian utama:
1. **`extension/`**: Berisi *source code* ekstensi browser .
2. **`server/`**: Backend berbasis **FastAPI** yang menangani proses inferensi model machine learning dan manajemen basis data.

```text
├── domains.json                # Dataset domain yang telah dilabeli
├── extension.zip               # Ekstensi siap pakai dalam bentuk zip
