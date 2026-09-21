import matplotlib.pyplot as plt
import pandas as pd

original = pd.read_csv(r"C:\UIRS\surface-classification\combined_processed_4W.csv")
filtered = pd.read_csv(r"C:\UIRS\surface-classification\filtered_4W_window10_step1.csv")

# Берем один эксперимент
exp = original[(original['surface'] == 'artificial_grass') & 
               (original['number_exper'] == 1)]

exp_filt = filtered[(filtered['surface'] == 'artificial_grass') & 
                    (filtered['number_exper'] == 1)]

# Ограничиваем одинаковым временным диапазоном
time_limit = 5.0 
exp = exp[exp['Time'] <= time_limit]
exp_filt = exp_filt[exp_filt['Time'] <= time_limit]

# Список колонок для проверки
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

fig, axes = plt.subplots(4, 2, figsize=(16, 14))
axes = axes.flatten()

for idx, col in enumerate(columns_to_check):
    if idx >= len(axes):
        break
    
    ax = axes[idx]
    
    # Рисуем исходный сигнал
    ax.plot(exp['Time'], exp[col], 
            label='Исходный (100 Гц)', linewidth=1, alpha=0.3, color='blue', zorder=1)
    
    # Рисуем отфильтрованный сигнал
    ax.plot(exp_filt['Time'], exp_filt[col], 
            label='Фильтр (окно=10, шаг=1)', linewidth=2, color='orange', zorder=2)
    
    ax.set_title(col, fontsize=11, fontweight='bold')
    ax.set_ylabel('Значение от времени')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle(f'Сравнение сигналов: исходный vs фильтрованный (первые {time_limit} сек)', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()