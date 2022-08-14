#%% Importações

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% Carregamento

path_folder = r'C:\Users\vinic\python_projects\mancal_project\Mancal com FBG\Mancal com FBG'
name_file = '10hz.txt'
path_file = path_folder+'\\'+name_file

#%% Carregando dados e acertando eles

cols = ['Timestamp','CH 1','CH 2','CH 3','CH 4','CH 5','CH 6','CH 7','CH 8', 'Val1', 'Val2']
data = pd.read_csv(path_file, delimiter='\\t', header=None) # carrega dados após exclusão de cabeçalho
# e tudo que estiver acima

data = data.rename(columns={0:cols[0], 1:cols[1], 2:cols[2], 3:cols[3], 4:cols[4],\
    5:cols[5], 6:cols[6], 7:cols[7], 8:cols[8], 9:cols[9], 10:cols[10]}) # cria novo cabeçalho

# acertando tipo das variáveis
data['Timestamp'] = pd.to_datetime(data['Timestamp']).dt.total_seconds() # transforma em tempo a coluna Timestamp
data['Val1'] = data['Val1'].str.replace(',', '.').astype(float) # transforma em float a coluna Val1
data['Val2'] = data['Val2'].str.replace(',', '.').astype(float)

#%% Criando as variáveis de tempo e valores
plt.plot(data['Timestamp'], data['Val1'])
plt.show()

# %%
