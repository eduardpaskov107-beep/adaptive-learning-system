#!/usr/bin/env python3
"""
Упрощенная версия Flask приложения
"""

from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'simple-secret-key-123'

# Создаем папки
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/register', methods=['GET'])
def register_get():
    """Страница регистрации"""
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    """Обработка регистрации"""
    student_id = request.form.get('student_id', '').strip()
    specialization = request.form.get('specialization', 'data_science')

    if not student_id:
        return redirect(url_for('register_get'))

    # Сохраняем в сессии
    session['student_id'] = student_id
    session['specialization'] = specialization

    return redirect(url_for('assessment'))


@app.route('/assessment')
def assessment():
    """Страница тестирования"""
    if 'student_id' not in session:
        return redirect(url_for('index'))

    return render_template('assessment.html')


@app.route('/learning')
def learning():
    """Страница обучения"""
    if 'student_id' not in session:
        return redirect(url_for('index'))

    return render_template('learning.html')


@app.route('/profile')
def profile():
    """Страница профиля"""
    if 'student_id' not in session:
        return redirect(url_for('index'))

    return render_template('profile.html')


@app.route('/logout')
def logout():
    """Выход из системы"""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("=" * 60)
    print("🎓 АДАПТИВНАЯ СИСТЕМА ОБУЧЕНИЯ")
    print("=" * 60)
    print("🌐 Сервер запущен: http://localhost:5001")
    print("👉 Откройте браузер и перейдите по адресу")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5001)