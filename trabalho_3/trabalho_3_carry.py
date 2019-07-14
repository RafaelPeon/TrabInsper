
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt # Biblioteca para gerar os gráficos - https://matplotlib.org/
import math
import numpy as np

dataFrame = pd.read_csv('trabalho_3/carry.csv') # Le o arquivo e cria o objeto panda com a instancia do CSV



col_length = dataFrame.shape[1] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.shape.html

#Declarando variaveis
consolidado = [] # Variavel com o consolidado geral
result = [] # Variavel com o consolidado por coluna
days = [] # Variavel com os dados diarios



# Gerando dataFrame
for index in range(0, col_length-1):  # lista as colunas do csv

    df = dataFrame.iloc[:, index+1] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
    last_daily_var = 100 # quantidade de dias para gerar a media


    for row_index, row in df.iteritems():
        # Realiza os calculos apos a 100 linha
        if row_index >= 1: #pula as 100 primeiras linhas

            last_val = dataFrame.iloc[row_index - 1, index + 1] # obtem o registro anterior

            result.append( (row-last_val) / row )


    consolidado.append(result)
    result = []

rank = DataFrame(consolidado).T.rank(axis=1)
col_length = rank.shape[1]
consolidado_rank = []
result_rank = []



for index_rank in range(0, col_length-1):  # lista as colunas do csv

    df = rank.iloc[:, index_rank] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
    last_daily_var = 100 # quantidade de dias para gerar a media


    for row_index, row in df.iteritems():
        # Realiza os calculos apos a 100 linha
        data_row = dataFrame.iloc[row_index, index_rank+1]
        last_val = dataFrame.iloc[row_index - 1, index_rank+1]
        if row_index == 1:
            result_rank.append(100)

        if row_index >= 2:
            if data_row <= 4: #pula as 100 primeiras linhas
                 # obtem o registro anterior
                result_rank.append( ((data_row-last_val) / data_row ))
            else:
                result_rank.append(((last_val - data_row) / data_row ) )

    consolidado_rank.append(result_rank)
    result_rank = []



final_rank = DataFrame(consolidado_rank).T
col_length = final_rank.shape[1]
final_geral = []
consolidado_final = []

for index_geral in range(0, col_length):  # lista as colunas do csv

    df = final_rank.iloc[:, index_geral] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html

    for row_index, row in df.iteritems():
        # Realiza os calculos apos a 100 linha
        if row_index >= 1:
            data_row = final_rank.iloc[row_index, index_geral]
            final_geral.append( last_val + (last_val * data_row))
            last_val = last_val + (last_val * data_row)
        else :
            last_val = 100

    consolidado_final.append(final_geral)
    final_geral = []




print(DataFrame(consolidado_final).T)

final = DataFrame(consolidado_final)

#Gera a imagem do grafico
pd.DataFrame(DataFrame(consolidado_final).T).plot()
plt.savefig('trabalho_3/carry.png', bbox_inches='tight')
