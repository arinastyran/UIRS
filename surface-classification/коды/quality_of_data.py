import pandas as pd

# Загружаем ваши отфильтрованные данные
df = pd.read_csv(r"C:\UIRS\surface-classification\filtered_4W_window_step.csv")

print("СТАТИСТИКА ПО ПОВЕРХНОСТЯМ")

# 1. Сколько всего строк у каждой поверхности
print("\n1. ОБЩЕЕ КОЛИЧЕСТВО СТРОК по поверхностям:")
surface_counts = df.groupby('surface').size()
for surface, count in surface_counts.items():
    print(f"   {surface:25s}: {count:,} строк")

print(f"\n   Минимум: {surface_counts.min():,} строк")
print(f"   Максимум: {surface_counts.max():,} строк")

# 2. Сколько экспериментов у каждой поверхности
print("\n2. КОЛИЧЕСТВО ЭКСПЕРИМЕНТОВ по поверхностям:")
exp_counts = df.groupby(['surface', 'number_exper']).size().groupby('surface').count()
for surface, count in exp_counts.items():
    print(f"   {surface:25s}: {count} экспериментов")

print(f"\n   Минимум: {exp_counts.min()} экспериментов")
print(f"   Максимум: {exp_counts.max()} экспериментов")
