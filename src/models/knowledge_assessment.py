
### Шаг 2.2: Модель оценки знаний

**`src/models/knowledge_assessment.py`**
```python
"""
Модель для оценки уровня знаний студента
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sentence_transformers import SentenceTransformer
import json
import pickle


class KnowledgeAssessor:
    """
    Класс для оценки знаний студента на основе тестов
    """
    
    def __init__(self):
        self.model = None
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.student_profiles = {}
        
    def create_initial_assessment(self, answers: Dict[str, List[int]]) -> Dict:
        """
        Создает начальную оценку знаний на основе ответов на тест
        
        Args:
            answers: Словарь с ответами {topic_id: [ответ1, ответ2, ...]}
        
        Returns:
            Оценка знаний студента
        """
        assessment = {
            "overall_level": "beginner",
            "topic_scores": {},
            "weak_topics": [],
            "strong_topics": []
        }
        
        topic_scores = {}
        total_correct = 0
        total_questions = 0
        
        for topic, answer_list in answers.items():
            if not answer_list:
                continue
                
            # Оценка по теме (0-100%)
            correct = sum(1 for ans in answer_list if ans == 0)  # предполагаем 0 как правильный
            score = (correct / len(answer_list)) * 100
            topic_scores[topic] = score
            
            # Определяем уровень по теме
            if score >= 80:
                level = "advanced"
                assessment["strong_topics"].append(topic)
            elif score >= 50:
                level = "intermediate"
            else:
                level = "beginner"
                assessment["weak_topics"].append(topic)
            
            total_correct += correct
            total_questions += len(answer_list)
        
        # Общий уровень
        overall_score = (total_correct / total_questions) * 100 if total_questions > 0 else 0
        
        if overall_score >= 75:
            assessment["overall_level"] = "advanced"
        elif overall_score >= 40:
            assessment["overall_level"] = "intermediate"
        else:
            assessment["overall_level"] = "beginner"
        
        assessment["topic_scores"] = topic_scores
        assessment["overall_score"] = overall_score
        
        return assessment
    
    def recommend_topics(self, assessment: Dict, specialization: str) -> List[Dict]:
        """
        Рекомендует темы для изучения на основе оценки и специализации
        
        Args:
            assessment: Оценка знаний студента
            specialization: Специализация студента
        
        Returns:
            Список рекомендуемых тем с приоритетами
        """
        from src.data.knowledge_base import THEORY_DATABASE
        
        recommendations = []
        
        for topic_id, topic_data in THEORY_DATABASE.items():
            for subtopic_id, subtopic_data in topic_data["subtopics"].items():
                # Проверяем уровень сложности
                if subtopic_data["level"] != assessment["overall_level"]:
                    continue
                
                # Проверяем, нужно ли изучать эту тему
                topic_key = f"{topic_id}_{subtopic_id}"
                score = assessment["topic_scores"].get(topic_key, 0)
                
                if score < 70:  # Если знание темы ниже 70%
                    # Добавляем специализацию в объяснение
                    specialization_text = subtopic_data.get("specializations", {}).get(
                        specialization, 
                        "Эта тема важна для вашей специализации."
                    )
                    
                    recommendations.append({
                        "topic": topic_data["topic"],
                        "subtopic": subtopic_id,
                        "subtopic_name": subtopic_data.get("name", subtopic_id),
                        "priority": 100 - score,  # Чем ниже балл, тем выше приоритет
                        "current_score": score,
                        "specialization_application": specialization_text,
                        "content_link": f"{topic_id}/{subtopic_id}"
                    })
        
        # Сортируем по приоритету
        recommendations.sort(key=lambda x: x["priority"], reverse=True)
        
        return recommendations[:5]  # Топ-5 рекомендаций
    
    def update_assessment(self, student_id: str, new_answers: Dict) -> Dict:
        """
        Обновляет оценку знаний студента после изучения материалов
        
        Args:
            student_id: ID студента
            new_answers: Новые ответы на тесты
        
        Returns:
            Обновленная оценка
        """
        if student_id not in self.student_profiles:
            self.student_profiles[student_id] = self.create_initial_assessment(new_answers)
        else:
            # Логика обновления существующей оценки
            old_assessment = self.student_profiles[student_id]
            new_assessment = self.create_initial_assessment(new_answers)
            
            # Объединяем оценки (можно добавить весовые коэффициенты)
            for topic in new_assessment["topic_scores"]:
                if topic in old_assessment["topic_scores"]:
                    # Среднее значение с весом для новых результатов
                    new_assessment["topic_scores"][topic] = (
                        old_assessment["topic_scores"][topic] * 0.3 + 
                        new_assessment["topic_scores"][topic] * 0.7
                    )
            
            self.student_profiles[student_id] = new_assessment
        
        return self.student_profiles[student_id]
    
    def save_model(self, path: str = "models/knowledge_assessor.pkl"):
        """Сохраняет модель на диск"""
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load_model(cls, path: str = "models/knowledge_assessor.pkl"):
        """Загружает модель с диска"""
        with open(path, 'rb') as f:
            return pickle.load(f)
