import pandas as pd

df =pd.read_csv("crazy.csv")

unique_count = df['dealerName'].unique()
print(f"Number of unique values in the column: {unique_count}")