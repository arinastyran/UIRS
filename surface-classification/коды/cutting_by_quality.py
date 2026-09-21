import pandas as pd
import numpy as np
from pathlib import Path

# Загружаем данные
INPUT_FILE = Path(r"C:\UIRS\surface-classification\filtered_4W_window10_step1.csv")
OUTPUT_FILE = Path(r"C:\UIRS\surface-classification\balanced_4W.csv")

df = pd.read_csv(INPUT_FILE)


# 1. Считаем минимальное количество экспериментов
exp_counts = df.groupby('surface')['number_exper'].nunique()
min_experiments = exp_counts.min()

# 2. Считаем минимальную длину эксперимента
exp_lengths = df.groupby(['surface', 'number_exper']).size()
min_length = exp_lengths.min()

print(f"\nМинимальное количество экспериментов: {min_experiments}")
print(f"Минимальная длина эксперимента: {min_length} строк")

# 3. Выравниваем данные
balanced_parts = []

for surface in df['surface'].unique():
    surface_data = df[df['surface'] == surface]
    
    # Берём первые min_experiments экспериментов
    experiments = sorted(surface_data['number_exper'].unique())[:min_experiments]
    
    for exp_num in experiments:
        exp_data = surface_data[surface_data['number_exper'] == exp_num]
        
        # Сортируем по времени и обрезаем до min_length строк
        exp_data = exp_data.sort_values('Time').head(min_length)
        
        balanced_parts.append(exp_data)

# 4. Собираем итоговый датасет
balanced_df = pd.concat(balanced_parts, ignore_index=True)

# 5. Сохраняем
balanced_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nРезультат:")
print(f"  Всего строк: {len(balanced_df):,}")
print(f"  Поверхностей: {balanced_df['surface'].nunique()}")
print(f"  Экспериментов на поверхность: {min_experiments}")
print(f"  Строк на эксперимент: {min_length}")
print(f"  Итого экспериментов: {len(balanced_df) // min_length}")
print(f"\nСохранено в: {OUTPUT_FILE}")

# Проверка
print("\nПроверка баланса:")
for surface in sorted(balanced_df['surface'].unique()):
    count = len(balanced_df[balanced_df['surface'] == surface])
    exps = balanced_df[balanced_df['surface'] == surface]['number_exper'].nunique()
    print(f"  {surface:25s}: {count:,} строк ({exps} экспериментов)")