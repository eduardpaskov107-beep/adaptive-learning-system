"""
Командный интерфейс для системы обучения
"""

import sys
import json
from pathlib import Path
from typing import Optional

from src.core.learning_engine import AdaptiveLearningEngine
from src.data.knowledge_base import SPECIALIZATIONS


def main():
    """Основная функция CLI"""
    print("=" * 50)
    print("АДАПТИВНАЯ СИСТЕМА ОБУЧЕНИЯ")
    print("=" * 50)
    
    engine = AdaptiveLearningEngine()
    
    # Пробуем загрузить существующий прогресс
    engine.load_progress()
    
    while True:
        print("\nМеню:")
        print("1. Начать обучение (новый студент)")
        print("2. Продолжить обучение")
        print("3. Просмотреть прогресс")
        print("4. Выйти")
        
        choice = input("\nВыберите действие (1-4): ").strip()
        
        if choice == "1":
            new_student_flow(engine)
        elif choice == "2":
            continue_student_flow(engine)
        elif choice == "3":
            view_progress_flow(engine)
        elif choice == "4":
            print("Сохранение прогресса...")
            engine.save_progress()
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def new_student_flow(engine: AdaptiveLearningEngine):
    """Процесс для нового студента"""
    print("\n" + "=" * 30)
    print("РЕГИСТРАЦИЯ НОВОГО СТУДЕНТА")
    print("=" * 30)
    
    student_id = input("Введите ваш ID (или имя): ").strip()
    if not student_id:
        print("ID не может быть пустым!")
        return
    
    print("\nВыберите вашу специализацию:")
    for i, (key, name) in enumerate(SPECIALIZATIONS.items(), 1):
        print(f"{i}. {name}")
    
    try:
        spec_choice = int(input("\nВаш выбор (1-5): ").strip())
        specialization = list(SPECIALIZATIONS.keys())[spec_choice - 1]
    except (ValueError, IndexError):
        print("Неверный выбор. Установлена специализация Data Science.")
        specialization = "data_science"
    
    # Начинаем оценку
    result = engine.start_assessment(student_id, specialization)
    
    print(f"\nПривет, {student_id}!")
    print(f"Специализация: {SPECIALIZATIONS[specialization]}")
    print("\nТеперь пройдите начальный тест из 10 вопросов.")
    print("Ответы вводите цифрами (1, 2, 3, 4).\n")
    
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
                    answers[question['id']] = answer - 1  # Сохраняем как 0-based индекс
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
            print(f"{i}. {rec['subtopic_name']} (приоритет: {rec['priority']:.0f})")
            print(f"   Применение в {SPECIALIZATIONS[specialization]}:")
            print(f"   {rec['specialization_application']}\n")
    
    # Предлагаем изучить первую тему
    if assessment_result['recommendations']:
        study_first_topic = input("Хотите начать изучение первой рекомендованной темы? (да/нет): ").strip().lower()
        if study_first_topic in ['да', 'yes', 'y']:
            first_rec = assessment_result['recommendations'][0]
            study_topic_flow(engine, student_id, first_rec)


def continue_student_flow(engine: AdaptiveLearningEngine):
    """Процесс для существующего студента"""
    student_id = input("Введите ваш ID: ").strip()
    
    progress = engine.get_student_progress(student_id)
    if "error" in progress:
        print(f"Студент с ID '{student_id}' не найден.")
        return
    
    print(f"\nДобро пожаловать, {student_id}!")
    print(f"Уровень: {progress['current_level'].upper()}")
    print(f"Прогресс: {progress.get('overall_progress', 0):.1f}%")
    
    if progress['recommendations']:
        print("\nВаши следующие рекомендации:")
        for i, rec in enumerate(progress['recommendations'][:3], 1):
            print(f"{i}. {rec['subtopic_name']}")
        
        choice = input("\nВыберите тему для изучения (номер) или 0 для выхода: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(progress['recommendations']):
                study_topic_flow(engine, student_id, progress['recommendations'][idx])
    else:
        print("Поздравляем! Вы изучили все рекомендованные темы.")


def study_topic_flow(engine: AdaptiveLearningEngine, student_id: str, recommendation: dict):
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
                    print(f"Пожалуйста, введите число от 1 до {len(question['options'])}.")
            except ValueError:
                print("Пожалуйста, введите число.")
    
    # Проверяем ответы
    correct = 0
    for i, (question, answer) in enumerate(zip(content['practice_questions'], quiz_answers)):
        if answer == question['correct']:
            correct += 1
            print(f"\nВопрос {i+1}: ✓ Правильно!")
        else:
            print(f"\nВопрос {i+1}: ✗ Неправильно. {question['explanation']}")
    
    score = correct / len(quiz_answers) if quiz_answers else 0
    
    print(f"\nРезультат: {correct}/{len(quiz_answers)} ({score*100:.0f}%)")
    
    # Отмечаем тему как изученную
    if score >= 0.6:  # Если правильных ответов >= 60%
        result = engine.mark_topic_completed(
            student_id, 
            topic_parts[0], 
            topic_parts[1], 
            score
        )
        print(f"\n{result['message']}")
    else:
        print("\nРекомендуем повторить тему и пройти тест снова.")


def view_progress_flow(engine: AdaptiveLearningEngine):
    """Просмотр прогресса"""
    student_id = input("Введите ID студента: ").strip()
    
    progress = engine.get_student_progress(student_id)
    if "error" in progress:
        print(f"Студент с ID '{student_id}' не найден.")
        return
    
    print(f"\n{'='*50}")
    print(f"ПРОГРЕСС СТУДЕНТА: {student_id}")
    print(f"{'='*50}")
    
    print(f"\nСпециализация: {SPECIALIZATIONS.get(progress['specialization'], 'Не указана')}")
    print(f"Уровень: {progress['current_level'].upper()}")
    print(f"Общий прогресс: {progress.get('overall_progress', 0):.1f}%")
    print(f"Дата начала: {progress.get('start_date', 'Неизвестно')}")
    
    if progress.get('assessment'):
        print(f"\nОценка знаний:")
        for topic, score in progress['assessment'].get('topic_scores', {}).items():
            print(f"  {topic}: {score:.1f}%")
    
    if progress.get('studied_topics'):
        print(f"\nИзученные темы ({len(progress['studied_topics'])}):")
        for topic in progress['studied_topics']:
            print(f"  - {topic['topic']} ({topic['score']*100:.0f}%)")


if __name__ == "__main__":
    main()
