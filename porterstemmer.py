from porter2stemmer import Porter2Stemmer

Stemmer=Porter2Stemmer()
l=['caresses', 'plastered', 'hopping', 'filing', 'happy','condition', 'conditionality', 'rational', 'rationality', 'decisiveness', 'electrical', 'electrocution', 'adjustment', 'adjustable','probate', 'probationary',  'controlling']
for i in l:
    print(i,Stemmer.stem(i))