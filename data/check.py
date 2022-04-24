import pandas as pd

df = pd.read_csv('sample.csv')
df = df.loc[:,['source', 'question', 'answer']]

for i, row in df.iterrows():
    print(i, row.question)

print(df.columns)

for i in range(len(df)):
    question = df.loc[i,'question']
    print(question)
