"""
Сервис для работы с историей запросов.
"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from backend.models.schemas import HistoryItem

class HistoryService:
    """
    Управление историей запросов пользователя.
    """
    HISTORY_FILE = Path("history.json")
    MAX_ITEMS = 10

    def load_history(self) -> list:
        """
        Загружает историю из файла.

        Returns:
            list: Список элементов истории.
        """
        if self.HISTORY_FILE.exists():
            try:
                with self.HISTORY_FILE.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                return data
            except Exception:
                return []
        return []

    def save_history(self, item: HistoryItem):
        """
        Сохраняет новый элемент истории.

        Args:
            item (HistoryItem): Элемент истории.
        """
        history = self.load_history()
        history.append(item.model_dump())
        if len(history) > self.MAX_ITEMS:
            history = history[-self.MAX_ITEMS:]
        with self.HISTORY_FILE.open("w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2, default=str)

    def clear_history(self):
        """
        Очищает историю запросов.
        """
        if self.HISTORY_FILE.exists():
            self.HISTORY_FILE.unlink()

history_service = HistoryService()
