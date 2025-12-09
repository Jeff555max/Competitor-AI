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
        # ...existing code...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
