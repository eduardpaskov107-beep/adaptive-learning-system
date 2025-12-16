# 🎓 Адаптивная система обучения с ИИ

[![Tests](https://github.com/ваш-username/adaptive-learning-system/workflows/Tests/badge.svg)](https://github.com/ваш-username/adaptive-learning-system/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Персонализированная система обучения, которая определяет уровень знаний студента с помощью ИИ и рекомендует только те материалы, которые ему действительно нужны, с объяснением применения в выбранной специализации.

## ✨ Особенности

- 🧠 **Оценка уровня знаний** с помощью адаптивного тестирования
- 🎯 **Персонализированные рекомендации** на основе слабых мест
- 📚 **Контекстуализация материала** под специализацию студента
- 📊 **Аналитика прогресса** с ежедневными отчетами
- ⚙️ **Автоматизация** через CI/CD (GitHub Actions)

## 🏗️ Архитектура
adaptive-learning-system/
├── run.py                          # Точка входа
├── requirements.txt                # Зависимости
├── src/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── enhanced_cli.py        # Улучшенный интерфейс
│   │   └── main.py                # Старый интерфейс
│   ├── core/
│   │   ├── __init__.py
│   │   └── learning_engine.py     # Улучшенный движок
│   ├── data/
│   │   ├── __init__.py
│   │   └── knowledge_base.py      # Расширенная база знаний
│   └── models/
│       ├── __init__.py
│       └── knowledge_assessment.py
├── data/                           # Данные прогресса
└── .github/workflows/              # CI/CD


## 🚀 Быстрый старт

### Установка

```bash
# Клонирование репозитория
git clone https://github.com/ваш-username/adaptive-learning-system.git
cd adaptive-learning-system

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск CLI интерфейса
python src/cli/main.py

# Или запуск тестов
pytest tests/

# Проверка качества кода
flake8 src/
black --check src/
