"""
Командный интерфейс для системы обучения (исправленная версия)
"""

import sys
import os

# Добавляем родительскую директорию в путь Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


def main():
    """Основная функция CLI"""
    print("=" * 50)
    print("АДАПТИВНАЯ СИСТЕМА ОБУЧЕНИЯ")
    print("=" * 50)

    # Импортируем здесь, после добавления пути
    from src.core.learning_engine import AdaptiveLearningEngine
    from src.data.knowledge_base import SPECIALIZATIONS

    engine = AdaptiveLearningEngine()

    while True:
        print("\nМеню:")
        print("1. Начать обучение (новый студент)")
        print("2. Выйти")

        choice = input("\nВыберите действие (1-2): ").strip()

        if choice == "1":
            new_student_flow(engine)
        elif choice == "2":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def new_student_flow(engine):
    """Процесс для нового студента"""
    print("\n" + "=" * 30)
    print("РЕГИСТРАЦИЯ НОВОГО СТУДЕНТА")
    print("=" * 30)

    student_id = input("Введите ваш ID (или имя): ").strip()
    if not student_id:
        print("ID не может быть пустым!")
        return
    from src.core.learning_engine import AdaptiveLearningEngine
    from src.data.knowledge_base import SPECIALIZATIONS
    print("\nВыберите вашу специализацию:")
    for i, (key, name) in enumerate(SPECIALIZATIONS.items(), 1):
        print(f"{i}. {name}")

    try:
        spec_choice = int(input("\nВаш выбор (1-3): ").strip())
        specialization = list(SPECIALIZATIONS.keys())[spec_choice - 1]
    except (ValueError, IndexError):
        print("Неверный выбор. Установлена специализация Data Science.")
        specialization = "data_science"

    # Начинаем оценку
    result = engine.start_assessment(student_id, specialization)

    print(f"\nПривет, {student_id}!")
    print(f"Специализация: {SPECIALIZATIONS[specialization]}")
    print("\nТест из 5 вопросов. Ответы вводите цифрами (1, 2, 3, 4).\n")

    answers = {}
    for i, question in enumerate(result["test"], 1):
        print(f"\nВопрос {i}/{len(result['test'])}:")
        print(f"Тема: {question['topic']}")
        print(f"\n{question['question']}")

        for j, option in enumerate(question['options'], 1):
            print(f"{j}. {option}")

        while True:
            try:
                answer = int(input("\nВаш ответ (1-4): ").strip())
                if 1 <= answer <= 4:
                    answers[question['id']] = answer - 1
                    break
                else:
                    print("Пожалуйста, введите число от 1 до 4.")
            except ValueError:
                print("Пожалуйста, введите число.")

    # Отправляем ответы
    print("\nОбработка результатов...")
    assessment_result = engine.submit_assessment(student_id, answers)

    print(f"\nВаш уровень: {assessment_result['assessment']['overall_level'].upper()}")
    print(f"Общий балл: {assessment_result['assessment']['overall_score']:.1f}%")

    if assessment_result['recommendations']:
        print("\nРекомендуемые темы для изучения:")
        for i, rec in enumerate(assessment_result['recommendations'], 1):
            print(f"\n{i}. {rec['subtopic_name']}")
            print(f"   Текущий балл: {rec['current_score']:.1f}%")
            print(f"   Применение в {SPECIALIZATIONS[specialization]}:")
            print(f"   {rec['specialization_application']}")

    # Предлагаем изучить первую тему
    if assessment_result['recommendations']:
        study_choice = input("\nХотите начать изучение первой рекомендованной темы? (да/нет): ").strip().lower()
        if study_choice in ['да', 'yes', 'y', 'д']:
            first_rec = assessment_result['recommendations'][0]
            study_topic_flow(engine, student_id, first_rec, specialization)


def study_topic_flow(engine, student_id, recommendation, specialization):
    """Процесс изучения темы"""
    print(f"\n{'='*40}")
    print(f"ИЗУЧЕНИЕ ТЕМЫ: {recommendation['subtopic_name']}")
    print(f"{'='*40}")

    # Получаем контент
    topic_parts = recommendation['content_link'].split('/')
    content = engine.get_topic_content(topic_parts[0], topic_parts[1])

    if not content:
        print("Контент не найден.")
        return

    print(f"\n{content['content']}")

    # Вопросы для закрепления
    if content.get('practice_questions'):
        print("\n" + "="*30)
        print("ВОПРОСЫ ДЛЯ ЗАКРЕПЛЕНИЯ")
        print("="*30)

        quiz_answers = []
        for i, question in enumerate(content['practice_questions'], 1):
            print(f"\nВопрос {i}:")
            print(question['text'])

            for j, option in enumerate(question['options'], 1):
                print(f"{j}. {option}")

            while True:
                try:
                    answer = int(input("\nВаш ответ: ").strip())
                    if 1 <= answer <= len(question['options']):
                        quiz_answers.append(answer - 1)
                        break
                    else:
                        print(f"Введите число от 1 до {len(question['options'])}")
                except ValueError:
                    print("Пожалуйста, введите число.")

        # Проверяем ответы
        correct = 0
        for i, (question, answer) in enumerate(zip(content['practice_questions'], quiz_answers)):
            if answer == question['correct']:
                correct += 1
                print(f"\nВопрос {i+1}: ✓ Правильно!")
            else:
                print(f"\nВопрос {i+1}: ✗ Неправильно")
                print(f"   Объяснение: {question['explanation']}")

        score = correct / len(quiz_answers) if quiz_answers else 0

        print(f"\nРезультат: {correct}/{len(quiz_answers)} ({score*100:.0f}%)")

        # Отмечаем тему как изученную
        if score >= 0.6:
            result = engine.mark_topic_completed(
                student_id,
                topic_parts[0],
                topic_parts[1],
                score
            )
            print(f"\n{result['message']}")
        else:
            print("\nРекомендуем повторить тему.")
    else:
        print("\nДля этой темы нет вопросов для закрепления.")


if __name__ == "__main__":
    main()