from pandas_datareader import data as pdr
#import fix_yahoo_finance as yf
import yfinance as yf
import datetime
import pandas as pd
from pandas import DataFrame
import numpy as np
import math
import matplotlib.pyplot as plt # Biblioteca para gerar os gráficos - https://matplotlib.org/

###################################
# TRACKER
###################################

#Definir data de inicio e fim
start_sp = datetime.datetime(2000, 7, 12)
end_sp = datetime.datetime(2019, 7, 12)

yf.pdr_override() # arredondando dados para duas casas decimais

# Definindo ativo para gerar base de dados
sp500 = pdr.get_data_yahoo('SPY', start_sp, end_sp)

df = DataFrame(sp500) # Definindo DataFrame


#########################################
# Calculate Relative Strength Index(RSI) #
#########################################

n = 9
prices = df.iloc[:, 3]


deltas = np.diff(prices.T)
seed = deltas[:n + 1]
up = seed[seed >= 0].sum() / n
down = -seed[seed < 0].sum() / n
rs = up / down
rsi = np.zeros_like(prices)
rsi[:n] = 100. - 100. / (1. + rs)

for i in range(n, len(prices)):
    delta = deltas[i - 1]  # cause the diff is 1 shorter

    if delta > 0:
        upval = delta
        downval = 0.
    else:
        upval = 0.
        downval = -delta

    up = (up * (n - 1) + upval) / n
    down = (down * (n - 1) + downval) / n

    rs = up / down
    rsi[i] = 100. - 100. / (1. + rs)




###################################
# MEDIA 200 e 50
###################################



def calcula_resultado(start, end):

    index = 0
    #data50_200 = []

    zerada_long = False;
    zerada_short = False;
    ultimo_long = 0;
    ultimo_short = 0;

    fundo_1 = 100
    fundo_primeiro = 100
    fundo_segundo = 100
    fundo_terceiro = 100
    custo_operacional = 0.9995  # Custo operacional = 0.05%

    grafico_estrategia = []  # Dados do Gráfico Estratégia

    # Boostrap
    bootstrap_3_periodos = math.ceil(df.iloc[:, 4].count() / 3)
    primeiro_periodo = []

    for row_index, row in df.iloc[:,4].iteritems():

        rol_200 = 0
        rol_50 = 0

        # MEDIA 50 periodos
        if index >= 50:
            rol_50 = df.iloc[index - 50:index, 3].mean()  # obtem a os 50 registros anteriores a linha atual
            #data50_200.
            #exit()

        if index >= 200:
            rol_50 = df.iloc[index - 50:index, 3].mean()  # obtem a os 50 registros anteriores a linha atual
            rol_200 = df.iloc[index - 200:index, 3].mean()  # obtem a os 50 registros anteriores a linha atual

            ###################################
            # COMPRA
            ###################################
            if rol_50 > rol_200:
                #Tendencia de compra
                if rsi[index] < 30 :
                    if zerada_long == False :
                        ultimo_long = df.iloc[index, 3]
                        #print ("ENTRADA")
                    zerada_long = True

                    #Grava o close do dia do comprado

            ###################################
            # VENDA
            ###################################
            else:

               if rsi[index] > 70:

                   if zerada_short == False:
                       ultimo_short = df.iloc[index, 3]
                   zerada_short = True
                   #print(df.iloc[index])

                   # Grava o close do dia do comprado

            if rsi[index] < 30:
                # print(compra)
               if zerada_short == True:
                    # print("Compra zerada")
                    #print(df.iloc[index, :])
                    # print(rsi[index])
                    acao_compra = df.iloc[index, 3];
                    #print(ultimo_short)
                    #print(acao_compra)

                    #RESULTADO
                    resultado = (ultimo_short - acao_compra) / acao_compra
                    fundo_1 = (fundo_1+ (fundo_1*resultado)) * custo_operacional
                    zerada_short = False
                    grafico_estrategia.append(fundo_1)


                    print(resultado)

                    # Verificando se pertence ao primeiro periodo
                    if len(grafico_estrategia) > start and len(grafico_estrategia) < end :
                        fundo_primeiro = ( fundo_primeiro + (fundo_primeiro * resultado) ) * custo_operacional
                        primeiro_periodo.append(fundo_primeiro)

            if rsi[index] > 70:
                # print(compra)
                if zerada_long == True:
                    # print ("SAIDA")
                    # print("Compra zerada")
                    # print(rsi[index])
                    venda = df.iloc[index, 3];
                    # print(ultimo_long)
                    # print(venda)
                    # print(ultimo_long)
                    resultado = (((venda - ultimo_long)) / ultimo_long)
                    fundo_1 = (fundo_1 + (fundo_1 * resultado)) * custo_operacional
                    zerada_long = False

                    grafico_estrategia.append(fundo_1)
                    print(resultado)


                    # Verificando se pertence ao primeiro periodo
                    if len(grafico_estrategia) > start and len(grafico_estrategia) < end:
                        fundo_primeiro = (fundo_primeiro + (fundo_primeiro * resultado)) * custo_operacional
                        primeiro_periodo.append(fundo_primeiro)
        index += 1

    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    if end == 0:
        return grafico_estrategia

    else:
        return primeiro_periodo


#calcula_resultado(0,0)


grafico_estrategia = calcula_resultado(0,0)
data = DataFrame(grafico_estrategia)
print(data)

bootstrap_3_periodos = math.ceil(data.count() / 3)
primeiro_periodo = calcula_resultado(0, bootstrap_3_periodos)
segundo_periodo = calcula_resultado(bootstrap_3_periodos+1, bootstrap_3_periodos*2)
terceiro_periodo = calcula_resultado(bootstrap_3_periodos*2+1, bootstrap_3_periodos*3)

data_primeiro = DataFrame(primeiro_periodo)
data_segundo = DataFrame(segundo_periodo)
data_terceiro = DataFrame(terceiro_periodo)



#################################################
# GRAFICOS
######################
# Periodo Total      #
######################
pd.DataFrame(data).plot()
plt.title('Resultado estrategia')
plt.savefig('resultado_estrategia.png', bbox_inches='tight')

######################
# Primeiro periodo   #
######################
pd.DataFrame(data_primeiro).plot()
plt.title('Primeiro Periodo')
plt.savefig('primeiro_periodo.png', bbox_inches='tight')


######################
# Segundo periodo    #
######################
#print(data)
pd.DataFrame(data_segundo).plot()
plt.title('Segundo periodo')
plt.savefig('segundo_periodo.png', bbox_inches='tight')


######################
# Terceiro periodo   #
######################
pd.DataFrame(data_terceiro).plot()
plt.title('Terceiro periodo')
plt.savefig('terceiro_periodo.png', bbox_inches='tight')

exit()

sp500.head()