import matplotlib.pyplot as plt
import numpy as np
import tempfile
from matplotlib.patches import FancyBboxPatch


def time_to_float(time_obj):
    return time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600


async def create_activity_graph(periods_by_day, username, selected_date):
    # Создаем более широкий график для лучшей наглядности
    fig, ax = plt.subplots(figsize=(16, 4))  # Размер графика сделан шире и немного выше

    # Общий интервал времени (от 0 до 24 часов)
    start_time = 0
    end_time = 24

    # Настройка основного фона и поля вокруг
    fig.patch.set_facecolor('#f0f0f0')  # Светло-серый фон для всего графика
    ax.set_facecolor('#ffffff')          # Белый фон для основной области графика

    # Красный полупрозрачный фон для состояния "Не в сети"
    ax.add_patch(FancyBboxPatch((start_time, 0.3), end_time - start_time, 0.3,
                                boxstyle="round,pad=0.03", edgecolor='none',
                                facecolor='#ff4c4c', alpha=0.7, zorder=1))  # Полупрозрачная красная полоса

    # Подсчёт общего времени в сети
    total_online_hours = 0
    for day, periods in periods_by_day.items():
        for start, end in periods:
            start_float = time_to_float(start)
            end_float = time_to_float(end)
            total_online_hours += (end_float - start_float)
            # Добавляем зелёные зоны активности (в сети)
            ax.add_patch(FancyBboxPatch((start_float, 0.3),
                                        end_float - start_float, 0.3,
                                        boxstyle="round,pad=0.03", edgecolor='none',
                                        facecolor='#77DD77', alpha=0.9, zorder=2))  # Менее прозрачная зеленая полоса

    # Настройки графика
    ax.set_xlim(start_time, end_time)  # Устанавливаем пределы по X от 0 до 24 часов
    ax.set_ylim(0, 1)  # Ограничиваем по оси Y

    # Скрываем ось Y
    ax.yaxis.set_visible(False)

    # Оформление временной шкалы
    ax.set_xticks(np.arange(0, 25, 1))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: f'{int(val):02d}'))
    ax.set_xlabel("Время суток", color='#333333', fontsize=12, fontweight='bold')
    ax.tick_params(axis='x', colors='#333333', length=6)

    # Плавные разделительные линии
    ax.grid(False)
    for i in range(25):
        ax.axvline(x=i, color='#cccccc', linestyle='-', zorder=0, linewidth=0.7)  # Разделительные линии

    # Убираем рамки графика
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#666666')  # Более контрастная линия снизу

    # Поднимаем юзернейм (Fe4ester)
    plt.text(-2, 1.2, username, color='#333333', fontsize=16, ha='left', va='center', fontweight='bold')

    # Добавляем надпись об общем времени ровно между юзернеймом и надписью "Не в сети"
    total_hours_formatted = f"{int(total_online_hours)} ч {int((total_online_hours % 1) * 60)} мин"
    plt.text(12, 1.2, f"Общее время в сети: {total_hours_formatted}", color='#333333', fontsize=12,
             ha='center', va='center', fontweight='bold', bbox=dict(facecolor='#eeeeee', edgecolor='none', boxstyle='round,pad=0.5'))

    # Поднимаем водяной знак "SeeOnlineBot" на уровень юзернейма
    plt.text(25.5, 1.2, 'SeeOnlineBot', color='#999999', fontsize=14, ha='right', va='center', alpha=0.6)

    # Добавляем дату выбранного периода рядом с шкалой времени
    formatted_date = selected_date.strftime("%d %b")
    plt.text(-2, -0.05, formatted_date, color='#555555', fontsize=10, ha='left', va='center')

    # Добавляем легенду в верхней части графика с новым стилем
    ax.legend(['Не в сети', 'В сети'], loc='upper center', bbox_to_anchor=(0.5, 1.2),
              ncol=2, fontsize=12, frameon=False, markerscale=1.2, labelspacing=1.5)

    # Создаем временный файл для сохранения графика
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, format='png', facecolor=fig.get_facecolor(), bbox_inches='tight')
        temp_file_path = tmpfile.name

    # Закрываем фигуру для освобождения памяти
    plt.close(fig)

    return temp_file_path
