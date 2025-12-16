#!/usr/bin/env python3
"""
Запуск адаптивной системы обучения
"""

import sys
import os


def main():
    """Запускает систему обучения"""
    print("=" * 60)
    print("🎓 АДАПТИВНАЯ СИСТЕМА ОБУЧЕНИЯ")
    print("=" * 60)

    try:
        # Запускаем улучшенный CLI
        from src.cli.enhanced_cli import main as cli_main
        cli_main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()