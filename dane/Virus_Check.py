import pandas as pd

l = "https://docs.google.com/spreadsheets/d/1QiX8JfHH2tnyyzSOMuV8Yh5EIY9YH8TLr5td9ZWWnCM/edit#gid=0" #Link do arkuszy google

def clean_gs(link:str): #Przyjmuje link jako wartość
    df = pd.read_csv(link.replace("/edit#gid=", "/export?format=csv&gid=")) #Oczyszcza link
    last = df.loc[0,"_t"]   #Odczytuje zawartość kolumny "_t"
    df = df.iloc[0:,0].dropna() #Oczyszcza z wartości pustych lub błędów
    return [df.values.tolist(), last] #Zwraca listę oczyszczonych plików oraz datę ostatniego wpisu


lista = clean_gs(l)[0] #Lista linków
aktualizacja = clean_gs(l)[1]   #Data ostatniego wpisu
lista = [i for i in lista if "/" in i]  #Oczyszczanie z wpisów nie będących linkami

print("Data ostatniego wpisu w arkuszu Google to {}".format(aktualizacja))  #Wyprintowanie ostatniego wpisu

"""

To do

*Pomyśleć nad jakimś antywirusem skanującym te linki (będę szukać)
"""
