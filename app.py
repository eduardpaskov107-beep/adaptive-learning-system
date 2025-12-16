#!/usr/bin/env python3
"""
Flask веб-приложение для адаптивной системы обучения
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import os
import json
from datetime import datetime

# Импортируем нашу систему обучения
import sys

sys.path.insert(0, os.path.abspath('.'))

from src.core.learning_engine import AdaptiveLearningEngine
from src.data.knowledge_base import THEORY_DATABASE, SPECIALIZATIONS

app = Flask(__name__)
app.secret_key = 'adaptive-learning-secret-key-2024'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = './flask_session'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 час

Session(app)

# Инициализируем движок обучения
engine = AdaptiveLearningEngine()

# Создаем папки если их нет
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('flask_session', exist_ok=True)


# ============ ВАЖНО: УБЕРИТЕ ДУБЛИРОВАНИЕ МАРШРУТОВ ============

@app.route('/')
def index():
    """Главная страница - ОДИН раз определено"""
    if 'student_id' in session:
        # Пользователь уже залогинен
        student_id = session['student_id']
        progress = engine.get_student_progress(student_id)
        return render_template('dashboard.html',
                               student_id=student_id,
                               progress=progress,
                               specializations=SPECIALIZATIONS)

    return render_template('index.html', specializations=SPECIALIZATIONS)


@app.route('/register', methods=['GET'])
def register_page():
    """Страница регистрации (GET)"""
    return render_template('register.html', specializations=SPECIALIZATIONS)


@app.route('/register', methods=['POST'])
def register_post():
    """Обработка регистрации (POST)"""
    student_id = request.form.get('student_id', '').strip()
    specialization = request.form.get('specialization', 'data_science')

    if not student_id:
        return redirect(url_for('register_page'))

    if specialization not in SPECIALIZATIONS:
        specialization = 'data_science'

    # Сохраняем в сессии
    session['student_id'] = student_id
    session['specialization'] = specialization

    # Начинаем оценку
    result = engine.start_assessment(student_id, specialization)

    return redirect(url_for('assessment'))


@app.route('/assessment')
def assessment():
    """Страница тестирования"""
    if 'student_id' not in session:
        return redirect(url_for('index'))

    student_id = session['student_id']
    specialization = session.get('specialization', 'data_science')

    # Получаем или создаем тест
    result = engine.start_assessment(student_id, specialization)

    if 'error' in result:
        return redirect(url_for('index'))

    return render_template('assessment.html',
                           test=result['test'],
                           specializations=SPECIALIZATIONS)


@app.route('/submit_test', methods=['POST'])
def submit_test():
    """Принимает ответы на тест"""
    if 'student_id' not in session:
        return jsonify({'error': 'Студент не найден'}), 401

    student_id = session['student_id']
    answers = request.json.get('answers', {})

    if not answers:
        return jsonify({'error': 'Нет ответов'}), 400

    result = engine.submit_assessment(student_id, answers)

    if 'error' in result:
        return jsonify(result), 400

    # Сохраняем уровень в сессии
    session['current_level'] = result['assessment']['overall_level']

    return jsonify(result)


@app.route('/learning')
def learning():
    """Страница обучения"""
    if 'student_id' not in session:
        return redirect(url_for('index'))

    student_id = session['student_id']

    # Получаем следующую тему
    next_content = engine.get_next_content(student_id)

    if 'error' in next_content:
        # Если ошибка, возвращаем на главную
        return redirect(url_for('index'))

    # Получаем прогресс студента
    progress = engine.get_student_progress(student_id)

    return render_template('learning.html',
                           content=next_content['content'],
                           topic_info=next_content['topic_info'],
                           progress=next_content['progress'],
                           student_progress=progress,
                           specializations=SPECIALIZATIONS)


@app.route('/get_next_topic', methods=['GET'])
def get_next_topic():
    """Возвращает следующую тему в JSON формате"""
    if 'student_id' not in session:
        return jsonify({'error': 'Студент не найден'}), 401

    student_id = session['student_id']
    next_content = engine.get_next_content(student_id)

    return jsonify(next_content)


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    """Принимает ответы на quiz по теме"""
    if 'student_id' not in session:
        return jsonify({'error': 'Студент не найден'}), 401

    student_id = session['student_id']
    data = request.json

    topic_id = data.get('topic_id')
    subtopic_id = data.get('subtopic_id')
    answers = data.get('answers', [])

    if not all([topic_id, subtopic_id]):
        return jsonify({'error': 'Не указана тема'}), 400

    result = engine.submit_topic_quiz(student_id, topic_id, subtopic_id, answers)

    return jsonify(result)


@app.route('/profile')
def profile():
    """Страница профиля студента"""
    if 'student_id' not in session:
        return redirect(url_for('index'))

    student_id = session['student_id']
    progress = engine.get_student_progress(student_id)

    if 'error' in progress:
        return redirect(url_for('index'))

    # Получаем рекомендации
    recommendations = engine.get_recommendations(student_id)

    return render_template('profile.html',
                           progress=progress,
                           recommendations=recommendations,
                           specializations=SPECIALIZATIONS)


@app.route('/dashboard')
def dashboard():
    """Дашборд (синоним для профиля)"""
    return redirect(url_for('profile'))


@app.route('/progress_data')
def progress_data():
    """Возвращает данные о прогрессе в JSON"""
    if 'student_id' not in session:
        return jsonify({'error': 'Студент не найден'}), 401

    student_id = session['student_id']
    progress = engine.get_student_progress(student_id)

    return jsonify(progress)


@app.route('/achievements')
def achievements():
    """Достижения студента"""
    if 'student_id' not in session:
        return jsonify({'error': 'Студент не найден'}), 401

    student_id = session['student_id']
    progress = engine.get_student_progress(student_id)

    if 'error' in progress:
        return jsonify({'error': 'Прогресс не найден'}), 404

    achievements = progress.get('achievements', [])

    return jsonify({
        'achievements': achievements,
        'count': len(achievements)
    })


@app.route('/logout')
def logout():
    """Выход из системы"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    """Административная панель (только для демо)"""
    # Получаем статистику всех студентов
    try:
        with open('data/student_progress.json', 'r', encoding='utf-8') as f:
            all_progress = json.load(f)

        stats = {
            'total_students': len(all_progress),
            'by_specialization': {},
            'by_level': {'beginner': 0, 'intermediate': 0, 'advanced': 0},
            'total_topics_studied': 0
        }

        for student_id, data in all_progress.items():
            spec = data.get('specialization', 'unknown')
            stats['by_specialization'][spec] = stats['by_specialization'].get(spec, 0) + 1

            level = data.get('current_level', 'unknown')
            if level in stats['by_level']:
                stats['by_level'][level] += 1

            studied = data.get('studied_topics', [])
            stats['total_topics_studied'] += len(studied)

        return render_template('admin.html', stats=stats, specializations=SPECIALIZATIONS)

    except FileNotFoundError:
        return render_template('admin.html', stats=None, specializations=SPECIALIZATIONS)


# API endpoints для фронтенда
@app.route('/api/topics')
def api_topics():
    """Возвращает список всех тем"""
    topics_list = []

    for topic_id, topic_data in THEORY_DATABASE.items():
        for subtopic_id, subtopic_data in topic_data['subtopics'].items():
            topics_list.append({
                'id': f"{topic_id}/{subtopic_id}",
                'topic': topic_data['topic'],
                'subtopic': subtopic_data.get('name', subtopic_id),
                'level': subtopic_data['level'],
                'question_count': len(subtopic_data['questions'])
            })

    return jsonify({'topics': topics_list})


@app.route('/api/topic/<path:topic_path>')
def api_topic(topic_path):
    """Возвращает контент конкретной темы"""
    try:
        topic_id, subtopic_id = topic_path.split('/')

        if topic_id in THEORY_DATABASE and subtopic_id in THEORY_DATABASE[topic_id]['subtopics']:
            content_data = THEORY_DATABASE[topic_id]['subtopics'][subtopic_id]

            return jsonify({
                'success': True,
                'topic': THEORY_DATABASE[topic_id]['topic'],
                'subtopic': content_data.get('name', subtopic_id),
                'content': content_data['content'],
                'questions': content_data['questions'],
                'level': content_data['level'],
                'specializations': content_data.get('specializations', {})
            })

        return jsonify({'error': 'Тема не найдена'}), 404

    except ValueError:
        return jsonify({'error': 'Неверный формат темы'}), 400


@app.route('/api/specializations')
def api_specializations():
    """Возвращает список специализаций"""
    return jsonify({'specializations': SPECIALIZATIONS})


# Статические файлы
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/api/check_health')
def api_check_health():
    """Проверка работоспособности API"""
    return jsonify({
        'status': 'ok',
        'service': 'adaptive-learning-system',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Создаем папку для данных если её нет
    os.makedirs('data', exist_ok=True)

    # Запускаем Flask
    print("=" * 60)
    print("🚀 Запуск адаптивной системы обучения")
    print("=" * 60)
    print("🌐 Адрес: http://localhost:5001")
    print("👉 Откройте браузер и перейдите по адресу")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5001)