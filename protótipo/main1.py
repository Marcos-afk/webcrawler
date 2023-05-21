from bs4 import BeautifulSoup
import requests
import re
import string
import wordninja
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

websites = [
  "https://www.google.com",
  "https://www.amazon.com",
  "https://www.facebook.com",
  "https://www.twitter.com",
  "https://www.instagram.com",
  "https://www.linkedin.com",
  "https://www.youtube.com",
  "https://www.reddit.com",
  "https://www.wikipedia.org",
  "https://www.yahoo.com",
]

def split_words(words):
    split_words = []
    for word in words:
        split = wordninja.split(word)
        split_words.extend(split)
    return split_words

def parseandclean():
    listas = []
    for website in websites:
        response = requests.get(website)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        clean_text = soup.get_text()
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        clean_text = re.sub(r'\d', '', clean_text)
        clean_text = re.sub(r'\W+', ' ', clean_text).strip()
        clean_text = clean_text.lower()
        clean_text = clean_text.translate(str.maketrans('', '', string.punctuation))

        tokens = word_tokenize(clean_text)
        stop_words = set(stopwords.words('portuguese'))
        filtered_tokens = [token for token in tokens if token not in stop_words]

        split_words(filtered_tokens)
        listas.append(filtered_tokens)

    return listas

listastermos = parseandclean()

for i, lista in enumerate(listastermos):
    filename = f'termos_site_{i}.txt'
    with open("lista_arquivos.txt", "a") as f:
        f.write(filename)
        f.write('\n')

    with open(filename, 'w', encoding='utf-8') as f2:
        for word in lista:
            try:
                f2.write(word)
                f2.write('\n')
            except UnicodeEncodeError:
                continue
