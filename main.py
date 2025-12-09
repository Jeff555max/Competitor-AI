"""
Главный модуль FastAPI приложения.
Мультимодальный ассистент мониторинга конкурентов.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.config import settings
from backend.models.schemas import (
    TextAnalysisRequest,
    TextAnalysisResponse,
    ImageAnalysisResponse,
    ParseDemoRequest,
    ParseDemoResponse,
    HistoryResponse
)
from backend.services.openai_service import openai_service
from backend.services.parser_service import parser_service
from backend.services.history_service import history_service

app = FastAPI(
    title="Мониторинг конкурентов",
    description="Мультимодальный AI ассистент для анализа конкурентов.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Главная страница — отдаёт фронтенд.
    """
    return FileResponse("frontend/index.html")

@app.post("/analyze_text", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Анализирует текст конкурента.
    """
    if len(request.text) < 10:
        return TextAnalysisResponse(success=False, error="Текст слишком короткий")
    analysis = openai_service.analyze_text(request.text)
    # Сохраняем в историю
    from backend.models.schemas import HistoryItem
    import uuid
    from datetime import datetime
    history_service.save_history(HistoryItem(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(),
        request_type="text",
        request=request.text,
        response=analysis
    ))
    return TextAnalysisResponse(success=True, result=analysis)

# ...existing endpoints...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
