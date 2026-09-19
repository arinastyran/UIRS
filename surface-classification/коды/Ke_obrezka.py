import pandas as pd
import numpy as np
from pathlib import Path

# 1. Загружаем данные после первого окна 
INPUT_FILE = Path(r"C:\UIRS\surface-classification\filtered_4W_window10_step1.csv")
OUTPUT_FILE = Path(r"C:\UIRS\surface-classification\dct2_ready_data.csv")

print("Загрузка данных...")
df = pd.read_csv(INPUT_FILE)

N_nominal = 0.11  # Номинальная нагрузка (Н·м)
R = 0.031        # Радиус колеса (м)
L = 0.159        # Ширина колесной базы (м)

print("Расчет Ke и угловой скорости робота (omega)...")

# Расчет Ke (формула 4)
numerator = (
    df['wheel_load.1'] * df['wheel_angular_velocity.1'] +
    df['wheel_load.2'] * df['wheel_angular_velocity.2'] +
    df['wheel_load.3'] * df['wheel_angular_velocity.3'] +
    df['wheel_load.4'] * df['wheel_angular_velocity.4']
)
denominator = N_nominal * (
    df['wheel_angular_velocity.1'].abs() +
    df['wheel_angular_velocity.2'].abs() +
    df['wheel_angular_velocity.3'].abs() +
    df['wheel_angular_velocity.4'].abs()
)
denominator = denominator.replace(0, np.nan)
df['Ke'] = (numerator / denominator).replace([np.inf, -np.inf], np.nan).fillna(0)

# Расчет омега (формула 2)
v_left = R * (df['wheel_angular_velocity.1'] + df['wheel_angular_velocity.4']) / 2
v_right = R * (df['wheel_angular_velocity.2'] + df['wheel_angular_velocity.3']) / 2
df['omega_robot'] = (v_left - v_right) / L

print("Поиск общего диапазона omega...")
omega_stats = df.groupby(['surface', 'number_exper'])['omega_robot'].agg(['min', 'max'])
omega_min = omega_stats['min'].max()
omega_max = omega_stats['max'].min()
print(f"Общий диапазон: [{omega_min:.4f}, {omega_max:.4f}] рад/с")

print("Обрезка данных и группировка по 100 интервалам...")
# Обрезаем до общего диапазона
df = df[(df['omega_robot'] >= omega_min) & (df['omega_robot'] <= omega_max)].copy()

# Создаем 100 интервалов
n_bins = 100
bin_edges = np.linspace(omega_min, omega_max, n_bins + 1)
df['omega_bin'] = pd.cut(df['omega_robot'], bins=bin_edges, labels=False, include_lowest=True)

# Считаем медиану и стандартное отклонение Ke для каждой поверхности в каждом бине
print("Вычисление медиан и стандартных отклонений...")
final_data = df.groupby(['surface', 'omega_bin']).agg(
    median_Ke=('Ke', 'median'),
    std_Ke=('Ke', 'std')
).reset_index()

# Добавляем центр бина (значение omega) для удобного построения графиков
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
final_data['omega_center'] = final_data['omega_bin'].map(lambda x: bin_centers[int(x)])

# Сортируем
final_data = final_data.sort_values(['surface', 'omega_bin'])

final_data.to_csv(OUTPUT_FILE, index=False)

print(f"\nГОТОВО! Сохранен один чистый файл: {OUTPUT_FILE}")
print(f"Размер итогового файла: {len(final_data)} строк (10 поверхностей × 100 интервалов)")