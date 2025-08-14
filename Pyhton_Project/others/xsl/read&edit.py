import pandas as pd

df = pd.read_excel(input("Give full file location"))
print(df)

data = {}

for i in range(len(df)):
    x = df.loc[i].values
    if any(isinstance(cell, str) and "rutwik" in cell for cell in x) or any(isinstance(cell, str) and "balley" in cell for cell in x):

        data[i] = x

df1 = pd.DataFrame(list(data.values()), index=list(data.keys()), columns=df.columns)

df1.to_excel("text1.xlsx", index=False)








