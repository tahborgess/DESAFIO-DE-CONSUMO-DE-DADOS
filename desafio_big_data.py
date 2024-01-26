# -*- coding: utf-8 -*-
"""Desafio Big Data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ehch7S-k9KMHypvf-92Viyf0aQQiJnTV

## Passo 1: Importar as funções
"""

import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil

"""## Passo 2: Conectar na API"""

def fetch_data(endpoint):
    base_url = "https://swapi.dev/api/"
    url = base_url + endpoint
    results = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results.extend(data['results'])
            url = data['next']
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            break
    return results

"""## Passo 3: Transformando em um dataframe"""

endpoints = ['starships','people','vehicles','planets']

# Conectando os dados de starships
starships_data = fetch_data('starships')

# Convertendo os dados em um dataframe utilizando pandas.
starships_df = pd.DataFrame(starships_data)

# Exibindo as primeiras 5 linhas do dataframe.
starships_df.head()

"""## Passo 4: Criação do banco de dados"""

import sqlite3

def save_to_sqlite(df, db_name, table_name):
    # Criando a conexão com o SQLite database
    conn = sqlite3.connect(db_name)
    # Salvando o dataframe em uma tabela no database
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    # Fechando a conexão
    conn.close()

for x in endpoints:
  print(f"Criando tabelas do endpoint: {x}")
  save_to_sqlite(pd.DataFrame(fetch_data(x)).astype(str),'swapi.db',x)

"""## Passo 5: Análises"""

import pandas as pd
import sqlite3

def read_table_as_dataframe(db_name, table_name):
    """
    Lendo a tabela do database e retornando um dataframe, utilizando pandas.

    Parâmetros:
    db_name (str): Nome do arquivo.
    table_name (str): Nome da tabela que será lida.

    Retorna:
    Dataframe: Um dataframe contendo os dados da tabela específica.
    """
    # Criando a conexão com o SQLite database
    conn = sqlite3.connect(db_name)

    # Lendo a tabela do dataframe
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)

    # Fechando a conexão
    conn.close()

    return df


# Exemplo
db_name = 'swapi.db'
table_name = 'starships'
starships_df = read_table_as_dataframe(db_name, table_name)

starships_df.head()

read_table_as_dataframe('swapi.db','vehicles') #Lendo a tabela que contém os veículos.

"""## 5.1 - Qual é o personagem que apareceu em mais filmes de Star Wars?"""

res = fetch_data('people')

df = pd.DataFrame(res)

df.head()

df['qtd_films'] = df['films'].apply(len)

df.head()

display(
    df.qtd_films.value_counts(dropna=False,ascending=False),
    df[df.qtd_films==df.qtd_films.max()].name
)

"""## 5.2 - Quais são os planetas mais quentes do universo de Star Wars?"""

res2 = fetch_data('planets')
res2

qtd_res2 = fetch_data('planets')

df2 = pd.DataFrame(res2)

df2.head()

display(
    df2.climate.value_counts(dropna=False,ascending=False),
    df2.terrain.value_counts(dropna=False,ascending=False)
)

df2[df2['name'].isin(['Tatooine','Mustafar','Jakku','Geonosis','Sullust'])] # Resposta -> Planetas mais quentes, considerando as colunas terrain e climate.

df2.climate.value_counts()

len(df2)

"""## 5.3 - Quais são as naves espaciais mais rápidas do universo de StarWars?"""

starships_df

starships_df.sort_values(by='max_atmosphering_speed', ascending=False)

import re

def capture_first_number(text):
    try:
      pattern = r'\d+(\.\d+)?'  # Padrão para combinar números inteiros e floats.
      match = re.search(pattern, text)
      if match:
        return float(match.group())
      else:
        return None
    except:
      return None


# Aplicando a função à coluna 'texto'.
starships_df['velocidade_tratada'] = starships_df['max_atmosphering_speed'].apply(capture_first_number).astype('float')

starships_df.sort_values(by='velocidade_tratada', ascending=False).head() # Top 5 das naves mais rápidas