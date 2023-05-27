# --------------------------------- #
# Desenvolvido por: --------------- #
# Kaleb Carvalho Santos ----------- #
# Jônatas Mota da Silva Júnior ---- #
# Marcos André Lima de Melo ------- #
# ----------------------------------#

from functions import *

urls = []  # Lista de links
documentos = []  # Lista de listas dos termos de cada site
all_termos = []  # Todos os vocabulários em uma única lista

# Cria lista baseada no arquivo de links
with open("websites.txt", "r") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        urls.append(lines[i].strip())

# Loop da lista de links
for url in urls:
    try:
        response = requests.get(url)
        # Se o site aceitar o pedido:
        if response.status_code == 200:
            # Cria o nome do banco de dados a partir da URL atual
            name = urlparse(url).netloc
            new_name = name.replace('.', '-')

            # Adquire todos os dados
            html = get_html(response)
            head_tag = get_head(response)
            body_tag = get_body(response)
            meta_tags = get_meta(response)
            internos, externos = get_links(url)
            termos = get_terms(response)
            vocabulario = vocabulary(termos)

            # Cria dados para matriz
            for termo in vocabulario:
                all_termos.append(termo)
            documentos.append(vocabulario)

            # Insere todos os dados no banco
            insert_data(new_name, "Código HTML", str(html))
            insert_data(new_name, "Head tag", head_tag)
            insert_data(new_name, "Body tag", body_tag)
            insert_data(new_name, "Meta tag", meta_tags)
            if len(internos) > 0:
                insert_data(new_name, "Links internos", list(internos))
            if len(externos) > 0:
                insert_data(new_name, "Links externos", list(externos))
            insert_data(new_name, "Termos", termos)
            insert_data(new_name, "Vocabulário", vocabulario)

            print(new_name + " done!!")

    # Se não houver resposta, continua com o próximo link na lista
    except requests.exceptions.RequestException:
        continue

# Cria a matriz e insere no banco
matriz = matrix(all_termos, documentos)
insert_matrix("Matriz", "Booleana", matriz)

# Termos de consulta
consulta = "carro bebida morte"
resultado = search(consulta, documentos)

# Imprime resultados da consulta
print("Resultados da consulta: ")
print(resultado)
