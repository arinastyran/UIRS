import pandas as pd
import matplotlib.pyplot as plt

# 1. Загрузка файлов
original = pd.read_csv(r"C:\UIRS\surface-classification\combined_processed_4W.csv")
mean_filt = pd.read_csv(r"C:\UIRS\surface-classification\filtered_4W_window10_step5.csv")
median_filt = pd.read_csv(r"C:\UIRS\surface-classification\filtered_4W_MEDIAN_window10_step5.csv")

# 2. Фильтрация по одному эксперименту
surface_name = 'artificial_grass'
exp_num = 1

exp_orig = original[(original['surface'] == surface_name) & (original['number_exper'] == exp_num)]
exp_mean = mean_filt[(mean_filt['surface'] == surface_name) & (mean_filt['number_exper'] == exp_num)]
exp_med = median_filt[(median_filt['surface'] == surface_name) & (median_filt['number_exper'] == exp_num)]

# Ограничиваем по времени 
time_limit = 5.0
exp_orig = exp_orig[exp_orig['Time'] <= time_limit]
exp_mean = exp_mean[exp_mean['Time'] <= time_limit]
exp_med = exp_med[exp_med['Time'] <= time_limit]

# 3. Список из 8 параметров (используем как есть)
columns_to_check = [
    'linear_acceleration.x',
    'linear_acceleration.y',
    'linear_acceleration.z',
    'angular_velocity.x',
    'angular_velocity.y',
    'angular_velocity.z',
    'wheel_load.1',
    'estimated_power.1'
]

# 4. Создаем сетку графиков 4x2
fig, axes = plt.subplots(4, 2, figsize=(18, 16))
axes = axes.flatten() 

for idx, col in enumerate(columns_to_check):
    ax = axes[idx]
    
    # Исходный сигнал
    ax.plot(exp_orig['Time'], exp_orig[col], 
            label='Исходный', linewidth=1, alpha=0.3, color='blue')
    
    # Среднее значение
    ax.plot(exp_mean['Time'], exp_mean[col], 
            label='Среднее', linewidth=2, color='orange')
    
    # Медиана
    ax.plot(exp_med['Time'], exp_med[col], 
            label='Медиана', linewidth=2, color='green', linestyle='--')
    
    ax.set_title(col, fontsize=12, fontweight='bold', pad=8)
    ax.set_xlabel('Время (с)', fontsize=9)
    ax.set_ylabel('Значение', fontsize=9)
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, alpha=0.3)

plt.suptitle(f'Сравнение фильтров: Исходный vs Среднее vs Медиана\n', 
             fontsize=16, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()