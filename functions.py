from bs4 import BeautifulSoup
import requests
import os
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse, urljoin
import pprint
from pymongo import MongoClient

nltk.download('punkt)
nltk.download('stopwords')

# Conecta ao banco de dados
def connect():
    url = "mongodb+srv://admin:admin@webcrawler.crbgm9t.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(url)
    return client

# Insere matriz no banco de dados
def insert_matrix(database, collection, matrix):
    client = connect()
    db = client[database]
    col = db[collection]

    document = {"Array": matrix}
    result = col.insert_one(document)

    return result.inserted_id

# Insere os dados no banco de dados MongoDB
def insert_data(database, collection, documents):
    client = connect()
    db = client[database]
    col = db[collection]
    ids = ""
    
    if type(documents) == list:
        docs = [{f"{i}": documents[i]} for i in range(len(documents))]
        result = col.insert_many(docs)
        ids = result.inserted_ids
    elif type(documents) == str:
        doc = {"string": documents}
        result = col.insert_one(doc)
        ids = result.inserted_id
    client.close()

    return ids

# Pega o código HTML do website
def get_html(response):
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")
    return soup

# Pega a tag head do website
def get_head(url):
    soup = get_html(url)
    head = soup.find('head')
    return head.prettify()

# Pega a tag body do website
def get_body(url):
    soup = get_html(url)
    body = soup.find('body')
    return body.prettify()

# Pega todas as meta tags do website
def get_meta(url):
    tags = []

    soup = get_html(url)
    meta = soup.find_all('meta')
    meta = list(meta)

    for m in meta:
        tags.append(str(m))

    return tags

# Pega todos os links internos e externos do website
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
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
                links_externos.add(href)
            else:
                links_internos.add(href)

    return links_externos, links_internos

# Pega todos os termos do website (excluindo tags)
def get_terms(url):
    soup = get_html(url)

    # Remove todas as tags, descapitaliza o texto, remove pontuação
    clean_text = soup.get_text(separator=' ') # 
    clean_text = re.sub(r'\s+', ' ', clean_text).strip() # Remove 2 ou mais espaços em branco seguidos
    clean_text = re.sub(r'\d', '', clean_text) # Remove todos os números
    clean_text = re.sub(r'\W+', ' ', clean_text).strip()  # Remove todos os caracteres que não são letras
    # clean_text = clean_text.translate(str.maketrans('', '', string.punctuation))

    # Transforma o texto em tokens (termos únicos), remove conectores
    termos = word_tokenize(clean_text)
    connectors = set(stopwords.words('portuguese') + stopwords.words('english'))
    termos_filtrados = [termo for termo in termos if termo not in connectors]

    return termos_filtrados


def vocabulary(termos):
    lower_vocab = []

    # for i in range(len(termos)):
    #     termo = termos[i].lower()
    #     if termo not in vocab:
    #         vocab.append(termo)
    vocab = sorted(list(set(termos)))

    for wrd in vocab:
        lower_vocab.append(wrd.lower())

    return lower_vocab

# Cria matriz booleana
def matrix(termos, documentos):
    matriz = []

    for termo in termos:
        linha = []
        for documento in documentos:
            presente = termo in documento
            linha.append(presente)
        matriz.append(linha)

    return matriz

# Consultar termos
def search(consulta, documentos):
    termosConsulta = consulta.split(' ')
    resultados = []

    for documento in documentos:
        presente = any(termo in termosConsulta for termo in documento)
        resultados.append(presente)
    return resultados
              
