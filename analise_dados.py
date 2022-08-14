# Importações

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% Carregamento

path_folder = r'C:\Users\vinic\python_projects\mancal_project\Mancal com FBG\Mancal com FBG'
name_file = '20hz.txt'
path_file = path_folder+'\\'+name_file

# %% Carregando dados e acertando eles

sample_time = 1/1000  # T para 1000 hz

cols = ['Timestamp', 'CH 1', 'CH 2', 'CH 3', 'CH 4',
        'CH 5', 'CH 6', 'CH 7', 'CH 8', 'Val1', 'Val2']
# carrega dados após exclusão de cabeçalho
data = pd.read_csv(path_file, delimiter='\\t', header=None)
# e tudo que estiver acima

data = data.rename(columns={0: cols[0], 1: cols[1], 2: cols[2], 3: cols[3], 4: cols[4],
                            5: cols[5], 6: cols[6], 7: cols[7], 8: cols[8], 9: cols[9], 10: cols[10]})  # cria novo cabeçalho

# acertando tipo das variáveis
# transforma em tempo a coluna Timestamp
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data['Val1'] = data['Val1'].str.replace(',', '.').astype(
    float)  # transforma em float a coluna Val1
data['Val2'] = data['Val2'].str.replace(',', '.').astype(float)
seconds = np.linspace(0, len(data['Timestamp'])
                      * sample_time, len(data['Timestamp']))

# %% Plotando as variáveis
n_max1 = 100  # número de pontos a serem plotados, devido à dificuldade de mostrar todos
media_sensor1 = np.mean(data['Val1'])
media_sensor2 = np.mean(data['Val2'])


plt.figure(1)
plt.plot(seconds[:n_max1], data['Val1'].iloc[:n_max1], label='Sensor 1')
plt.plot(seconds[:n_max1], data['Val2'].iloc[:n_max1], label='Sensor 2')
plt.xlabel('tempo (s)')
plt.ylabel('comprimento da onda refletida (nm)')
plt.suptitle(f'DADOS DE {name_file[0:4].upper()} NO DOMÍNIO DO TEMPO ')
plt.title(
    f'Média sensor 1 = {round(media_sensor1, 2)}; Média sensor 2 = {round(media_sensor2)} \n', y=0.98)
plt.legend()
plt.subplots_adjust(top=0.83)
plt.show()

# %% FFT

#sample_time = 1

data_freq = np.fft.fftfreq(len(data['Timestamp']), d=sample_time)
data_freq = data_freq[data_freq >= 0]
data_FFT1 = np.fft.fft(data['Val1']-media_sensor1)
data_FFT2 = np.fft.fft(data['Val2']-media_sensor2)

#plt.plot(data['Timestamp'], data_freq)

n_max = len(data_freq)

"""max_FFT1 = max(abs(data_FFT1[:n_max]))
max_freq1 = data_freq[list(data_FFT1[:n_max]).index(abs(max_FFT1))]
max_FFT2 = max(abs(data_FFT2[:n_max]))
max_freq2 = data_freq[list(data_FFT2[:n_max]).index(abs(max_FFT2))]"""

# %% Plot FFT

#n_max2 = 100

plt.figure(2)
plt.plot(data_freq[:n_max], data_FFT1[:n_max], label='Sensor 1')
plt.plot(data_freq[:n_max], data_FFT2[:n_max], label='Sensor 2')
plt.xlabel('frequência (hz)')
plt.ylabel('comprimento da onda refletida (nm)')
plt.suptitle(
    f'DADOS DE {name_file[0:4].upper()} NO DOMÍNIO DA FREQUÊNCIA', y=0.99)
#plt.title(f'Sensor 1: valor de pico = {round(float(max_FFT1), 2)}, frequência = {round(max_freq1, 4)} \nSensor 2: valor de pico = {round(float(max_FFT2),2)}, frequência = {round(max_freq2, 4)} \n', y=0.98)
plt.legend()
plt.subplots_adjust()#top=0.78)
plt.show()

# %% Obtendo o maior pico se frequência maior que frequencia de corte
freq_corte = 5

n_maior = len(data_freq)
n_menor = n_maior-len(data_freq[abs(data_freq) > freq_corte])

top_sensor1 = max(abs(data_FFT1[n_menor:n_maior]))
top_sensor2 = max(abs(data_FFT2[n_menor:n_maior]))

top_freq1 = data_freq[n_menor:][list(abs(
    data_FFT1[n_menor:n_maior])).index(abs(top_sensor1))]
top_freq2 = data_freq[n_menor:][list(abs(
    data_FFT2[n_menor:n_maior])).index(abs(top_sensor2))]


# %%
plt.figure(3)
plt.scatter(top_freq1, top_sensor1, label='Sensor 1')
plt.scatter(top_freq2, top_sensor2, label='Sensor 2')
plt.xlabel('frequência (hz)')
plt.ylabel('comprimento da onda refletida (nm)')
plt.suptitle(f'MAIORES PICOS ABSOLUTOS DE {name_file[0:4].upper()} NO DOMÍNIO DA FREQUÊNCIA SE F>{freq_corte}HZ', y=0.99)
plt.title(f'Sensor 1: valor de pico = {round(float(top_sensor1), 2)}, frequência = {round(top_freq1, 4)} \nSensor 2: valor de pico = {round(float(top_sensor2),2)}, frequência = {round(top_freq2, 4)} \n', y=0.98)
plt.legend()
plt.subplots_adjust(top=0.78)
plt.show()

# %%
