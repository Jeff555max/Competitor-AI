"""
Pydantic схемы для API.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class TextAnalysisRequest(BaseModel):
    """
    Запрос на анализ текста конкурента.
    """
    text: str = Field(..., min_length=10, description="Текст для анализа")

class ParseDemoRequest(BaseModel):
    """
    Запрос на парсинг URL.
    """
    url: str = Field(..., description="URL для парсинга")

class CompetitorAnalysis(BaseModel):
    """
    Структурированный анализ конкурента.
    """
    strengths: List[str] = Field(default_factory=list, description="Сильные стороны конкурента")
    weaknesses: List[str] = Field(default_factory=list, description="Слабые стороны конкурента")
    unique_offers: List[str] = Field(default_factory=list, description="Уникальные предложения конкурента")
    recommendations: List[str] = Field(default_factory=list, description="Рекомендации по улучшению стратегии")
    summary: str = Field("", description="Общее резюме")

class ImageAnalysis(BaseModel):
    """
    Анализ изображения конкурента.
    """
    description: str = Field("", description="Описание изображения")
    insights: List[str] = Field(default_factory=list, description="Маркетинговые инсайты")
    visual_style_score: int = Field(0, ge=0, le=10, description="Оценка визуального стиля конкурента")
    recommendations: List[str] = Field(default_factory=list, description="Рекомендации")

class ParsedContent(BaseModel):
    """
    Результат парсинга страницы.
    """
    title: str = Field("", description="Title страницы")
    h1: str = Field("", description="Главный заголовок (h1)")
    first_paragraph: str = Field("", description="Первый абзац")
    error: Optional[str] = None

class TextAnalysisResponse(BaseModel):
    """
    Ответ на анализ текста.
    """
    success: bool = True
    analysis: Optional[CompetitorAnalysis] = None
    error: Optional[str] = None

class ImageAnalysisResponse(BaseModel):
    """
    Ответ на анализ изображения.
    """
    success: bool = True
    analysis: Optional[ImageAnalysis] = None
    error: Optional[str] = None

class ParseDemoResponse(BaseModel):
    """
    Ответ на парсинг сайта.
    """
    success: bool = True
    parsed: Optional[ParsedContent] = None
    analysis: Optional[CompetitorAnalysis] = None
    error: Optional[str] = None

class HistoryItem(BaseModel):
    """
    Элемент истории запроса.
    """
    id: str
    timestamp: datetime
    request_type: str
    request_summary: str
    response_summary: str

class HistoryResponse(BaseModel):
    """
    Ответ со списком истории.
    """
    items: List[HistoryItem]
    total: int
