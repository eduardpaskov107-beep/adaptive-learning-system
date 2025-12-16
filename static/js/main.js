// Основной JavaScript для системы

document.addEventListener('DOMContentLoaded', function() {
    console.log('Система обучения загружена');

    // ============ ОБРАБОТКА ФОРМ ============
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            console.log('Форма отправлена:', this.action);

            // Для формы регистрации - простой редирект
            if (this.action.includes('/register')) {
                e.preventDefault();

                const studentId = document.getElementById('student_id')?.value;
                if (!studentId) {
                    alert('Пожалуйста, введите ваш ID');
                    return;
                }

                // Показываем загрузку
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Регистрация...';
                submitBtn.disabled = true;

                // Имитация загрузки
                setTimeout(() => {
                    // Отправляем форму
                    this.submit();
                }, 1000);
            }
        });
    });

    // ============ ОБРАБОТКА КНОПОК ============
    document.querySelectorAll('button[data-href]').forEach(btn => {
        btn.addEventListener('click', function() {
            const href = this.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });
    });

    document.querySelectorAll('button[data-action="alert"]').forEach(btn => {
        btn.addEventListener('click', function() {
            const message = this.getAttribute('data-message') || 'Действие выполнено!';
            alert(message);
        });
    });

    // ============ НАВИГАЦИЯ ============
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ============ ТЕСТИРОВАНИЕ ============
    const testSubmitBtn = document.querySelector('#submitTestBtn, button[data-href="/learning"]');
    if (testSubmitBtn && window.location.pathname.includes('/assessment')) {
        testSubmitBtn.addEventListener('click', function(e) {
            // Проверяем, отвечены ли все вопросы
            const answered = document.querySelectorAll('input[type="radio"]:checked').length;
            const totalQuestions = document.querySelectorAll('input[type="radio"][name^="question"]').length / 3;

            if (answered < totalQuestions) {
                alert(`Пожалуйста, ответьте на все вопросы. Отвечено: ${answered}/${totalQuestions}`);
                e.preventDefault();
            }
        });
    }

    // ============ АНИМАЦИИ ============
    // Анимация появления карточек
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});