import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загружаем подготовленные данные
INPUT_FILE = r"C:\UIRS\surface-classification\dct2_ready_data.csv"
df = pd.read_csv(INPUT_FILE)

print("Загрузка данных завершена.")

plt.figure(figsize=(12, 8))

surfaces = df['surface'].unique()
colors = plt.cm.tab10(np.linspace(0, 1, len(surfaces)))

for i, surface in enumerate(surfaces):
    surf_data = df[df['surface'] == surface].sort_values('omega_bin')
    
    plt.plot(surf_data['omega_center'], surf_data['median_Ke'], 
             linewidth=2, label=surface.replace('_', ' '), color=colors[i])

# Оформление графика
plt.title('Медианы Ke для всех поверхностей', fontsize=14, fontweight='bold', pad=15)
plt.xlabel(r'Угловая скорость робота, рад/с ($\omega$)', fontsize=12)
plt.ylabel('Медианный коэффициент Ke', fontsize=12)

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Тип поверхности', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)

plt.tight_layout()

plt.savefig(r"C:\UIRS\surface-classification\figure_8_medians.png", dpi=300, bbox_inches='tight')
print("График сохранен: figure_8_medians.png")

plt.show()