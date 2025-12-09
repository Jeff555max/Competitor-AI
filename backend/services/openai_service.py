"""
Сервис для работы с OpenAI API.
"""
import base64
import json
from openai import OpenAI
from backend.config import settings
from backend.models.schemas import CompetitorAnalysis, ImageAnalysis

class OpenAIService:
    """
    Сервис для анализа текста и изображений через OpenAI.
    """
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.vision_model = settings.OPENAI_VISION_MODEL

    def analyze_text(self, text: str) -> CompetitorAnalysis:
        """
        Анализирует текст конкурента через GPT-4o.

        Args:
            text (str): Текст конкурента.

        Returns:
            CompetitorAnalysis: Структурированный анализ.
        """
        # TODO: Реализовать реальный запрос к OpenAI GPT-4o
        # Здесь возвращается пример для теста
        return CompetitorAnalysis(
            strengths=["Сильный бренд", "Хорошая поддержка", "Широкий ассортимент"],
            weaknesses=["Высокие цены", "Медленная доставка"],
            unique_offers=["Эксклюзивные продукты"],
            recommendations=["Снизить цены", "Улучшить логистику"],
            summary="Конкурент силён, но есть возможности для улучшения."
        )

    def analyze_image(self, image_bytes: bytes) -> ImageAnalysis:
        """
        Анализирует изображение конкурента через GPT-4o.

        Args:
            image_bytes (bytes): Изображение в байтах.

        Returns:
            ImageAnalysis: Анализ изображения.
        """
        # TODO: Реализовать реальный запрос к OpenAI Vision
        # Здесь возвращается пример для теста
        return ImageAnalysis(
            description="Баннер с яркой цветовой палитрой и современным шрифтом.",
            insights=["Привлекает внимание", "Хорошая композиция"],
            visual_style_score=8,
            recommendations=["Добавить CTA", "Упростить дизайн"]
        )

openai_service = OpenAIService()
