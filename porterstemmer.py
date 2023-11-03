from porter2stemmer import Porter2Stemmer
from nltk.stem import SnowballStemmer
import spacy
nlp = spacy.load("es_core_news_sm")

text="Hoy hace mucho frío. Es invierno y todas las calles están cubiertas de nieve. Dentro de poco vendrá la primavera y con ella el sol y el tiempo cálido. La semana pasada estuvo de lluvia y tormenta. Incluso un rayo cayó encima de la campana de la catedral, pero no ocurrió nada. Los truenos siempre me han dado miedo y mucho respeto. Pero tenemos suerte... pues la previsión del tiempo para mañana es muy buena. Dicen que hoy habrá heladas y por la tarde granizo, pero mañana el día será soleado. A ver si tengo suerte y veo algún arcoíris."
# nlp = spacy.load("es_core_news_sm")
from langdetect import detect
print(detect(text))
text2="española"
print(detect(text2))
doc=nlp(text)
for token in doc:
    print(token.text)



Stemmer=Porter2Stemmer()
spanish_stemmer=SnowballStemmer("spanish")
l=['española']
for s in l:
    print(s,Stemmer.stem(s))
    print(s,spanish_stemmer.stem(s))
    if s!='':
        i=0
        j=len(s)-1
        while(i<j):
            ascii_val=ord(s[i])
            if s[i].isalnum():
                break
            else:
                i+=1
        while(j>=0):
            ascii_val=ord(s[j])
            if s[j].isalnum():
                break
            else:
                j-=1
        st=''
        for k in range(i,j+1):
            if s[k]=='\'' or s[k]=='"':
                continue
            else:
                st+=s[k]
        print(st)

