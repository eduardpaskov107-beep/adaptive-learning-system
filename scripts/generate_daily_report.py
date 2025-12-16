#!/usr/bin/env python3
"""
Скрипт для генерации ежедневного отчета по обучению
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.path.append(str(Path(__file__).parent.parent / 'src'))


def generate_report(date_str: str, format: str = 'markdown'):
    """Генерирует отчет по обучению"""
    
    report_date = datetime.strptime(date_str, '%Y-%m-%d') if date_str != 'today' else datetime.now()
    
    # Создаем папку для отчетов
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)
    
    # Загружаем данные о прогрессе
    progress_file = Path('data/student_progress.json')
    
    if not progress_file.exists():
        print("Файл с прогрессом не найден. Создаем тестовый отчет...")
        report_data = create_sample_report()
    else:
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        report_data = analyze_progress(progress_data, report_date)
    
    # Генерируем отчет в нужном формате
    if format == 'markdown':
        generate_markdown_report(report_data, report_date, reports_dir)
    elif format == 'json':
        generate_json_report(report_data, report_date, reports_dir)
    elif format == 'html':
        generate_html_report(report_data, report_date, reports_dir)
    
    print(f"Отчет сгенерирован: {reports_dir}/report_{report_date.strftime('%Y-%m-%d')}.{format}")


def analyze_progress(progress_data: dict, report_date: datetime) -> dict:
    """Анализирует данные о прогрессе"""
    
    total_students = len(progress_data)
    active_today = 0
    total_topics_studied = 0
    specialization_stats = {}
    level_stats = {'beginner': 0, 'intermediate': 0, 'advanced': 0}
    
    for student_id, data in progress_data.items():
        # Проверяем активность
        last_activity = data.get('last_activity', '')
        if last_activity:
            try:
                last_date = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                if last_date.date() == report_date.date():
                    active_today += 1
            except (ValueError, TypeError):
                pass
        
        # Собираем статистику
        spec = data.get('specialization', 'unknown')
        specialization_stats[spec] = specialization_stats.get(spec, 0) + 1
        
        level = data.get('current_level', 'unknown')
        if level in level_stats:
            level_stats[level] += 1
        
        # Считаем изученные темы
        studied = data.get('studied_topics', [])
        total_topics_studied += len(studied)
    
    return {
        'report_date': report_date.isoformat(),
        'total_students': total_students,
        'active_today': active_today,
        'active_percentage': (active_today / total_students * 100) if total_students > 0 else 0,
        'total_topics_studied': total_topics_studied,
        'avg_topics_per_student': total_topics_studied / total_students if total_students > 0 else 0,
        'specialization_stats': specialization_stats,
        'level_stats': level_stats,
        'most_popular_specialization': max(specialization_stats.items(), key=lambda x: x[1])[0] if specialization_stats else 'none',
        'most_common_level': max(level_stats.items(), key=lambda x: x[1])[0] if level_stats else 'none'
    }


def create_sample_report() -> dict:
    """Создает тестовый отчет для демонстрации"""
    return {
        'report_date': datetime.now().isoformat(),
        'total_students': 42,
        'active_today': 15,
        'active_percentage': 35.7,
        'total_topics_studied': 127,
        'avg_topics_per_student': 3.02,
        'specialization_stats': {
            'data_science': 25,
            'web_dev': 12,
            'bioinformatics': 5
        },
        'level_stats': {
            'beginner': 20,
            'intermediate': 18,
            'advanced': 4
        },
        'most_popular_specialization': 'data_science',
        'most_common_level': 'beginner'
    }


def generate_markdown_report(data: dict, date: datetime, output_dir: Path):
    """Генерирует отчет в формате Markdown"""
    
    # Создаем график
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # График специализаций
    specs = list(data['specialization_stats'].keys())
    spec_counts = list(data['specialization_stats'].values())
    axes[0].bar(specs, spec_counts)
    axes[0].set_title('Распределение по специализациям')
    axes[0].set_xlabel('Специализация')
    axes[0].set_ylabel('Количество студентов')
    axes[0].tick_params(axis='x', rotation=45)
    
    # График уровней
    levels = list(data['level_stats'].keys())
    level_counts = list(data['level_stats'].values())
    axes[1].bar(levels, level_counts, color=['red', 'orange', 'green'])
    axes[1].set_title('Распределение по уровням знаний')
    axes[1].set_xlabel('Уровень')
    axes[1].set_ylabel('Количество студентов')
    
    plt.tight_layout()
    chart_path = output_dir / f'charts_{date.strftime("%Y-%m-%d")}.png'
    plt.savefig(chart_path, dpi=100, bbox_inches='tight')
    plt.close()
    
    # Создаем markdown файл
    md_content = f"""# 📊 Ежедневный отчет по системе обучения
