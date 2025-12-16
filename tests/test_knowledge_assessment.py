"""
Тесты для модуля оценки знаний
"""

import pytest
import numpy as np
from src.models.knowledge_assessment import KnowledgeAssessor


class TestKnowledgeAssessor:
    """Тесты для класса KnowledgeAssessor"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.assessor = KnowledgeAssessor()
    
    def test_create_initial_assessment(self):
        """Тест создания начальной оценки"""
        answers = {
            "python_basics_variables": [0, 0],  # 2 правильных ответа
            "python_basics_data_types": [1, 0],  # 1 правильный, 1 неправильный
        }
        
        assessment = self.assessor.create_initial_assessment(answers)
        
        assert "overall_level" in assessment
        assert "topic_scores" in assessment
        assert "weak_topics" in assessment
        assert "strong_topics" in assessment
        
        # Проверяем расчет баллов
        assert assessment["topic_scores"]["python_basics_variables"] == 100.0
        assert assessment["topic_scores"]["python_basics_data_types"] == 50.0
    
    def test_recommend_topics(self):
        """Тест рекомендации тем"""
        assessment = {
            "overall_level": "beginner",
            "topic_scores": {
                "python_basics_variables": 30.0,  # Низкий балл
                "python_basics_data_types": 90.0,  # Высокий балл
            },
            "weak_topics": ["python_basics_variables"],
            "strong_topics": ["python_basics_data_types"]
        }
        
        recommendations = self.assessor.recommend_topics(assessment, "data_science")
        
        # Должна быть рекомендована тема с низким баллом
        assert len(recommendations) > 0
        
        # Проверяем наличие специализации
        for rec in recommendations:
            assert "specialization_application" in rec
            assert "data_science" in rec["specialization_application"].lower()
    
    def test_update_assessment(self):
        """Тест обновления оценки"""
        student_id = "test_student_123"
        initial_answers = {"python_basics_variables": [0, 0]}
        
        # Создаем начальную оценку
        initial_assessment = self.assessor.update_assessment(student_id, initial_answers)
        
        # Обновляем с новыми ответами
        new_answers = {"python_basics_variables": [1, 1]}  # Все неправильные
        updated_assessment = self.assessor.update_assessment(student_id, new_answers)
        
        # Проверяем, что оценка обновилась
        assert updated_assessment["topic_scores"]["python_basics_variables"] < 100.0
    
    def test_save_load_model(self, tmp_path):
        """Тест сохранения и загрузки модели"""
        # Сохраняем модель
        save_path = tmp_path / "test_model.pkl"
        self.assessor.save_model(str(save_path))
        
        # Загружаем модель
        loaded_assessor = KnowledgeAssessor.load_model(str(save_path))
        
        # Проверяем, что модель загрузилась
        assert isinstance(loaded_assessor, KnowledgeAssessor)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
