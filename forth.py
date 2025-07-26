import pandas as pd

df1 = pd.read_csv("final.csv")
df2 = pd.read_csv("add_data_fixed.csv")

final_df = pd.concat([df1, df2], ignore_index=True)
