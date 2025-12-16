"""
Основной движок системы обучения
"""

import json
from typing import Dict, List, Optional
from datetime import datetime

from src.models.knowledge_assessment import KnowledgeAssessor
from src.data.knowledge_base import THEORY_DATABASE, SPECIALIZATIONS


class AdaptiveLearningEngine:
    """
    Основной класс системы адаптивного обучения
    """
    
    def __init__(self):
        self.assessor = KnowledgeAssessor()
        self.student_progress = {}
        
    def start_assessment(self, student_id: str, specialization: str) -> Dict:
        """
        Начинает процесс оценки для нового студента
        
        Args:
            student_id: Уникальный идентификатор студента
            specialization: Специализация студента
        
        Returns:
            Начальный тест
        """
        test = self._generate_initial_test()
        
        self.student_progress[student_id] = {
            "specialization": specialization,
            "current_level": "unknown",
            "assessment": None,
            "recommendations": [],
            "studied_topics": [],
            "start_date": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        return {
            "student_id": student_id,
            "test": test,
            "specialization": specialization,
            "message": "Пройдите начальный тест для определения вашего уровня"
        }
    
    def _generate_initial_test(self) -> List[Dict]:
        """
        Генерирует начальный тест для определения уровня
        """
        test = []
        
        # Выбираем по 2 вопроса из каждой темы начального уровня
        for topic_id, topic_data in THEORY_DATABASE.items():
            for subtopic_id, subtopic_data in topic_data["subtopics"].items():
                if subtopic_data["level"] == "beginner" and len(subtopic_data["questions"]) >= 2:
                    for i, question in enumerate(subtopic_data["questions"][:2]):
                        test.append({
                            "id": f"{topic_id}_{subtopic_id}_q{i}",
                            "topic": topic_data["topic"],
                            "subtopic": subtopic_id,
                            "question": question["text"],
                            "options": question["options"],
                            "correct_answer": question["correct"]
                        })
        
        return test[:10]  # Ограничиваем 10 вопросами
    
    def submit_assessment(self, student_id: str, answers: Dict[str, int]) -> Dict:
        """
        Принимает ответы на тест и возвращает рекомендации
        
        Args:
            student_id: ID студента
            answers: Ответы на вопросы {question_id: answer_index}
        
        Returns:
            Результаты оценки и рекомендации
        """
        if student_id not in self.student_progress:
            return {"error": "Студент не найден"}
        
        # Группируем ответы по темам
        topic_answers = {}
        for q_id, answer in answers.items():
            topic_key = "_".join(q_id.split("_")[:2])
            if topic_key not in topic_answers:
                topic_answers[topic_key] = []
            topic_answers[topic_key].append(answer)
        
        # Создаем оценку
        assessment = self.assessor.create_initial_assessment(topic_answers)
        
        # Получаем рекомендации
        specialization = self.student_progress[student_id]["specialization"]
        recommendations = self.assessor.recommend_topics(assessment, specialization)
        
        # Обновляем прогресс студента
        self.student_progress[student_id].update({
            "current_level": assessment["overall_level"],
            "assessment": assessment,
            "recommendations": recommendations,
            "last_activity": datetime.now().isoformat()
        })
        
        return {
            "student_id": student_id,
            "assessment": assessment,
            "recommendations": recommendations,
            "message": f"Ваш уровень: {assessment['overall_level'].upper()}. Найдено {len(recommendations)} тем для изучения."
        }
    
    def get_topic_content(self, topic_id: str, subtopic_id: str) -> Optional[Dict]:
        """
        Возвращает контент для изучения темы
        """
        topic_parts = topic_id.split("_")
        main_topic = "_".join(topic_parts[:-1]) if len(topic_parts) > 1 else topic_id
        subtopic = topic_parts[-1] if len(topic_parts) > 1 else subtopic_id
        
        if main_topic in THEORY_DATABASE and subtopic in THEORY_DATABASE[main_topic]["subtopics"]:
            content = THEORY_DATABASE[main_topic]["subtopics"][subtopic]["content"]
            questions = THEORY_DATABASE[main_topic]["subtopics"][subtopic]["questions"]
            
            return {
                "topic": THEORY_DATABASE[main_topic]["topic"],
                "subtopic": subtopic,
                "content": content,
                "practice_questions": questions[:3]  # Первые 3 вопроса для закрепления
            }
        
        return None
    
    def mark_topic_completed(self, student_id: str, topic_id: str, subtopic_id: str, 
                           quiz_score: float) -> Dict:
        """
        Отмечает тему как изученную
        """
        if student_id not in self.student_progress:
            return {"error": "Студент не найден"}
        
        topic_key = f"{topic_id}_{subtopic_id}"
        
        if topic_key not in self.student_progress[student_id]["studied_topics"]:
            self.student_progress[student_id]["studied_topics"].append({
                "topic": topic_key,
                "completed_date": datetime.now().isoformat(),
                "score": quiz_score
            })
        
        # Обновляем оценку знаний
        current_assessment = self.student_progress[student_id]["assessment"]
        if current_assessment and "topic_scores" in current_assessment:
            current_assessment["topic_scores"][topic_key] = quiz_score * 100
        
        return {
            "success": True,
            "message": f"Тема '{subtopic_id}' отмечена как изученная",
            "next_recommendation": self._get_next_recommendation(student_id)
        }
    
    def _get_next_recommendation(self, student_id: str) -> Optional[Dict]:
        """
        Получает следующую рекомендацию для студента
        """
        if student_id in self.student_progress:
            recommendations = self.student_progress[student_id]["recommendations"]
            studied = [t["topic"] for t in self.student_progress[student_id]["studied_topics"]]
            
            for rec in recommendations:
                if rec["content_link"] not in studied:
                    return rec
        
        return None
    
    def get_student_progress(self, student_id: str) -> Dict:
        """
        Возвращает прогресс студента
        """
        if student_id in self.student_progress:
            progress = self.student_progress[student_id].copy()
            
            # Рассчитываем общий прогресс
            total_topics = sum(len(t["subtopics"]) for t in THEORY_DATABASE.values())
            studied_count = len(progress["studied_topics"])
            progress["overall_progress"] = (studied_count / total_topics) * 100
            
            return progress
        
        return {"error": "Студент не найден"}
    
    def save_progress(self, filepath: str = "data/student_progress.json"):
        """
        Сохраняет прогресс всех студентов
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.student_progress, f, ensure_ascii=False, indent=2)
    
    def load_progress(self, filepath: str = "data/student_progress.json"):
        """
        Загружает прогресс студентов
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.student_progress = json.load(f)
        except FileNotFoundError:
            self.student_progress = {}
