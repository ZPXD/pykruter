from flask import Flask, render_template
import random
import pandas as pd

app=Flask(__name__)


@app.route('/')
def index():

    # Dane
    df = pd.read_csv('data/sample.csv')
    
    # Losowanie pytania
    i = random.choice(range(len(df)))
    this_question = df.loc[i, :]
    question = this_question['question']
    answer = this_question['answer']

    return render_template("index.html", question=question, answer=answer)

if __name__=="__main__":
    app.run()
