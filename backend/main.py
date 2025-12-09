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
        request_summary=request.text[:50],
        response_summary=analysis.summary
    ))
    return TextAnalysisResponse(success=True, analysis=analysis)

@app.post("/analyze_image", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Анализирует изображение конкурента.
    """
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"]:
        return ImageAnalysisResponse(success=False, error="Недопустимый формат изображения")
    image_bytes = await file.read()
    analysis = openai_service.analyze_image(image_bytes)
    from backend.models.schemas import HistoryItem
    import uuid
    from datetime import datetime
    history_service.save_history(HistoryItem(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(),
        request_type="image",
        request_summary=file.filename,
        response_summary=analysis.description
    ))
    return ImageAnalysisResponse(success=True, analysis=analysis)

@app.post("/parse_demo", response_model=ParseDemoResponse)
async def parse_demo(request: ParseDemoRequest):
    """
    Парсит сайт и анализирует контент.
    """
    parsed = parser_service.parse(request.url)
    if parsed["error"]:
        return ParseDemoResponse(success=False, error=parsed["error"])
    # Анализируем текст из title, h1, первого абзаца
    text = f"{parsed['title']} {parsed['h1']} {parsed['first_paragraph']}"
    analysis = openai_service.analyze_text(text)
    from backend.models.schemas import HistoryItem
    import uuid
    from datetime import datetime
    history_service.save_history(HistoryItem(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(),
        request_type="parse",
        request_summary=request.url,
        response_summary=analysis.summary
    ))
    return ParseDemoResponse(success=True, parsed=parsed, analysis=analysis)

@app.get("/history", response_model=HistoryResponse)
async def get_history():
    """
    Возвращает историю последних запросов.
    """
    items = history_service.load_history()
    from backend.models.schemas import HistoryItem
    result = [HistoryItem(**item) for item in items]
    return HistoryResponse(items=result, total=len(result))

@app.delete("/history")
async def clear_history():
    """
    Очищает историю запросов.
    """
    history_service.clear_history()
    return {"success": True, "message": "История очищена"}

@app.get("/health")
async def health_check():
    """
    Проверка работоспособности сервиса.
    """
    return {"status": "healthy", "version": "1.0.0"}

app.mount("/static", StaticFiles(directory="frontend"), name="static")
