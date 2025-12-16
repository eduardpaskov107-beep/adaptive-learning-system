"""
Основной движок системы обучения
"""

import json
import os
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from src.models.knowledge_assessment import SimpleKnowledgeAssessor
from src.data.knowledge_base import THEORY_DATABASE, SPECIALIZATIONS, INITIAL_TEST_QUESTIONS


class AdaptiveLearningEngine:
    """
    Основной класс системы адаптивного обучения
    """

    def __init__(self):
        self.assessor = SimpleKnowledgeAssessor()
        self.student_progress = {}
        self.load_progress()

    def start_assessment(self, student_id: str, specialization: str) -> Dict:
        """
        Начинает процесс оценки для нового студента
        """
        # Проверяем, есть ли уже такой студент
        if student_id in self.student_progress:
            print(f"Добро пожаловать, {student_id}! Продолжаем обучение.")
            return self.get_next_content(student_id)

        test = self._generate_initial_test()

        self.student_progress[student_id] = {
            "student_id": student_id,
            "specialization": specialization,
            "current_level": "unknown",
            "assessment": None,
            "recommendations": [],
            "studied_topics": [],
            "learning_path": [],
            "current_topic_index": 0,
            "start_date": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "total_questions_answered": 0,
            "total_correct_answers": 0,
            "streak_days": 1,
            "last_study_date": datetime.now().isoformat(),
            "achievements": []
        }

        return {
            "student_id": student_id,
            "test": test,
            "specialization": specialization,
            "message": f"Пройдите начальный тест из {len(test)} вопросов для определения вашего уровня"
        }

    def _generate_initial_test(self) -> List[Dict]:
        """
        Генерирует начальный тест для определения уровня
        """
        test = []

        # Собираем вопросы по уровням
        questions_by_level = {"beginner": [], "intermediate": [], "advanced": []}

        for topic_id, topic_data in THEORY_DATABASE.items():
            for subtopic_id, subtopic_data in topic_data["subtopics"].items():
                level = subtopic_data["level"]
                if level in questions_by_level and subtopic_data["questions"]:
                    for i, question in enumerate(subtopic_data["questions"]):
                        questions_by_level[level].append({
                            "id": f"{topic_id}_{subtopic_id}_q{i}",
                            "topic": topic_data["topic"],
                            "subtopic": subtopic_id,
                            "subtopic_name": subtopic_data.get("name", subtopic_id),
                            "question": question["text"],
                            "options": question["options"],
                            "correct_answer": question["correct"],
                            "level": level
                        })

        # Выбираем вопросы по квотам
        for level, count in INITIAL_TEST_QUESTIONS.items():
            if questions_by_level[level]:
                selected = random.sample(questions_by_level[level],
                                         min(count, len(questions_by_level[level])))
                test.extend(selected)

        # Перемешиваем вопросы
        random.shuffle(test)
        return test[:10]  # Ограничиваем 10 вопросами

    def submit_assessment(self, student_id: str, answers: Dict[str, int]) -> Dict:
        """
        Принимает ответы на тест и возвращает рекомендации
        """
        if student_id not in self.student_progress:
            return {"error": "Студент не найден"}

        # Группируем ответы по темам и проверяем правильность
        topic_answers = {}
        correct_answers = 0
        total_questions = len(answers)

        for q_id, answer in answers.items():
            try:
                # Разбираем ID вопроса вида: python_basics_variables_q0
                # Где:
                #   python_basics - topic_id
                #   variables - subtopic_id
                #   q0 - номер вопроса (q + number)

                parts = q_id.split("_")

                # Определяем topic_id и subtopic_id
                if len(parts) >= 3:
                    # Находим где начинается q (номер вопроса)
                    q_index = -1
                    for i, part in enumerate(parts):
                        if part.startswith('q'):
                            q_index = i
                            break

                    if q_index > 0:
                        # topic_id может состоять из нескольких частей (python_basics)
                        topic_id = "_".join(parts[:q_index - 1])
                        subtopic_id = parts[q_index - 1]

                        # Извлекаем номер вопроса
                        question_part = parts[q_index]  # например 'q0'
                        question_num = int(question_part[1:])  # убираем 'q', оставляем число
                    else:
                        # Простая структура: topic_subtopic_qN
                        topic_id = parts[0]
                        subtopic_id = parts[1]
                        question_part = parts[2]
                        question_num = int(question_part[1:])
                else:
                    # Резервный вариант
                    topic_id = parts[0] if len(parts) > 0 else ""
                    subtopic_id = parts[1] if len(parts) > 1 else ""
                    question_num = 0

                # Получаем правильный ответ из базы знаний
                correct_answer = None
                if (topic_id in THEORY_DATABASE and
                        subtopic_id in THEORY_DATABASE[topic_id]["subtopics"]):
                    questions = THEORY_DATABASE[topic_id]["subtopics"][subtopic_id]["questions"]
                    if question_num < len(questions):
                        correct_answer = questions[question_num]["correct"]

                # Проверяем ответ
                topic_key = f"{topic_id}_{subtopic_id}"
                if topic_key not in topic_answers:
                    topic_answers[topic_key] = []

                is_correct = (answer == correct_answer) if correct_answer is not None else False
                topic_answers[topic_key].append(1 if is_correct else 0)

                if is_correct:
                    correct_answers += 1

            except (ValueError, IndexError) as e:
                print(f"Ошибка обработки вопроса {q_id}: {e}")
                # Добавляем как неправильный ответ для обработки ошибки
                topic_key = f"unknown_{q_id}"
                if topic_key not in topic_answers:
                    topic_answers[topic_key] = []
                topic_answers[topic_key].append(0)

        # Обновляем статистику
        self.student_progress[student_id]["total_questions_answered"] += total_questions
        self.student_progress[student_id]["total_correct_answers"] += correct_answers

        # Создаем оценку
        assessment = self.assessor.create_initial_assessment(topic_answers)

        # Получаем рекомендации
        specialization = self.student_progress[student_id]["specialization"]
        recommendations = self.assessor.recommend_topics(assessment, specialization)

        # Создаем путь обучения
        learning_path = self._create_learning_path(recommendations, assessment["overall_level"])

        # Обновляем прогресс студента
        self.student_progress[student_id].update({
            "current_level": assessment["overall_level"],
            "assessment": assessment,
            "recommendations": recommendations,
            "learning_path": learning_path,
            "current_topic_index": 0,
            "last_activity": datetime.now().isoformat(),
            "test_score": (correct_answers / total_questions * 100) if total_questions > 0 else 0
        })

        self.save_progress()

        return {
            "student_id": student_id,
            "assessment": assessment,
            "recommendations": recommendations,
            "learning_path": learning_path[:3],  # первые 3 темы пути
            "test_score": (correct_answers / total_questions * 100) if total_questions > 0 else 0,
            "message": f"Ваш уровень: {assessment['overall_level'].upper()}. Найдено {len(recommendations)} тем для изучения."
        }

    def _create_learning_path(self, recommendations: List[Dict], level: str) -> List[Dict]:
        """
        Создает путь обучения на основе рекомендаций
        """
        learning_path = []

        # Группируем темы по уровням сложности
        beginner_topics = []
        intermediate_topics = []
        advanced_topics = []

        for rec in recommendations:
            # Определяем уровень темы по ее названию или другим признакам
            topic_id, subtopic_id = rec["content_link"].split("/")
            if topic_id in THEORY_DATABASE and subtopic_id in THEORY_DATABASE[topic_id]["subtopics"]:
                topic_level = THEORY_DATABASE[topic_id]["subtopics"][subtopic_id]["level"]
                rec["level"] = topic_level

                if topic_level == "beginner":
                    beginner_topics.append(rec)
                elif topic_level == "intermediate":
                    intermediate_topics.append(rec)
                else:
                    advanced_topics.append(rec)

        # Строим путь в зависимости от уровня студента
        if level == "beginner":
            # 70% beginner, 30% intermediate
            learning_path.extend(beginner_topics)
            learning_path.extend(intermediate_topics[:max(1, len(intermediate_topics) // 3)])
        elif level == "intermediate":
            # 50% intermediate, 30% beginner (для повторения), 20% advanced
            learning_path.extend(intermediate_topics)
            learning_path.extend(beginner_topics[:max(1, len(beginner_topics) // 3)])
            learning_path.extend(advanced_topics[:max(1, len(advanced_topics) // 5)])
        else:  # advanced
            # 60% advanced, 40% intermediate (для закрепления)
            learning_path.extend(advanced_topics)
            learning_path.extend(intermediate_topics[:max(2, len(intermediate_topics) // 2)])

        # Ограничиваем путь 15 темами
        return learning_path[:15]

    def get_next_content(self, student_id: str) -> Dict:
        """
        Возвращает следующий контент для изучения
        """
        if student_id not in self.student_progress:
            return {"error": "Студент не найден"}

        student = self.student_progress[student_id]

        # Проверяем streak
        self._update_streak(student_id)

        # Получаем следующую тему
        if not student.get("learning_path"):
            # Если пути нет, создаем новый
            if student.get("assessment"):
                recommendations = self.assessor.recommend_topics(
                    student["assessment"],
                    student["specialization"]
                )
                learning_path = self._create_learning_path(
                    recommendations,
                    student["current_level"]
                )
                student["learning_path"] = learning_path
                student["current_topic_index"] = 0
            else:
                return {"error": "Нет данных для обучения"}

        current_index = student.get("current_topic_index", 0)

        if current_index >= len(student["learning_path"]):
            # Пройден весь путь, создаем новый
            recommendations = self.assessor.recommend_topics(
                student["assessment"],
                student["specialization"]
            )
            student["learning_path"] = self._create_learning_path(
                recommendations,
                student["current_level"]
            )
            student["current_topic_index"] = 0
            current_index = 0

            # Добавляем достижение
            self._add_achievement(student_id, "path_completed",
                                  "🎓 Завершён первый учебный путь!")

        # Получаем текущую тему
        current_topic = student["learning_path"][current_index]
        topic_id, subtopic_id = current_topic["content_link"].split("/")

        # Получаем контент
        content = self.get_topic_content(topic_id, subtopic_id)

        if not content:
            return {"error": "Контент не найден"}

        # Добавляем информацию о прогрессе
        content["progress"] = {
            "current_topic": current_index + 1,
            "total_topics": len(student["learning_path"]),
            "percentage": ((current_index) / len(student["learning_path"]) * 100)
            if student["learning_path"] else 0,
            "studied_topics": len(student.get("studied_topics", [])),
            "streak_days": student.get("streak_days", 1)
        }

        return {
            "student_id": student_id,
            "content": content,
            "topic_info": current_topic,
            "progress": content["progress"],
            "message": f"Тема {current_index + 1} из {len(student['learning_path'])}"
        }

    def get_topic_content(self, topic_id: str, subtopic_id: str) -> Optional[Dict]:
        """
        Возвращает контент для изучения темы
        """
        if topic_id in THEORY_DATABASE and subtopic_id in THEORY_DATABASE[topic_id]["subtopics"]:
            content_data = THEORY_DATABASE[topic_id]["subtopics"][subtopic_id]

            # Добавляем дополнительные материалы в зависимости от специализации
            specialization_content = self._get_specialization_content(
                topic_id, subtopic_id, content_data
            )

            return {
                "topic_id": topic_id,
                "topic": THEORY_DATABASE[topic_id]["topic"],
                "subtopic_id": subtopic_id,
                "subtopic_name": content_data.get("name", subtopic_id),
                "level": content_data["level"],
                "content": content_data["content"],
                "practice_questions": content_data["questions"],
                "specializations": content_data.get("specializations", {}),
                "specialization_content": specialization_content,
                "estimated_time": self._estimate_study_time(content_data["content"]),
                "related_topics": self._get_related_topics(topic_id, subtopic_id)
            }

        return None

    def _get_specialization_content(self, topic_id: str, subtopic_id: str,
                                    content_data: Dict) -> Dict:
        """
        Возвращает дополнительный контент для специализации
        """
        specialization_content = {
            "examples": [],
            "projects": [],
            "resources": []
        }

        # Примеры кода для разных специализаций
        if topic_id == "python_basics" and subtopic_id == "variables":
            specialization_content["examples"] = [
                {
                    "data_science": "df = pd.read_csv('data.csv')  # DataFrame для анализа",
                    "web_dev": "user_session = {}  # Словарь для данных сессии",
                    "bioinformatics": "dna_sequence = 'ATCG'  # Последовательность ДНК"
                }
            ]

        # Мини-проекты
        if topic_id == "python_basics" and subtopic_id == "lists":
            specialization_content["projects"] = [
                {
                    "title": "Мини-проект",
                    "data_science": "Создайте список из 100 случайных чисел и посчитайте статистику",
                    "web_dev": "Создайте список пользователей и реализуйте поиск по имени",
                    "bioinformatics": "Создайте список генетических последовательностей и найдите паттерны"
                }
            ]

        # Дополнительные ресурсы
        specialization_content["resources"] = [
            {
                "type": "Документация",
                "link": "https://docs.python.org/3/tutorial/introduction.html"
            }
        ]

        return specialization_content

    def _estimate_study_time(self, content: str) -> int:
        """
        Оценивает время изучения в минутах
        """
        words = len(content.split())
        return max(5, min(30, words // 50))  # 5-30 минут

    def _get_related_topics(self, topic_id: str, subtopic_id: str) -> List[Dict]:
        """
        Возвращает связанные темы
        """
        related = []

        if topic_id == "python_basics":
            if subtopic_id == "variables":
                related.append({"topic": "functions", "subtopic": "basic_functions",
                                "reason": "Переменные используются в функциях"})
            elif subtopic_id == "lists":
                related.append({"topic": "python_basics", "subtopic": "variables",
                                "reason": "Списки - это тип данных переменных"})

        return related

    def submit_topic_quiz(self, student_id: str, topic_id: str, subtopic_id: str,
                          answers: List[int]) -> Dict:
        """
        Принимает ответы на quiz по теме и обновляет прогресс
        """
        if student_id not in self.student_progress:
            return {"error": "Студент не найден"}

        # Получаем правильные ответы
        if (topic_id in THEORY_DATABASE and
                subtopic_id in THEORY_DATABASE[topic_id]["subtopics"]):
            questions = THEORY_DATABASE[topic_id]["subtopics"][subtopic_id]["questions"]

            # Проверяем ответы
            correct = 0
            for i, (question, answer) in enumerate(zip(questions, answers)):
                if i < len(answers) and answer == question["correct"]:
                    correct += 1

            score = correct / len(questions) if questions else 0

            # Отмечаем тему как изученную
            result = self.mark_topic_completed(student_id, topic_id, subtopic_id, score)

            # Переходим к следующей теме
            student = self.student_progress[student_id]
            student["current_topic_index"] += 1

            # Обновляем статистику
            student["total_questions_answered"] += len(questions)
            student["total_correct_answers"] += correct

            # Проверяем достижения
            self._check_achievements(student_id)

            self.save_progress()

            return {
                "success": True,
                "score": score * 100,
                "correct": correct,
                "total": len(questions),
                "message": f"Результат: {correct}/{len(questions)} ({score * 100:.1f}%)",
                "next_topic": self.get_next_content(student_id) if score >= 0.6 else None
            }

        return {"error": "Тема не найдена"}

    def mark_topic_completed(self, student_id: str, topic_id: str, subtopic_id: str,
                             quiz_score: float) -> Dict:
        """
        Отмечает тему как изученную
        """
        if student_id not in self.student_progress:
            return {"error": "Студент не найден"}

        student = self.student_progress[student_id]
        topic_key = f"{topic_id}_{subtopic_id}"

        # Проверяем, не изучали ли уже эту тему
        if not any(t["topic"] == topic_key for t in student.get("studied_topics", [])):
            studied_topic = {
                "topic": topic_key,
                "topic_id": topic_id,
                "subtopic_id": subtopic_id,
                "completed_date": datetime.now().isoformat(),
                "score": quiz_score,
                "retake_count": 0
            }

            student.setdefault("studied_topics", []).append(studied_topic)

            # Обновляем оценку знаний
            if student.get("assessment") and "topic_scores" in student["assessment"]:
                student["assessment"]["topic_scores"][topic_key] = quiz_score * 100

            # Обновляем последнюю дату изучения
            student["last_study_date"] = datetime.now().isoformat()

            return {
                "success": True,
                "message": f"Тема '{subtopic_id}' отмечена как изученная!",
                "total_studied": len(student["studied_topics"])
            }

        # Если тема уже изучена, увеличиваем счетчик повторений
        for topic in student.get("studied_topics", []):
            if topic["topic"] == topic_key:
                topic["retake_count"] = topic.get("retake_count", 0) + 1
                topic["last_retake_date"] = datetime.now().isoformat()
                break

        return {
            "success": True,
            "message": f"Тема '{subtopic_id}' повторена!",
            "total_studied": len(student["studied_topics"])
        }

    def _update_streak(self, student_id: str):
        """
        Обновляет счетчик дней подряд обучения
        """
        student = self.student_progress[student_id]
        last_date = datetime.fromisoformat(student.get("last_study_date",
                                                       student["start_date"]))
        current_date = datetime.now()

        # Если разница в днях = 1, увеличиваем streak
        if (current_date.date() - last_date.date()).days == 1:
            student["streak_days"] = student.get("streak_days", 1) + 1
        elif (current_date.date() - last_date.date()).days > 1:
            # Слишком большой перерыв, сбрасываем streak
            student["streak_days"] = 1

        # Обновляем дату
        student["last_study_date"] = current_date.isoformat()

        # Проверяем достижения по streak
        if student["streak_days"] >= 7:
            self._add_achievement(student_id, "week_streak",
                                  "🔥 Неделя обучения без перерыва!")
        if student["streak_days"] >= 30:
            self._add_achievement(student_id, "month_streak",
                                  "🏆 Месяц регулярного обучения!")

    def _add_achievement(self, student_id: str, achievement_id: str,
                         description: str):
        """
        Добавляет достижение студенту
        """
        student = self.student_progress[student_id]

        if not any(a["id"] == achievement_id for a in student.get("achievements", [])):
            achievement = {
                "id": achievement_id,
                "description": description,
                "date_earned": datetime.now().isoformat()
            }
            student.setdefault("achievements", []).append(achievement)

    def _check_achievements(self, student_id: str):
        """
        Проверяет и добавляет достижения
        """
        student = self.student_progress[student_id]

        # Достижение за количество изученных тем
        studied_count = len(student.get("studied_topics", []))
        if studied_count >= 5 and not any(a["id"] == "5_topics"
                                          for a in student.get("achievements", [])):
            self._add_achievement(student_id, "5_topics",
                                  "📚 Изучено 5 тем!")
        if studied_count >= 10 and not any(a["id"] == "10_topics"
                                           for a in student.get("achievements", [])):
            self._add_achievement(student_id, "10_topics",
                                  "🎓 Изучено 10 тем!")

        # Достижение за точность
        total_questions = student.get("total_questions_answered", 0)
        correct_answers = student.get("total_correct_answers", 0)
        if total_questions >= 20:
            accuracy = correct_answers / total_questions if total_questions > 0 else 0
            if accuracy >= 0.8 and not any(a["id"] == "high_accuracy"
                                           for a in student.get("achievements", [])):
                self._add_achievement(student_id, "high_accuracy",
                                      "🎯 Высокая точность ответов (80%+)")

    def get_student_progress(self, student_id: str) -> Dict:
        """
        Возвращает прогресс студента
        """
        if student_id in self.student_progress:
            student = self.student_progress[student_id].copy()

            # Рассчитываем прогресс
            total_topics = sum(len(t["subtopics"]) for t in THEORY_DATABASE.values())
            studied_count = len(student.get("studied_topics", []))
            student["overall_progress_percentage"] = (studied_count / total_topics * 100) \
                if total_topics > 0 else 0

            # Рассчитываем точность
            total_q = student.get("total_questions_answered", 0)
            correct_q = student.get("total_correct_answers", 0)
            student["accuracy_percentage"] = (correct_q / total_q * 100) \
                if total_q > 0 else 0

            # Информация о текущем пути
            learning_path = student.get("learning_path", [])
            current_index = student.get("current_topic_index", 0)
            if learning_path and current_index < len(learning_path):
                student["current_topic"] = learning_path[current_index]
                student["path_progress"] = {
                    "current": current_index + 1,
                    "total": len(learning_path),
                    "percentage": (current_index / len(learning_path) * 100)
                    if learning_path else 0
                }

            return student

        return {"error": "Студент не найден"}

    def get_recommendations(self, student_id: str) -> List[Dict]:
        """
        Возвращает персональные рекомендации
        """
        if student_id not in self.student_progress:
            return []

        student = self.student_progress[student_id]

        if not student.get("assessment"):
            return []

        # Базовые рекомендации на основе оценок
        recommendations = self.assessor.recommend_topics(
            student["assessment"],
            student["specialization"]
        )

        # Добавляем рекомендации на основе истории изучения
        studied_topics = {t["topic"] for t in student.get("studied_topics", [])}

        enhanced_recs = []
        for rec in recommendations:
            topic_key = rec["content_link"].replace("/", "_")

            if topic_key not in studied_topics:
                # Добавляем дополнительную информацию
                topic_id, subtopic_id = rec["content_link"].split("/")
                if topic_id in THEORY_DATABASE and subtopic_id in THEORY_DATABASE[topic_id]["subtopics"]:
                    topic_data = THEORY_DATABASE[topic_id]["subtopics"][subtopic_id]
                    rec["estimated_time"] = self._estimate_study_time(topic_data["content"])
                    rec["level"] = topic_data["level"]
                    rec["prerequisites"] = self._get_prerequisites(topic_id, subtopic_id)

                    enhanced_recs.append(rec)

        return enhanced_recs[:5]  # Топ-5 рекомендаций

    def _get_prerequisites(self, topic_id: str, subtopic_id: str) -> List[str]:
        """
        Возвращает предварительные требования для темы
        """
        prerequisites = []

        if topic_id == "functions" and subtopic_id == "basic_functions":
            prerequisites.append("Переменные и типы данных")
            prerequisites.append("Основные операторы")

        elif topic_id == "oop" and subtopic_id == "classes":
            prerequisites.append("Функции")
            prerequisites.append("Списки и словари")

        return prerequisites

    def save_progress(self, filepath: str = "data/student_progress.json"):
        """
        Сохраняет прогресс всех студентов
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Преобразуем datetime в строки
        serializable_progress = {}
        for student_id, data in self.student_progress.items():
            serializable_data = data.copy()
            # Убеждаемся, что все даты - строки
            for key, value in data.items():
                if isinstance(value, datetime):
                    serializable_data[key] = value.isoformat()
            serializable_progress[student_id] = serializable_data

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_progress, f, ensure_ascii=False, indent=2)

    def load_progress(self, filepath: str = "data/student_progress.json"):
        """
        Загружает прогресс студентов
        """
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.student_progress = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.student_progress = {}
        else:
            self.student_progress = {}