
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt # Biblioteca para gerar os gráficos - https://matplotlib.org/
import math
import numpy as np

dataFrame = pd.read_csv('trabalho_4/forward.csv') # Le o arquivo e cria o objeto panda com a instancia do CSV

 # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.shape.html

consolidado = [] # Variavel com o consolidado geral
result = [] # Variavel com o consolidado por coluna

rank = dataFrame.rank(axis=1).T
col_length = rank.shape[1]


# Apos rankear tomamos recursos na metade com menores taxas e aplicamos na outra metade com maiores taxas.
for index in range(0, col_length):  # lista as colunas do csv

    df = rank.iloc[:, index] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html

    for row_index, row in df.iteritems():
        if row <= 4:
            result.append('Aplico')
        else :
            result.append('Tomo')


    consolidado.append(result)
    result = []


consolidado_tomo_aplico = DataFrame(consolidado).T


consolidado_rank = []
trackerDataFrame = pd.read_csv('trabalho_4/tracker.csv')


col_length = trackerDataFrame.shape[1]

# Momentum
for index_rank in range(0, col_length-1):  # lista as colunas do csv

    df = trackerDataFrame.iloc[:, index_rank+1] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
    for row_index, row in df.iteritems():
        if row_index >= 1:
            data_row = trackerDataFrame.iloc[row_index-1, index_rank+1]
            result.append( (row - data_row) / data_row )
            last_val = (row - data_row) / data_row
        else:
            last_val = 100

    consolidado_rank.append(result)
    result = []


# Média de 10 e média de 100
consolidado_rank_df = DataFrame(consolidado_rank).T
col_length = consolidado_rank_df.shape[1] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.shape.html

#Declarando variaveis
consolidado_media = [] # Variavel com o consolidado geral
result = [] # Variavel com o consolidado por coluna
days = [] # Variavel com os dados diarios



# Gerando dataFrame
for index in range(0, col_length):  # lista as colunas do csv

    df = consolidado_rank_df.iloc[:, index] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
    last_daily_var = 100 # quantidade de dias para gerar a media


    for row_index, row in df.iteritems():

        # Realiza os calculos apos a 100 linha
        if row_index >= 100: #pula as 100 primeiras linhas

            last_val = consolidado_rank_df.iloc[row_index - 1, index ] # obtem o registro anterior
            rol_10 = consolidado_rank_df.iloc[row_index-10:row_index, index] # obtem a os 10 registros anteriores a linha
            rol_100 = consolidado_rank_df.iloc[row_index-100:row_index, index] # obtem a os 100 registros anteriores a linha
            if last_val == 0:
                daily_var = 0
            else:
                daily_var = ((row/last_val) - 1)*100 # variacao diaria
            # Comprado ou vendido
            if rol_10.mean() < rol_100.mean(): #media de 10 e menor que a media de 100: venda, senao compra
                #baixa
                result.append('Venda')
            else:
                result.append('Compra')
        else:
            result.append(0)

    consolidado_media.append(result)
    result = []

final = DataFrame(consolidado_media)






# Média de 10 e média de 100
consolidado_rank_df = DataFrame(dataFrame)
col_length = consolidado_rank_df.shape[1] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.shape.html

#Declarando variaveis
consolidado_media = [] # Variavel com o consolidado geral
result = [] # Variavel com o consolidado por coluna
days = [] # Variavel com os dados diarios



# Gerando dataFrame
for index in range(0, col_length-1):  # lista as colunas do csv

    df = consolidado_rank_df.iloc[:, index+1] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
    last_daily_var = 100 # quantidade de dias para gerar a media


    for row_index, row in df.iteritems():
        # Realiza os calculos apos a 100 linha
        if row_index >= 100: #pula as 100 primeiras linhas

            last_val = consolidado_rank_df.iloc[row_index - 1, index+1] # obtem o registro anterior
            rol_10 = consolidado_rank_df.iloc[row_index-10:row_index, index+1] # obtem a os 10 registros anteriores a linha
            rol_100 = consolidado_rank_df.iloc[row_index-100:row_index, index+1] # obtem a os 100 registros anteriores a linha
            if last_val == 0:
                daily_var = 0
            else:
                daily_var = ((row/last_val) - 1)*100 # variacao diaria
            # Comprado ou vendido
            if rol_10.mean() < rol_100.mean(): #media de 10 e menor que a media de 100: venda, senao compra
                #baixa
                result.append('Venda')
            else:
                result.append('Compra')
        else:
            result.append(0)

    consolidado_media.append(result)
    result = []

final_forward = DataFrame(consolidado_media)




#SUPER SINAL - Combinação dos 3 sinais
#Super aplicação
#Taxas altas - Aplico nelas + Momentum de venda e Value de venda
#Super sinal de tomar emprestado
#Taxas baixas - Tomo recursos nelas + Momentum de compra e Value de compra


#Declarando variaveis
consolidado_super_sinal = [] # Variavel com o consolidado geral
result = [] # Variavel com o consolidado por coluna
days = [] # Variavel com os dados diarios

# Gerando dataFrame
for index in range(0, col_length-1):  # lista as colunas do csv

    df = consolidado_rank_df.iloc[:, index+1] # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
    last_daily_var = 100 # quantidade de dias para gerar a media


    for row_index, row in df.iteritems():
        if row_index >= 2: #pula as 2 primeiras linhas
            tomo_e_aplico = consolidado_tomo_aplico.T.iloc[row_index, index]
            momentum = final.T.iloc[row_index, index] #Momentum
            value = final_forward.T.iloc[row_index, index]

            if tomo_e_aplico == "Aplico":
                if momentum == "Venda":
                    if value == "Venda":
                        result.append("Super sinal de aplicação")

            else:
                if tomo_e_aplico == "Tomo":
                    if momentum == "Compro":
                        if value == "Compro":
                            result.append("Super sinal de tomar emprestado")
                else :
                    result.append("-")

        else:
            result.append(0)

    consolidado_super_sinal.append(result)
    result = []

super_sinal = DataFrame(consolidado_super_sinal)

print(super_sinal.T)
exit()



print ("Tomo e aplico")
print(consolidado_tomo_aplico.T)

print("Taxa do Momentum")
print(DataFrame(consolidado_rank).T)
pd.DataFrame(consolidado_rank).T.plot()
plt.savefig('trabalho_4/taxa_do_momentum.png', bbox_inches='tight')

print("Momentum")
print(final.T)

print("Value")
print(final_forward.T)

print("Super sinal")
print(super_sinal.T)