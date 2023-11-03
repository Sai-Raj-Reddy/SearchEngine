import spacy
from nltk.stem import SnowballStemmer
nlp=spacy.load("en_core_web_sm")
text = "Apple company makes great products"
text="El río fluye suavemente entre las colinas verdes."
# Tokenize the text using spaCy
doc = nlp(text)
print(ord('í'))
print(ord('i'))
# Initialize a list to store token metadata
token_metadata = []

# Map token metadata to your search engine format
for token in doc:
    token_info = {
        "text": token.text,
        "pos": token.pos_,
        "lemma": token.lemma_,
    }
    token_metadata.append(token_info)
snowstemmer=SnowballStemmer("spanish")
# Utilize token metadata as needed
for token_info in token_metadata:
    print(snowstemmer.stem(token_info['text']))
    # print(token_info)