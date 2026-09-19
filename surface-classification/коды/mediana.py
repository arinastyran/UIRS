import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm

# Настройки
INPUT_FILE = Path(r"C:\UIRS\surface-classification\combined_processed_4W.csv")
OUTPUT_FILE = Path(r"C:\UIRS\surface-classification\filtered_4W_MEDIAN_window10_step5.csv") 
WINDOW_SIZE = 10   
STEP_SIZE = 5      

def apply_moving_window_median(df, window_size, step_size):
    
    exclude_cols = {'Unnamed: 0', 'Time', 'surface', 'wheels', 'number_exper'}
    numeric_cols = [col for col in df.select_dtypes(include=[np.number]).columns 
                    if col not in exclude_cols]
    
    print(f"Параметры: окно={window_size}, шаг={step_size}, метод=МЕДИАНА")
    
    all_windows = []
    groups = df.groupby(['surface', 'number_exper'], sort=False)
    
    print(f"\nОбрабатываю {len(groups)} групп...")
    
    for (surface, exp_num), group in tqdm(groups, desc="Медианная фильтрация", unit="группа"):
        group = group.sort_values('Time').reset_index(drop=True)
        
        if len(group) < window_size:
            continue
        
        for start_idx in range(0, len(group) - window_size + 1, step_size):
            end_idx = start_idx + window_size
            window = group.iloc[start_idx:end_idx]
            
            row = {
                'surface': surface,
                'number_exper': exp_num,
                'wheels': window['wheels'].iloc[0],
                'Time': window['Time'].mean(),  # Для времени оставляем среднее
                'window_start_idx': start_idx,
                'window_size': window_size,
            }
            
            for col in numeric_cols:
                row[col] = window[col].median()  # Было .mean(), стало .median()
            
            all_windows.append(row)
    
    result_df = pd.DataFrame(all_windows)
    
    first_cols = ['surface', 'number_exper', 'wheels', 'Time', 'window_start_idx', 'window_size']
    other_cols = [col for col in result_df.columns if col not in first_cols]
    result_df = result_df[first_cols + other_cols]
    
    return result_df


def main():
    print("МЕДИАННАЯ ФИЛЬТРАЦИЯ СКОЛЬЗЯЩИМ ОКНОМ")
    
    print(f"\n1. Чтение файла: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    print(f"   Загружено: {len(df):,} строк")
    
    print(f"\n2. Применение медианного окна...")
    filtered_df = apply_moving_window_median(df, WINDOW_SIZE, STEP_SIZE)
    
    print(f"\n3. Результаты:")
    print(f"   Строк после фильтрации: {len(filtered_df):,}")
    
    print(f"\n4. Сохранение в: {OUTPUT_FILE}")
    filtered_df.to_csv(OUTPUT_FILE, index=False)
    
    print("\nГОТОВО!")


if __name__ == "__main__":
    main()