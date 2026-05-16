import base64
import io
from contextlib import asynccontextmanager
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from PIL import Image
from tinydb import TinyDB, Query
from fastapi.middleware.cors import CORSMiddleware

# Import modular
from scripts.text_extractor import load_text_assets, extract_text_features
from scripts.image_extractor import load_visual_model, extract_image_features
from scripts.classification import load_model, get_prediction

# --- LIFESPAN EVENT HANDLER ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_text_assets()    
    load_visual_model()   
    load_model()          
    yield 
    print("--- Mematikan Server ---")

app = FastAPI(
    title="API Deteksi Konten Ilegal Multimodal",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi DB
prediction_logss_db = TinyDB('database/prediction_logs.json')
list_db = TinyDB('database/list.json')
reports_db = TinyDB('database/reports.json')

# Pydantic Models
class PredictRequest(BaseModel):
    url: str
    text_content: str 
    image_base64: str 
    html_features: List[float]
class ReportRequest(BaseModel):
    url: str
    label_reported_by_user: int
    
def get_domain(url: str) -> str:
    """Mengekstrak domain dari URL (misal: https://sub.example.com/page -> example.com atau sub.example.com)"""
    try:
        domain = urlparse(url).netloc
        # Jika netloc kosong (biasanya karena url tidak diawali http/https), coba parse ulang
        if not domain:
            domain = urlparse(f"http://{url}").netloc
        return domain.lower()
    except Exception:
        return url.lower()
    
def decode_image(b64_str):
    if "," in b64_str:
        b64_str = b64_str.split(",")[1]
    img_data = base64.b64decode(b64_str)
    return Image.open(io.BytesIO(img_data)).convert("RGB")

@app.post("/predict")
async def predict(request: PredictRequest):
    try:
        domain = get_domain(request.url)
        # Ekstraksi Fitur
        feat_text = extract_text_features(request.text_content)
        img_obj = decode_image(request.image_base64)
        feat_image = extract_image_features(img_obj)
        feat_html = request.html_features
        
        # Inferensi
        pred_idx, confidence = get_prediction(feat_text, feat_image, feat_html)     

        if pred_idx is None:
            pred_idx, confidence = 4, 1.0
        else:
            confidence = round(float(confidence), 4)
        
        # Simpan ke logs
        prediction_logss_db.insert({
            "url": request.url,
            "label": pred_idx,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })

        # Simpan ke list_db menggunakan URL utuh
        UrlQuery = Query()
        list_db.upsert(
            {"domain": domain, "label": pred_idx}, 
            UrlQuery.url == request.url
        )

        return {
            "label": pred_idx,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/check-domain")
async def check_domain(url: str):
    # Ekstrak domain dari input 
    domain = get_domain(url)    
    # Cari di database menggunakan key 'domain'
    DomainQuery = Query()
    result = list_db.get(DomainQuery.domain == domain)
    if result:
        return {
            "in_list": True, 
            "domain": domain,
            "label": result['label']
        }
        
    return {
        "in_list": False,
        "domain": domain
    }


@app.post("/report")
async def report(request: ReportRequest):
    if not (0 <= request.label_reported_by_user <= 3):
        raise HTTPException(status_code=400, detail="Label harus diantara 0-3")
        
    ReportQuery = Query()
    existing_report = reports_db.get(ReportQuery.url == request.url)
    
    if existing_report:
        # Update array count yang sudah ada
        current_counts = existing_report['count_label_reported_by_user']
        current_counts[request.label_reported_by_user] += 1
        reports_db.update(
            {"count_label_reported_by_user": current_counts}, 
            ReportQuery.url == request.url
        )
    else:
        counts = [0, 0, 0, 0]
        counts[request.label_reported_by_user] = 1
        reports_db.insert({
            "url": request.url,
            "count_label_reported_by_user": counts,
            "last_report_at": datetime.now().isoformat()
        })
    
    return {"status": "success", "message": "Report recorded"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)