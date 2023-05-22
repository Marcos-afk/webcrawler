from func import *

url = "https://www.youtube.com"

html = get_html(url)
head_tag = get_head(url)
body_tag = get_body(url)
meta_tags = get_meta(url)
internos, externos = get_links(url)
termos = get_terms(url)
