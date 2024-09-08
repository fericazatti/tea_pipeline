from mne import io
import mne
import numpy as np

from mne_connectivity import spectral_connectivity_epochs
from mne_connectivity.viz import plot_connectivity_circle

import matplotlib.pyplot as plt
import networkx as nx

import antropy as ant

directory = "/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/interim/" 


raw = io.read_raw_edf(directory + '1Abby_Resting.edf')

sfreq = raw.info['sfreq']
duration  = round(60 * sfreq)
data = raw.get_data(stop = duration)

ent = []
for ch, data_ch in zip(raw.ch_names, data):
    ent.append(ant.app_entropy(data_ch))
    #print('Variable entropia del canal {}: {}'.format(ch, ent))

ent_ch = np.column_stack((raw.ch_names, ent))

# Crear una figura y ejes
fig, ax = plt.subplots()

valores_entropia = ent_ch[:, 1].astype(float)

# Graficar el histograma
ax.hist(valores_entropia, bins=10, color='skyblue', edgecolor='black')

# Etiquetas y título
ax.set_xlabel('Entropía')
ax.set_ylabel('Frecuencia')
ax.set_title('Histograma de Valores de Entropía')

# Mostrar la gráfica
plt.show()

# Obtener nombres de canales y valores de entropía
nombres_canales = ent_ch[:, 0]
valores_entropia = ent_ch[:, 1].astype(float)

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(6, 12))

# Graficar diagrama de barras
ax.barh(nombres_canales, valores_entropia)

# Etiquetas y título
ax.set_xlabel('Valor de Entropía')
ax.set_ylabel('Canales de EEG')
ax.set_title('Valores de Entropía para Canales de EEG')

# Mostrar la gráfica
plt.show()

ent = []
for ch, data_ch in zip(raw.ch_names, data):
    ent.append(ant.hjorth_params(data_ch))
    #print('Variable entropia del canal {}: {}'.format(ch, ent))


# Agregar los nuevos valores de entropía a tu arreglo_eeg
arreglo_eeg = np.column_stack((ent_ch, ent))

# Obtener nombres de canales y valores de entropía
nombres_canales = arreglo_eeg[:, 0]
valores_entropia = arreglo_eeg[:, 1].astype(float)
valores_entropia_2 = arreglo_eeg[:, 2].astype(float)  # Nuevos valores de entropía

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(8, 6))

# Graficar diagrama de dispersión (scatter plot)
ax.scatter(valores_entropia, valores_entropia_2, color='red')

# Etiquetas y título
ax.set_xlabel('Valor de Entropía 1')
ax.set_ylabel('Valor de Entropía 2')
ax.set_title('Diagrama de Dispersión de Valores de Entropía')
ax.grid()

# Mostrar la gráfica
plt.show()

# Función para calcular todas las métricas de entropía
def calculate_entropies(data):
    entropy_functions = [
        ant.app_entropy,
        ant.perm_entropy,       # Permutation Entropy
        ant.sample_entropy,     # Sample Entropy
        ant.svd_entropy,        # Singular Value Decomposition Entropy          
    ]
    
    metrics = []
    for func in entropy_functions:
        try:
            entropy_value = func(data)
            metrics.append(entropy_value)
        except Exception as e:
            metrics.append(np.nan)  # Use NaN to indicate an error
            print(f"Error calculating {func.__name__}: {e}")
    return metrics


data = raw.get_data()

# Número de electrodos y métricas de entropía
n_electrodes = data.shape[0]
n_metrics = 4  # Número de funciones de entropía que estamos utilizando

# Crear una matriz para almacenar los valores de entropía
entropy_matrix = np.zeros((n_electrodes, n_metrics))

# Calcular las métricas de entropía para cada electrodo
for i in range(n_electrodes):
    entropy_matrix[i, :] = calculate_entropies(data[i, :])

# Mostrar la matriz de entropía
print("Matriz de Entropía (Electrodos vs. Métricas de Entropía):")
print(entropy_matrix)