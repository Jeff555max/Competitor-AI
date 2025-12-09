"""
Сборка desktop-приложения на PyQt6 с помощью PyInstaller.
Интерфейс повторяет функционал веб-версии: анализ текста, изображений, парсинг сайта, история.
"""
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QLineEdit, QMessageBox, QListWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import requests

API_URL = "http://localhost:8000"  # Можно вынести в .env или конфиг

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Мониторинг конкурентов")
        self.setGeometry(100, 100, 700, 800)
        self.setStyleSheet("""
            QWidget {
                background: #f8fafc;
                color: #222;
                font-family: Arial, sans-serif;
                font-size: 15px;
            }
            QLabel {
                font-size: 1.1em;
                margin-bottom: 4px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06b6d4, stop:1 #8b5cf6);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                margin: 8px 0;
                font-size: 1em;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8b5cf6, stop:1 #06b6d4);
            }
            QTextEdit, QLineEdit {
                background: #fff;
                color: #222;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                padding: 10px;
                margin-bottom: 8px;
            }
            QListWidget {
                background: #fff;
                color: #222;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                padding: 8px;
                margin-bottom: 8px;
            }
        """)
        layout = QVBoxLayout()

        # Анализ текста
        layout.addWidget(QLabel("Анализ текста конкурента:"))
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)
        self.text_btn = QPushButton("Проанализировать текст")
        self.text_btn.clicked.connect(self.analyze_text)
        layout.addWidget(self.text_btn)
        self.text_result = QLabel()
        self.text_result.setWordWrap(True)
        layout.addWidget(self.text_result)

        # Анализ изображения
        layout.addWidget(QLabel("Анализ изображения конкурента:"))
        self.img_btn = QPushButton("Выбрать изображение и проанализировать")
        self.img_btn.clicked.connect(self.analyze_image)
        layout.addWidget(self.img_btn)
        self.img_result = QLabel()
        self.img_result.setWordWrap(True)
        layout.addWidget(self.img_result)

        # Парсинг сайта
        layout.addWidget(QLabel("Парсинг сайта конкурента:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://site.com")
        layout.addWidget(self.url_input)
        self.url_btn = QPushButton("Парсить и анализировать")
        self.url_btn.clicked.connect(self.parse_site)
        layout.addWidget(self.url_btn)
        self.url_result = QLabel()
        self.url_result.setWordWrap(True)
        layout.addWidget(self.url_result)

        # История
        layout.addWidget(QLabel("История запросов:"))
        self.history_btn = QPushButton("Обновить историю")
        self.history_btn.clicked.connect(self.load_history)
        layout.addWidget(self.history_btn)
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        self.clear_history_btn = QPushButton("Очистить историю")
        self.clear_history_btn.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_history_btn)

        self.setLayout(layout)
        self.load_history()

    def analyze_text(self):
        text = self.text_input.toPlainText()
        if len(text) < 10:
            QMessageBox.warning(self, "Ошибка", "Введите текст не короче 10 символов.")
            return
        # Улучшенный системный промпт
        system_prompt = (
            "Ты — профессиональный маркетолог и аналитик конкурентной среды. "
            "Проанализируй предоставленный текст конкурента максимально глубоко и структурированно. "
            "Ответ строго в формате JSON с ключами: strengths (сильные стороны, 3-5), weaknesses (слабые стороны, 3-5), "
            "unique_offers (уникальные предложения, 2-3), recommendations (конкретные рекомендации по улучшению стратегии, 3-5), summary (краткое резюме, 1-2 предложения). "
            "Оцени реальные конкурентные преимущества, недостатки, УТП, предложи практические шаги для усиления позиций. "
            "Пиши на русском, избегай общих фраз, используй профессиональную лексику."
        )
        try:
            r = requests.post(f"{API_URL}/analyze_text", json={"text": text, "system_prompt": system_prompt})
            data = r.json()
            if data.get("success") and data.get("analysis"):
                a = data["analysis"]
                res = f"<b>Сильные стороны:</b> {', '.join(a['strengths'])}<br>"
                res += f"<b>Слабые стороны:</b> {', '.join(a['weaknesses'])}<br>"
                res += f"<b>Уникальные предложения:</b> {', '.join(a['unique_offers'])}<br>"
                res += f"<b>Рекомендации:</b> {', '.join(a['recommendations'])}<br>"
                res += f"<b>Резюме:</b> {a['summary']}"
                self.text_result.setText(res)
            else:
                self.text_result.setText(f"Ошибка: {data.get('error')}")
        except Exception as e:
            self.text_result.setText(f"Ошибка: {e}")

    def analyze_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.gif *.webp")
        if not fname:
            return
        # Улучшенный системный промпт для анализа изображения
        system_prompt = (
            "Ты — эксперт по визуальному маркетингу и брендингу. "
            "Проанализируй изображение конкурента максимально подробно. "
            "Ответ строго в формате JSON с ключами: description (детальное описание), insights (маркетинговые инсайты, 3-5), "
            "visual_style_score (оценка визуального стиля от 0 до 10), recommendations (конкретные рекомендации по улучшению, 3-5). "
            "Оцени цветовую палитру, типографику, композицию, UX/UI, соответствие целевой аудитории. "
            "Пиши на русском, используй профессиональные термины."
        )
        try:
            import mimetypes
            mime, _ = mimetypes.guess_type(fname)
            if not mime:
                mime = 'application/octet-stream'
            with open(fname, "rb") as f:
                files = {"file": (os.path.basename(fname), f, mime)}
                data = {"system_prompt": system_prompt}
                r = requests.post(f"{API_URL}/analyze_image", files=files, data=data)
                resp = r.json()
                if resp.get("success") and resp.get("analysis"):
                    a = resp["analysis"]
                    res = f"<b>Описание:</b> {a['description']}<br>"
                    res += f"<b>Инсайты:</b> {', '.join(a['insights'])}<br>"
                    res += f"<b>Оценка стиля:</b> {a['visual_style_score']}/10<br>"
                    res += f"<b>Рекомендации:</b> {', '.join(a['recommendations'])}"
                    self.img_result.setText(res)
                else:
                    self.img_result.setText(f"Ошибка: {resp.get('error')}")
        except Exception as e:
            self.img_result.setText(f"Ошибка: {e}")

    def parse_site(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Ошибка", "Введите URL сайта.")
            return
        try:
            r = requests.post(f"{API_URL}/parse_demo", json={"url": url})
            data = r.json()
            if data.get("success") and data.get("analysis"):
                a = data["analysis"]
                res = f"<b>Сильные стороны:</b> {', '.join(a['strengths'])}<br>"
                res += f"<b>Слабые стороны:</b> {', '.join(a['weaknesses'])}<br>"
                res += f"<b>Уникальные предложения:</b> {', '.join(a['unique_offers'])}<br>"
                res += f"<b>Рекомендации:</b> {', '.join(a['recommendations'])}<br>"
                res += f"<b>Резюме:</b> {a['summary']}"
                self.url_result.setText(res)
            else:
                self.url_result.setText(f"Ошибка: {data.get('error')}")
        except Exception as e:
            self.url_result.setText(f"Ошибка: {e}")

    def load_history(self):
        try:
            r = requests.get(f"{API_URL}/history")
            data = r.json()
            self.history_list.clear()
            if data.get("items"):
                for item in data["items"]:
                    self.history_list.addItem(f"{item['request_type']} | {item['request_summary']} | {item['response_summary']}")
            else:
                self.history_list.addItem("История пуста")
        except Exception as e:
            self.history_list.clear()
            self.history_list.addItem(f"Ошибка: {e}")

    def clear_history(self):
        try:
            r = requests.delete(f"{API_URL}/history")
            self.load_history()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка очистки истории: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