**Дата:** {date.strftime('%Y-%m-%d')}

## 📈 Общая статистика

| Показатель | Значение |
|------------|----------|
| Всего студентов | {data['total_students']} |
| Активных сегодня | {data['active_today']} |
| Процент активности | {data['active_percentage']:.1f}% |
| Всего изучено тем | {data['total_topics_studied']} |
| Среднее тем на студента | {data['avg_topics_per_student']:.2f} |

## 🎯 Распределение по специализациям

| Специализация | Количество студентов |
|---------------|----------------------|
{"".join(f"| {spec} | {count} |\n" for spec, count in data['specialization_stats'].items())}

**Самая популярная:** {data['most_popular_specialization']}

## 📊 Уровни знаний

| Уровень | Количество студентов |
|---------|----------------------|
| Начинающий | {data['level_stats'].get('beginner', 0)} |
| Средний | {data['level_stats'].get('intermediate', 0)} |
| Продвинутый | {data['level_stats'].get('advanced', 0)} |

**Наиболее частый уровень:** {data['most_common_level']}

## 📊 Визуализация

![Статистика обучения]({chart_path.relative_to(output_dir.parent)})

## 🎯 Рекомендации

1. **Для начинающих студентов:** Увеличить количество практических заданий
2. **По специализации {data['most_popular_specialization']}:** Добавить дополнительные материалы
3. **Для повышения активности:** Рассмотреть систему мотивации (бейджи, достижения)

*Отчет сгенерирован автоматически системой адаптивного обучения*
"""
    
    report_path = output_dir / f'report_{date.strftime("%Y-%m-%d")}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


def generate_json_report(data: dict, date: datetime, output_dir: Path):
    """Генерирует отчет в формате JSON"""
    report_path = output_dir / f'report_{date.strftime("%Y-%m-%d")}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_html_report(data: dict, date: datetime, output_dir: Path):
    """Генерирует отчет в формате HTML"""
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Отчет по обучению {date.strftime('%Y-%m-%d')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .card {{ background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .stat-item {{ background: white; padding: 15px; border-radius: 5px; text-align: center; }}
        .highlight {{ color: #2ecc71; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>📊 Ежедневный отчет по системе обучения</h1>
    <p><strong>Дата:</strong> {date.strftime('%Y-%m-%d')}</p>
    
    <div class="card">
        <h2>📈 Общая статистика</h2>
        <div class="stats">
            <div class="stat-item">
                <h3>Всего студентов</h3>
                <p class="highlight">{data['total_students']}</p>
            </div>
            <div class="stat-item">
                <h3>Активных сегодня</h3>
                <p class="highlight">{data['active_today']}</p>
            </div>
            <div class="stat-item">
                <h3>Процент активности</h3>
                <p class="highlight">{data['active_percentage']:.1f}%</p>
            </div>
            <div class="stat-item">
                <h3>Изучено тем</h3>
                <p class="highlight">{data['total_topics_studied']}</p>
            </div>
        </div>
    </div>
    
    <div class="card">
        <h2>🎯 Рекомендации</h2>
        <ul>
            <li>Для начинающих студентов: увеличить количество практических заданий</li>
            <li>По специализации {data['most_popular_specialization']}: добавить дополнительные материалы</li>
            <li>Для повышения активности: рассмотреть систему мотивации</li>
        </ul>
    </div>
    
    <p><em>Отчет сгенерирован автоматически системой адаптивного обучения</em></p>
</body>
</html>"""
    
    report_path = output_dir / f'report_{date.strftime("%Y-%m-%d")}.html'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Генератор ежедневного отчета по обучению')
    parser.add_argument('--date', default='today', help='Дата отчета (YYYY-MM-DD)')
    parser.add_argument('--format', choices=['markdown', 'json', 'html'], 
                       default='markdown', help='Формат отчета')
    
    args = parser.parse_args()
    generate_report(args.date, args.format)
