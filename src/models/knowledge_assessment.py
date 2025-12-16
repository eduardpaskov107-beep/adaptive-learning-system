"""
Модель для оценки уровня знаний студента
"""

from typing import Dict, List, Optional
import json


class SimpleKnowledgeAssessor:
    """
    Упрощенный класс для оценки знаний студента на основе тестов
    """

    def __init__(self):
        self.student_profiles = {}

    def create_initial_assessment(self, answers: Dict[str, List[int]]) -> Dict:
        """
        Создает начальную оценку знаний на основе ответов на тест
        """
        assessment = {
            "overall_level": "beginner",
            "topic_scores": {},
            "weak_topics": [],
            "strong_topics": [],
            "overall_score": 0
        }

        total_correct = 0
        total_questions = 0

        for topic, answer_list in answers.items():
            if not answer_list:
                continue

            # Оценка по теме (0-100%)
            correct = sum(answer_list)  # ответы уже 0/1
            score = (correct / len(answer_list)) * 100 if answer_list else 0
            assessment["topic_scores"][topic] = score

            # Определяем уровень по теме
            if score >= 80:
                assessment["strong_topics"].append(topic)
            elif score < 50:
                assessment["weak_topics"].append(topic)

            total_correct += correct
            total_questions += len(answer_list)

        # Общий уровень
        if total_questions > 0:
            overall_score = (total_correct / total_questions) * 100
            assessment["overall_score"] = overall_score

            if overall_score >= 75:
                assessment["overall_level"] = "advanced"
            elif overall_score >= 40:
                assessment["overall_level"] = "intermediate"
            else:
                assessment["overall_level"] = "beginner"

        return assessment

    def recommend_topics(self, assessment: Dict, specialization: str) -> List[Dict]:
        """
        Рекомендует темы для изучения на основе оценки и специализации
        """
        recommendations = []

        # Импортируем тут, чтобы избежать циклических импортов
        from src.data.knowledge_base import THEORY_DATABASE

        for topic_id, topic_data in THEORY_DATABASE.items():
            for subtopic_id, subtopic_data in topic_data["subtopics"].items():
                topic_key = f"{topic_id}_{subtopic_id}"
                score = assessment["topic_scores"].get(topic_key, 0)

                # Если знание темы ниже 70%
                if score < 70:
                    # Берем текст специализации или заглушку
                    specialization_text = subtopic_data.get("specializations", {}).get(
                        specialization,
                        f"Эта тема важна для вашей специализации ({specialization})."
                    )

                    recommendations.append({
                        "topic": topic_data["topic"],
                        "subtopic": subtopic_id,
                        "subtopic_name": subtopic_data.get("name", subtopic_id),
                        "priority": 100 - score,
                        "current_score": score,
                        "specialization_application": specialization_text,
                        "content_link": f"{topic_id}/{subtopic_id}"
                    })

        # Сортируем по приоритету и берем топ-5
        recommendations.sort(key=lambda x: x["priority"], reverse=True)
        return recommendations[:5]

    def update_assessment(self, student_id: str, new_answers: Dict) -> Dict:
        """
        Обновляет оценку знаний студента
        """
        if student_id not in self.student_profiles:
            self.student_profiles[student_id] = self.create_initial_assessment(new_answers)
        else:
            # Простая логика обновления
            old_assessment = self.student_profiles[student_id]
            new_assessment = self.create_initial_assessment(new_answers)

            # Объединяем оценки
            for topic in new_assessment["topic_scores"]:
                if topic in old_assessment["topic_scores"]:
                    new_assessment["topic_scores"][topic] = (
                            old_assessment["topic_scores"][topic] * 0.3 +
                            new_assessment["topic_scores"][topic] * 0.7
                    )

            self.student_profiles[student_id] = new_assessment

        return self.student_profiles[student_id]