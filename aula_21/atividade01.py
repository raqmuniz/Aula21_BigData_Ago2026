import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    cvli = cvli [['aisp', 'cvli']]


except Exception as e:
    print(f'Erro ao obter os dados - {e}')