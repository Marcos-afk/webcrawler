conectores = ['de', 'para', 'com', 'que', 'qual', 'o', 'a', 'um', 'uns',
              'uma', 'umas', 'as', 'os', 'e', 'da', 'do', 'das', 'dos']

# documentos = [
#     'O carro está na garagem',
#     'A bebida está gelada',
#     'A morte é inevitável'
# ]

# Lista de listas de termos sem conectores
docsSemConectores = []
# Lista de listas de termos
listas = []
# Lista de nomes dos arquivos de termos
arquivos = []

# Cria lista com nome dos arquivos
with open("lista_arquivos.txt", "r") as f:
    for linha in f:
        arquivos.append(linha.strip())

# Armazena conteudo dos arquivos em lista "listas"
for arquivo in arquivos:
    lista = []
    with open(arquivo, "r", encoding='utf-8') as f:
        for linha in f:
            lista.append(linha.strip())
    listas.append(lista)

for documento in listas:
    docsSemConectores.append(documento)

# Remove conectores from lista de termos
for doc in docsSemConectores:
    for word in doc:
        for conector in conectores:
            if word.lower() == conector:
                doc.remove(word)

# Cria vocabulário de termos
def criarVocabulario(documentos):
    vocab = []
    for documento in documentos:
        for i in range(len(documento)):
            wrd = documento[i].lower()
            if wrd not in vocab:
                vocab.append(wrd)
    return vocab

# Cria matriz booleana de termos
def criarMatriz(termos, documentos):
    matriz = []

    for termo in termos:
        linha = []
        for documento in documentos:
            termo_presente = termo in documento
            linha.append(termo_presente)
        matriz.append(linha)

    return matriz

# Cria consulta de termos
def consultaTermos(consulta, documentos):
    termosConsulta = consulta.split(' ')
    resultados = []

    for documento in documentos:
        presente = any(termo in termosConsulta for termo in documento)
        resultados.append(presente)
    return resultados


termos = criarVocabulario(docsSemConectores)
matriz_bool = criarMatriz(termos, docsSemConectores)

# Exibe dados
print("Matriz booleana:")
print(matriz_bool)

print("\nVocabulário:")
print(termos)

consulta = "Carro bebida morte"
resultadosConsulta = consultaTermos(consulta, docsSemConectores)

print("\nResultados da consulta: ")
print(resultadosConsulta)
