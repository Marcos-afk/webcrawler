from func import *

url = "https://www.youtube.com/"
suffix_title = url.split(".")[1]

internos, externos = get_links(url)

with open(f"{suffix_title}.links_internos.txt", "w", encoding='utf-8') as k:
    for link in internos:
        k.write(link)
        k.write('\n')

with open(f"{suffix_title}.links_externos.txt", "w", encoding='utf-8') as l:
    for link in externos:
        l.write(link)
        l.write('\n')

termos = get_terms(url)

with open(f"{suffix_title}.terms.txt", "w", encoding='utf8') as f:
    for termo in termos:
        f.write(termo)
        f.write('\n')
