import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_crimes_violentos = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(crimes violentos)

     # delimitando os dados
    df_cvli = df_crimes_violentos[['aisp', 'cvli']]
    #print(cvli.head(30))
    #print(cvli.tail(30))


     # ### PREPARANDO OS DADOS
        # Totalizando os crimes violentos por batalhão (Var Qualitativa 'aisp' e Var Quant 'cvli')
    df_cvli = df_cvli.groupby('aisp', as_index=False)['cvli'].sum()
    
    
        # Ordenando os dados
    df_cvli = df_cvli.sort_values(
            by='cvli',
            ascending=False
        )
    
    print(df_cvli.head(10))
        # print(df_roubo_veiculo.tail(10))
    
        
except Exception as e:
        print(f'Erro ao obter os dados - {e}')

#Obtendo as medidas de tendência central

try:
    print(f'\nObtendo informações sobre crimes violentos...')
    array_cvli = np.array(df_cvli['cvli'])

    media_cvli = np.mean(array_cvli)
    mediana_cvli = np.median(array_cvli)
    distancia = abs(
        (media_cvli - mediana_cvli) / mediana_cvli * 100
    )

    print('\nMedidas de Tendência Central')
    print(f'Média: {media_cvli}')
    print(f'Mediana: {mediana_cvli}')
    print(f'Distância Média - Mediana: {distancia:.2f}%')


except Exception as e:
    print(f'Obtendo Medidas - {e}')



