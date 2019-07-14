
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt # Biblioteca para gerar os gráficos - https://matplotlib.org/
import math

dataFrame = pd.read_csv('trabalho_3/time_series.csv') # Le o arquivo e cria o objeto panda com a instancia do CSV



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
        if row_index >= 100: #pula as 100 primeiras linhas

            last_val = dataFrame.iloc[row_index - 1, index + 1] # obtem o registro anterior
            rol_10 = dataFrame.iloc[row_index-10:row_index, index+1] # obtem a os 10 registros anteriores a linha
            rol_100 = dataFrame.iloc[row_index-100:row_index, index+1] # obtem a os 100 registros anteriores a linha
            daily_var = ((row/last_val) - 1)*100 # variacao diaria

            # Comprado ou vendido
            if rol_10.mean() < rol_100.mean(): #media de 10 e menor que a media de 100: venda, senao compra
                #baixa
                daily_var = (last_val/row) - 1

            last_daily_var = (last_daily_var*(1+daily_var))
            if math.isnan(daily_var): # verifica se a linha esta em branco
                result.append(0)
            else:
                result.append(daily_var) # armazena o dado em um novo array
        else:
            result.append(0)

    consolidado.append(result)
    result = []

final = DataFrame(consolidado)

# Calcula a media de cada linha gerado no consolidado
final.loc['mean'] = final.mean(axis=0, numeric_only=True)
last_val = 100
graph_data = []
for row_index, row in final.T.iloc[:, -1].iteritems():
    # print(row, last_val)
    if isinstance(row, str):
        graph_data.append(0)
    else:
        value = (1+row)*100
        graph_data.append(value)
        last_val = value

graph = DataFrame(graph_data)
final.loc['graph'] = graph_data
final.loc['date'] = dataFrame.iloc[:, 0]

plt.close('all')
print(final.loc[['graph']])

#Gera a imagem do grafico
pd.DataFrame(final.T, columns=['graph', 'date']).plot()
plt.savefig('trabalho_3/grafico.png', bbox_inches='tight')
