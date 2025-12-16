"""
Улучшенный CLI интерфейс с визуализацией прогресса
"""

import sys
import os
import time
from datetime import datetime

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


# Простые цвета для терминала
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text):
    """Выводит заголовок с цветом"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.END}")


def print_success(text):
    """Выводит успешное сообщение"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Выводит сообщение об ошибке"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    """Выводит информационное сообщение"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def print_warning(text):
    """Выводит предупреждение"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def progress_bar(percentage, width=50):
    """Создает текстовый прогресс-бар"""
    filled = int(width * percentage / 100)
    bar = f"{Colors.GREEN}{'█' * filled}{Colors.END}{'░' * (width - filled)}"
    return f"[{bar}] {percentage:.1f}%"


def print_progress(title, current, total):
    """Выводит прогресс с баром"""
    percentage = (current / total * 100) if total > 0 else 0
    bar = progress_bar(percentage)
    print(f"\n{Colors.BOLD}{title}{Colors.END}")
    print(f"  {bar} ({current}/{total})")


def animate_loading(text="Загрузка", duration=2):
    """Анимация загрузки"""
    print(f"\n{text}", end="", flush=True)
    for i in range(duration * 4):
        time.sleep(0.25)
        print(".", end="", flush=True)
    print()


def main():
    """Основная функция CLI"""
    print_header("🎓 АДАПТИВНАЯ СИСТЕМА ОБУЧЕНИЯ")

    try:
        from src.core.learning_engine import AdaptiveLearningEngine
        from src.data.knowledge_base import SPECIALIZATIONS

        engine = AdaptiveLearningEngine()
        print_success("Система загружена успешно!")

        while True:
            print(f"\n{Colors.BOLD}Главное меню:{Colors.END}")
            print(f"  1. {Colors.GREEN}Начать обучение{Colors.END}")
            print(f"  2. {Colors.BLUE}Продолжить обучение{Colors.END}")
            print(f"  3. {Colors.YELLOW}Мой прогресс{Colors.END}")
            print(f"  4. {Colors.RED}Выйти{Colors.END}")

            choice = input(f"\n{Colors.BOLD}Выберите действие (1-4): {Colors.END}").strip()

            if choice == "1":
                new_student_flow(engine)
            elif choice == "2":
                continue_student_flow(engine)
            elif choice == "3":
                view_progress_flow(engine)
            elif choice == "4":
                print_success("До свидания! Ваш прогресс сохранен.")
                break
            else:
                print_error("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print_error(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()


def new_student_flow(engine):
    """Процесс для нового студента"""
    print_header("НОВЫЙ СТУДЕНТ")
    from src.core.learning_engine import AdaptiveLearningEngine
    from src.data.knowledge_base import SPECIALIZATIONS
    student_id = input(f"{Colors.BOLD}Введите ваш ID (или имя): {Colors.END}").strip()
    if not student_id:
        print_error("ID не может быть пустым!")
        return

    print(f"\n{Colors.BOLD}Выберите вашу специализацию:{Colors.END}")
    for i, (key, name) in enumerate(SPECIALIZATIONS.items(), 1):
        print(f"  {Colors.CYAN}{i}. {name}{Colors.END}")

    try:
        spec_choice = int(input(f"\n{Colors.BOLD}Ваш выбор (1-3): {Colors.END}").strip())
        specialization = list(SPECIALIZATIONS.keys())[spec_choice - 1]
        print_success(f"Выбрана специализация: {SPECIALIZATIONS[specialization]}")
    except (ValueError, IndexError):
        print_warning("Неверный выбор. Установлена специализация Data Science.")
        specialization = "data_science"

    animate_loading("Настройка вашего профиля")

    # Начинаем оценку
    result = engine.start_assessment(student_id, specialization)

    print_success(f"Привет, {student_id}!")
    print_info(f"Специализация: {SPECIALIZATIONS[specialization]}")
    print_info(f"Тест из {len(result['test'])} вопросов")

    answers = take_test_flow(result["test"])

    animate_loading("Анализ ваших ответов")

    assessment_result = engine.submit_assessment(student_id, answers)

    print_header("РЕЗУЛЬТАТЫ ТЕСТА")
    print(
        f"\n{Colors.BOLD}Ваш уровень:{Colors.END} {Colors.YELLOW}{assessment_result['assessment']['overall_level'].upper()}{Colors.END}")
    print(f"{Colors.BOLD}Балл теста:{Colors.END} {assessment_result['test_score']:.1f}%")

    if assessment_result.get('learning_path'):
        print(f"\n{Colors.BOLD}Ваш учебный путь:{Colors.END}")
        for i, topic in enumerate(assessment_result['learning_path'], 1):
            level_color = {
                'beginner': Colors.GREEN,
                'intermediate': Colors.YELLOW,
                'advanced': Colors.RED
            }.get(topic.get('level', 'beginner'), Colors.WHITE)

            print(f"  {i}. {topic['subtopic_name']} [{level_color}{topic.get('level', '?')}{Colors.END}]")

    input(f"\n{Colors.BOLD}Нажмите Enter чтобы начать обучение...{Colors.END}")
    start_learning_flow(engine, student_id)


def take_test_flow(test_questions):
    """Процесс прохождения теста"""
    answers = {}

    for i, question in enumerate(test_questions, 1):
        print_header(f"ВОПРОС {i}/{len(test_questions)}")

        print(f"\n{Colors.BOLD}Тема:{Colors.END} {question['topic']}")
        print(f"{Colors.BOLD}Подтема:{Colors.END} {question.get('subtopic_name', '')}")

        print(f"\n{Colors.BOLD}{question['question']}{Colors.END}")

        for j, option in enumerate(question['options'], 1):
            print(f"  {Colors.CYAN}{j}.{Colors.END} {option}")

        while True:
            try:
                answer = int(input(f"\n{Colors.BOLD}Ваш ответ (1-{len(question['options'])}): {Colors.END}").strip())
                if 1 <= answer <= len(question['options']):
                    answers[question['id']] = answer - 1

                    # Показываем обратный отсчет
                    remaining = len(test_questions) - i
                    if remaining > 0:
                        print_info(f"Осталось вопросов: {remaining}")
                    break
                else:
                    print_error(f"Пожалуйста, введите число от 1 до {len(question['options'])}")
            except ValueError:
                print_error("Пожалуйста, введите число")

    return answers


def continue_student_flow(engine):
    """Процесс для существующего студента"""
    print_header("ПРОДОЛЖИТЬ ОБУЧЕНИЕ")

    student_id = input(f"{Colors.BOLD}Введите ваш ID: {Colors.END}").strip()

    progress = engine.get_student_progress(student_id)
    if "error" in progress:
        print_error(f"Студент с ID '{student_id}' не найден.")
        return

    print_success(f"Добро пожаловать, {student_id}!")

    # Показываем статистику
    show_student_stats(progress)

    input(f"\n{Colors.BOLD}Нажмите Enter чтобы продолжить обучение...{Colors.END}")
    start_learning_flow(engine, student_id)


def start_learning_flow(engine, student_id):
    """Процесс изучения тем"""
    while True:
        print_header("ОБУЧЕНИЕ")

        # Получаем следующую тему
        next_content = engine.get_next_content(student_id)

        if "error" in next_content:
            print_error(next_content["error"])
            break

        content = next_content["content"]
        topic_info = next_content["topic_info"]
        progress = next_content["progress"]

        # Показываем прогресс
        print(f"\n{Colors.BOLD}Тема {progress['current_topic']} из {progress['total_topics']}{Colors.END}")
        print_progress("Прогресс по пути", progress['current_topic'] - 1, progress['total_topics'])
        from src.core.learning_engine import AdaptiveLearningEngine
        from src.data.knowledge_base import SPECIALIZATIONS
        # Счетчик дней подряд
        if progress.get('streak_days', 1) > 1:
            print_info(f"🔥 Дней обучения подряд: {progress['streak_days']}")

        print(f"\n{Colors.BOLD}Тема:{Colors.END} {content['topic']}")
        print(f"{Colors.BOLD}Подтема:{Colors.END} {content['subtopic_name']}")

        level_color = {
            'beginner': Colors.GREEN,
            'intermediate': Colors.YELLOW,
            'advanced': Colors.RED
        }.get(content['level'], Colors.WHITE)

        print(f"{Colors.BOLD}Уровень:{Colors.END} {level_color}{content['level'].upper()}{Colors.END}")
        print(f"{Colors.BOLD}Примерное время:{Colors.END} {content['estimated_time']} мин")

        # Показываем контент
        print(f"\n{Colors.BOLD}Теория:{Colors.END}")
        print(content['content'][:500] + "..." if len(content['content']) > 500 else content['content'])

        # Показываем применение для специализации
        specialization = engine.student_progress[student_id]["specialization"]
        if specialization in content["specializations"]:
            print(f"\n{Colors.BOLD}💡 Применение в {SPECIALIZATIONS[specialization]}:{Colors.END}")
            print(content["specializations"][specialization])

        # Вопросы для закрепления
        if content.get('practice_questions'):
            print(f"\n{Colors.BOLD}Вопросы для закрепления:{Colors.END}")

            answers = []
            for i, question in enumerate(content['practice_questions'], 1):
                print(f"\n{Colors.BOLD}{i}. {question['text']}{Colors.END}")

                for j, option in enumerate(question['options'], 1):
                    print(f"  {j}. {option}")

                while True:
                    try:
                        answer = int(input(f"\nВаш ответ: ").strip())
                        if 1 <= answer <= len(question['options']):
                            answers.append(answer - 1)
                            break
                        else:
                            print_error(f"Введите число от 1 до {len(question['options'])}")
                    except ValueError:
                        print_error("Пожалуйста, введите число")

            # Проверяем ответы
            animate_loading("Проверка ваших ответов")
            quiz_result = engine.submit_topic_quiz(
                student_id,
                content['topic_id'],
                content['subtopic_id'],
                answers
            )

            if quiz_result.get("success"):
                print_header("РЕЗУЛЬТАТЫ ТЕСТА")
                print(f"\n{Colors.BOLD}Правильных ответов:{Colors.END} {quiz_result['correct']}/{quiz_result['total']}")
                print(f"{Colors.BOLD}Балл:{Colors.END} {quiz_result['score']:.1f}%")

                if quiz_result['score'] >= 60:
                    print_success("Отлично! Тема освоена!")

                    # Показываем достижения
                    student = engine.student_progress[student_id]
                    if student.get("achievements"):
                        last_achievement = student["achievements"][-1]
                        print_info(f"🎉 Получено достижение: {last_achievement['description']}")

                    # Предлагаем продолжить
                    print(f"\n{Colors.BOLD}Что дальше?{Colors.END}")
                    print(f"  1. Следующая тема")
                    print(f"  2. Вернуться в меню")

                    choice = input(f"\nВаш выбор (1-2): ").strip()
                    if choice == "2":
                        break
                    # Если выбор 1 или другой - продолжаем цикл
                else:
                    print_warning("Нужно повторить тему. Рекомендуем изучить материал еще раз.")
                    input(f"\n{Colors.BOLD}Нажмите Enter чтобы повторить тему...{Colors.END}")
                    continue
            else:
                print_error("Ошибка при проверке теста")
                break

        else:
            print_warning("Для этой темы нет вопросов для закрепления.")
            input(f"\n{Colors.BOLD}Нажмите Enter чтобы продолжить...{Colors.END}")


def view_progress_flow(engine):
    """Просмотр прогресса"""
    print_header("МОЙ ПРОГРЕСС")

    student_id = input(f"{Colors.BOLD}Введите ID студента: {Colors.END}").strip()

    progress = engine.get_student_progress(student_id)
    if "error" in progress:
        print_error(f"Студент с ID '{student_id}' не найден.")
        return

    print_success(f"Прогресс студента: {student_id}")
    print(f"\n{Colors.BOLD}📊 Общая статистика:{Colors.END}")
    from src.core.learning_engine import AdaptiveLearningEngine
    from src.data.knowledge_base import SPECIALIZATIONS
    from src.data.knowledge_base import THEORY_DATABASE
    # Основная статистика
    print(f"  • Специализация: {SPECIALIZATIONS.get(progress.get('specialization', 'Не указана'))}")
    print(f"  • Уровень знаний: {progress.get('current_level', 'Не определен').upper()}")

    # Прогресс
    if 'overall_progress_percentage' in progress:
        print_progress("Общий прогресс",
                       progress.get('studied_topics', []),
                       sum(len(t["subtopics"]) for t in THEORY_DATABASE.values()))

    # Точность
    if 'accuracy_percentage' in progress:
        accuracy = progress['accuracy_percentage']
        accuracy_color = Colors.GREEN if accuracy >= 80 else Colors.YELLOW if accuracy >= 60 else Colors.RED
        print(f"  • Точность ответов: {accuracy_color}{accuracy:.1f}%{Colors.END}")

    # Активность
    print(f"  • Вопросов отвечено: {progress.get('total_questions_answered', 0)}")
    print(f"  • Правильных ответов: {progress.get('total_correct_answers', 0)}")
    print(f"  • Дней подряд: {progress.get('streak_days', 1)}")

    # Изученные темы
    studied = progress.get('studied_topics', [])
    if studied:
        print(f"\n{Colors.BOLD}📚 Изученные темы ({len(studied)}):{Colors.END}")
        for i, topic in enumerate(studied[:5], 1):  # Показываем только 5
            score_color = Colors.GREEN if topic.get('score', 0) >= 0.7 else Colors.YELLOW
            print(
                f"  {i}. {topic.get('subtopic_id', 'Тема')} - {score_color}{topic.get('score', 0) * 100:.0f}%{Colors.END}")

        if len(studied) > 5:
            print(f"  ... и еще {len(studied) - 5} тем")

    # Достижения
    achievements = progress.get('achievements', [])
    if achievements:
        print(f"\n{Colors.BOLD}🏆 Достижения ({len(achievements)}):{Colors.END}")
        for ach in achievements[-3:]:  # Последние 3 достижения
            print(f"  • {ach.get('description', 'Достижение')}")

    # Рекомендации
    recommendations = engine.get_recommendations(student_id)
    if recommendations:
        print(f"\n{Colors.BOLD}🎯 Рекомендации:{Colors.END}")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"  {i}. {rec.get('subtopic_name', 'Тема')}")
            print(f"     {rec.get('specialization_application', '')[:80]}...")

    input(f"\n{Colors.BOLD}Нажмите Enter чтобы вернуться...{Colors.END}")


def show_student_stats(progress):
    """Показывает статистику студента"""
    print(f"\n{Colors.BOLD}📈 Ваша статистика:{Colors.END}")

    # Базовые показатели
    stats = [
        ("Уровень", progress.get('current_level', 'Не определен').upper()),
        ("Изучено тем", len(progress.get('studied_topics', []))),
        ("Дней подряд", progress.get('streak_days', 1)),
        ("Вопросов отвечено", progress.get('total_questions_answered', 0)),
    ]

    for label, value in stats:
        print(f"  • {label}: {Colors.CYAN}{value}{Colors.END}")

    # Прогресс-бар общего прогресса
    if 'overall_progress_percentage' in progress:
        percentage = progress['overall_progress_percentage']
        print(f"\n  • Общий прогресс: {progress_bar(percentage)}")


if __name__ == "__main__":
    main()