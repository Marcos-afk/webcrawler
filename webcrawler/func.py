from bs4 import BeautifulSoup
import requests
import re
import string
# import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse, urljoin

# nltk.download('punkt)
# nltk.download('stopwords')

# Pega o código HTML do website
def get_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")
    html_code = soup.prettify()
    return html_code

# Pega todos os links internos e externos do website
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 
    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc

    # Cria sets para links internos/externos
    links_internos = set()
    links_externos = set()

    # Para cada tag 'a' do código HTML do website
    for anchor in soup.find_all('a'):
        # Armazena o link na variável href
        href = anchor.get('href')
        if href: # Se href não está vazia
            href = urljoin(base_url, href)
            if urlparse(href).netloc == urlparse(url).netloc:
                links_internos.add(href)
            else:
                links_externos.add(href)

    return links_externos, links_internos

# Pega todos os termos do website (excluindo tags)
def get_terms(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")

    # Remove todas as tags, descapitaliza o texto, remove pontuação
    clean_text = soup.get_text()
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    clean_text = re.sub(r'\d', '', clean_text)
    clean_text = re.sub(r'\W+', ' ', clean_text).strip()
    clean_text = clean_text.lower()
    clean_text = clean_text.translate(str.maketrans('', '', string.punctuation))

    # Transforma o texto em tokens (termos únicos), remove conectores
    termos = word_tokenize(clean_text)
    connectors = set(stopwords.words('english'))
    termos_filtrados = [termo for termo in termos if termo not in connectors]

    return termos_filtrados