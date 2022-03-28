from flask import Flask, render_template
import random

app=Flask(__name__)

@app.route('/')
def index():
    text = open('dane/sample.txt').readlines()
    text = random.choice(text)
    return render_template("index.html", text=text)

if __name__=="__main__":
    app.run()
