import pandas as pd

import requests
from bs4 import BeautifulSoup
import re


pagina = requests.get("https://books.toscrape.com/catalogue/category/books/mystery_3/index.html")
dadosPagina = BeautifulSoup(pagina.text, 'html.parser')


titulos = []
precos = []
avaliacoes = []


titulos_html = dadosPagina.find_all('h3')
for t in titulos_html:
    titulo = t.a['title']
    titulos.append(titulo)


precos_html = dadosPagina.find_all('p', class_='price_color')
for p in precos_html:
    preco_texto = p.get_text().strip()
    preco_texto = re.sub(r'[^\d.,]', '', preco_texto)
    preco_texto = preco_texto.replace(',', '.')
    preco = float(preco_texto)
    precos.append(preco)


avaliacoes_html = dadosPagina.find_all('p', class_='star-rating')
mapa_avaliacoes = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

for a in avaliacoes_html:
    avaliacao = a['class'][1]
    avaliacao_num = mapa_avaliacoes[avaliacao]
    avaliacoes.append(avaliacao_num)


df = pd.DataFrame({
    "Título": titulos,
    "Preço (£)": precos,
    "Avaliação (1-5)": avaliacoes
})


df["Custo-Benefício"] = (df["Avaliação (1-5)"] / df["Preço (£)"]).round(2)


df_filtrado = df.sort_values(by="Custo-Benefício", ascending=False)


print("\n Livros ordenados por custo-benefício:\n")
print(df_filtrado.to_string(index=False))


df_filtrado.to_csv("livros_custo_beneficio.csv", index=False, encoding="utf-8")
print("\n Arquivo 'livros_custo_beneficio.csv' salvo com sucesso!")