# Calculando os quartis
try:
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_cvli, .25)
    q2 = np.quantile(array_cvli, .50)
    q3 = np.quantile(array_cvli, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Batalhões c/ menos ocorrências de crimes violentos
    df_cvli_menores = df_cvli[
        df_cvli['cvli'] < q1
    ]

    # Batalhões c/ maiores ocorrências de crimes violentos
    df_cvli_maiores = df_cvli[
        df_cvli['cvli'] > q3
    ]

    # Menores
    print('\nBatalhões com menores taxas de crimes violentos')
    print(30*'-')
    print(df_cvli_menores.sort_values(by='cvli', ascending=True))
    # Exportando o dataframe
    # index=False - Não exporta os índices. Salva os dados das colunas munic e roubo_veiculo
    # sep=';' - Altera o separador de colunas para ';'
    # encoding='iso-8859-1' - Informa o encoding para salvar o csv. "Pode ser o mesmo"
    df_cvli_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    # Maiores
    print('\nBatalhões com maiores taxas de crimes violentos')
    print(30*'-')
    print(df_cvli_maiores.sort_values(by='cvli', ascending=False))
    # Exportando o dataframe
    df_cvli_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')


# Medidas de Posição e Dispersão
try:
    print('\nCalculando a Amplitude Total')
    # amplitude_total = maior - menor
    # Quanto mais próximo do 0, mais homogêneos são os dados do conjunto.
    # Quanto mais próximo do maior valor, mais heterogêneos são os dados do conjunto.
    maximo = np.max(array_cvli)
    minimo = np.min(array_cvli)
    amplitude = maximo - minimo

except Exception as e:
    print(f'Erro ao calcular a amplitude: {e}')
    

# Achando os outliers
try:
    # Intervalo Interquartil (IQR)
    # É a amplitude dos dados mais centrais
    # Ignora o maior e o menor valor
    # Não sofre interferência dos Extremos
    # Quanto mais próximo do 0, mais homogêneos são os dados mais centrais
    # Quanto mais próximo do Q3, mais heterogêneos são os dados dos 50% mais centrais
    # 970.75
    iqr = q3 - q1

    # calculando os limites
    # Superior
    limite_superior = q3 + (1.5 * iqr)

    # Inferior
    limite_inferior = q1 - (1.5 * iqr)


    print(f'\nLimite Superior: {limite_superior}')
    print(f'\nLimite Inferior: {limite_inferior}')

    # Filtrando os outliers menores
    df_cvli_outliers_menores = (
        df_cvli[df_cvli['cvli'] < limite_inferior]
    )

    # Printando os outliers menores
    print('\nBatalhões com outliers inferiores')
    print(30*'-')
    if len(df_cvli_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_cvli_outliers_menores)
    

    # Printando os outliers maiores
    df_cvli_outliers_maiores = (
        df_cvli[df_cvli['cvli'] > limite_superior]
    )

    print('\nBatalhões com outliers superiores')
    print(30*'-')
    if len(df_cvli_outliers_maiores) == 0:
        print('Não há outliers Superiores')
    else:
        print(df_cvli_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers {e}')


try:
    print('\nMostrando Medidas')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')

    print(f'\nMédia: {media_cvli}')
    print(f'Mediana: {mediana_cvli}')
    print(f'Distância: {distancia}')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')    

except Exception as e:
    print(f'\nErro ao mostrar medidas {e}')


# # Plotando Gráfico
# try:
#     print('Plotando BoxPlot')
#     # pip install matplotlib 
#     # import matplotlib.pyplot as plt

#     # BoxPlot
#     # Retirar os outliers - showfliers=False  
#     # Coloar a média - showmeans=True
#     plt.boxplot(df_cvli['cvli'], orientation='horizontal', showmeans=True)
#     plt.show()

# except Exception as e:
#     print(f'Erro ao plotar o grafico: {e}')


try:
    print('\nInformações de Crimes violentos por batalhões do RJ')
    plt.figure(figsize=(16, 10))


    # Posição 01 - Boxplot
    plt.subplot(1, 2, 1)

    plt.boxplot(df_cvli['cvli'], orientation='horizontal', showmeans=True)
    plt.title('Distribuição dos dados')
    plt.xlabel('Crimes violentos')
    # plt.ylabel('Batalhões')


    plt.subplot(1, 2, 2)
    plt.text(0.1, 0.95, f'Limite Inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.90, f'Mínimo: {minimo}', fontsize=12)
    plt.text(0.1, 0.85, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.80, f'Q2: {q2}', fontsize=12)
    plt.text(0.1, 0.75, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.70, f'Limite Superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.65, f'Máximo: {maximo}', fontsize=12)

    plt.text(0.1, 0.55, f'Mediana: {mediana_cvli}', fontsize=12)
    plt.text(0.1, 0.50, f'Média: {media_cvli}', fontsize=12)
    plt.text(0.1, 0.45, f'IQR Intervalo Interquartil: {iqr}', fontsize=12)
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.text(0.1, 0.35, f'Distância: {distancia}', fontsize=12)
    plt.axis('off')
    
    
    plt.suptitle('Informações sobre Crimes violentos') 

    plt.show()

except Exception as e:
    print(f'Erro ao plotar o grafico: {e}')


# Barras | 10 Menores Valores
    plt.subplot(2, 2, 3)

    df_cvli_10menores = (
        df_cvli_menores.tail(10)
    )

    plt.barh(df_cvli_10menores['aisp'], df_cvli_10menores['cvli'])
    plt.ylabel('aisp')
    plt.xlabel('cvli')
    plt.title('Bottom 10 - Batalhões com menores taxas de crimes violentos')


    # 4ª Posição - Colunas | Top 10 Maiores
    plt.subplot(2, 2, 4)
    # Filtrando e Ordenando
    df_cvli_10maiores = (
        df_cvli_maiores
        .head(10)
        .sort_values(by='cvli', ascending=True)
    )

    plt.bar(df_cvli_10maiores['aisp'], df_cvli_10maiores['cvli'])
    plt.xlabel('aisp')
    plt.ylabel('cvli')
    plt.xticks(rotation=45, ha='right')  # Rotaciona


    
    plt.suptitle('Informações sobre Crimes violentos') 

    plt.show()

except Exception as e:
    print(f'Erro ao plotar o grafico: {e}')
    
    
   