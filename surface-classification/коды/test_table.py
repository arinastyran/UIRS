import pandas as pd
df = pd.read_csv(r"C:\UIRS\surface-classification\combined_processed_4W.csv")
print(f"Всего строк: {len(df)}")
print(f"Колонки: {list(df.columns)}")
print("\nПервые 5 строк:")
print(df.head())
print("\nТип данных:")
print(df.dtypes)