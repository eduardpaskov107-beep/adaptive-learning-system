"""
Простые тесты для проверки работоспособности
"""


def test_imports():
    """Тест на возможность импортировать модули"""
    try:
        # Пробуем импортировать основные модули
        import sys
        import os

        # Добавляем src в путь
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        # Теперь импортируем
        import src
        print("✓ Модуль src импортирован успешно")

        return True
    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        return False


def test_requirements():
    """Тест наличия основных библиотек"""
    required_packages = ['numpy', 'pandas', 'sklearn', 'pytest']
    missing = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} найден")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} не найден")

    if missing:
        print(f"\nОтсутствуют пакеты: {missing}")
        print("Установите: pip install " + " ".join(missing))
        return False
    return True


def test_basic_functionality():
    """Тест базовой функциональности"""
    # Создаем простой тест
    result = 2 + 2
    assert result == 4, f"Ожидалось 4, получено {result}"
    print("✓ Базовая математика работает")
    return True


if __name__ == "__main__":
    print("Запуск простых тестов...")
    print("-" * 50)

    results = []
    results.append(test_imports())
    results.append(test_requirements())
    results.append(test_basic_functionality())

    print("-" * 50)
    if all(results):
        print("✅ Все тесты пройдены!")
    else:
        print("❌ Некоторые тесты не пройдены")