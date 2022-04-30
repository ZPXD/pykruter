import pandas as pd
import os
import sys

file_name = "sample.csv"

'''
Modify to check datafile contents.
'''

def check_datafile(file_name):
    data_file = os.path.join(os.getcwd(), 'data', file_name)
    df = pd.read_csv(data_file)
    df = df.loc[:,['source', 'question', 'answer']]

    for i, row in df.iterrows():
        print(i, row.question)

    print(df.columns)

    for i in range(len(df)):
        question = df.loc[i,'question']
        print(question)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = file_name
    check_datafile(file)



