from flask import Flask, render_template
import random
import pandas as pd

def random_question_from_csv(): 

  # Dane
  df = pd.read_csv('data/sample.csv')
    
  # Losowanie pytania
  i = random.choice(range(len(df)))
  this_question = df.loc[i, :]
  question = this_question['question']
  answer = this_question['answer']
  tmp_answer_list = answer.split(' ')
  new_answer_list = []
  new_answer_str = ''
  for word in tmp_answer_list:
    if word.endswith('-'):
      new_answer_str+= ' '+word.replace('-','')
      new_answer_list.append(new_answer_str)
      new_answer_str = ''
    elif word.endswith('–'):
      new_answer_list.append(new_answer_str)
      new_answer_str = ''
      new_answer_str+= ' '+word.replace('–','')
    elif "\n" in word:
      tmp_word_list = word.split('\n')
      new_answer_str+= tmp_word_list[0]
      new_answer_list.append(new_answer_str)
      new_answer_str = tmp_word_list[1]
    else:
      new_answer_str+= ' '+word
  
  new_answer_list.append(new_answer_str)
  #new_answer_str = new_answer_str.replace('\n','<br />')
  
  return [question, new_answer_list]

app=Flask(__name__)

@app.route('/')
def pykruter():
	
	question_answer_list = random_question_from_csv()
	question = question_answer_list[0]
	answer_list = question_answer_list[1]
 
	return render_template("index.html", question=str(question), answer_list=answer_list)

if __name__=="__main__":
    app.run()
