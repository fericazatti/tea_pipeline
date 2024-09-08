import mne
import pywt
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo .edf
file_path = '/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/interim/1Abby_Resting.edf'
raw = mne.io.read_raw_edf(file_path, preload=True)

# Seleccionar el canal de EEG que deseas analizar
# Puedes obtener una lista de los nombres de los canales usando raw.ch_names
eeg_channel = 'Fp1'  # Reemplaza con el nombre del canal

# Extraer los datos del canal seleccionado
eeg_data = raw.get_data(picks=[eeg_channel])[0]

# Obtener la frecuencia de muestreo
sfreq = raw.info['sfreq']

# Descomponer la señal usando la Transformada Wavelet Discreta (DWT)
# Usaremos la wavelet 'db4' (Daubechies 4), que es comúnmente usada en el análisis de EEG
wavelet = 'db4'
coeffs = pywt.wavedec(eeg_data, wavelet, level=5)

# Coeficientes de detalle (bandas de frecuencia)
# Approximation coefficients (a5) are not typically used for EEG band analysis
cA5, cD5, cD4, cD3, cD2, cD1 = coeffs

# Determinar el número de muestras en 10 segundos
duration = 10  # segundos
n_samples = int(duration * sfreq)

# Calcular el tiempo en segundos para el eje x de la señal original
time_original = np.linspace(0, duration, n_samples)

# Ajustar el tiempo para cada coeficiente wavelet
time_cD1 = np.linspace(0, duration, len(cD1[:n_samples]))
time_cD2 = np.linspace(0, duration, len(cD2[:n_samples//2]))
time_cD3 = np.linspace(0, duration, len(cD3[:n_samples//4]))
time_cD4 = np.linspace(0, duration, len(cD4[:n_samples//8]))
time_cD5 = np.linspace(0, duration, len(cD5[:n_samples//16]))
time_cA5 = np.linspace(0, duration, len(cA5[:n_samples//32]))

# Visualizar los coeficientes de detalle y la señal original
plt.figure(figsize=(12, 12))

plt.subplot(7, 1, 1)
plt.plot(time_original, eeg_data[:n_samples], 'k')
plt.title('Original EEG Signal')
plt.xlim(0, duration)

plt.subplot(7, 1, 2)
plt.plot(time_cD1, cD1[:n_samples], 'r')
plt.title('High-gamma (64-128 Hz)')
plt.xlim(0, duration)

plt.subplot(7, 1, 3)
plt.plot(time_cD2, cD2[:n_samples//2], 'g')  # La longitud de cD2 es la mitad de cD1
plt.title('Gamma (32-64 Hz)')
plt.xlim(0, duration)

plt.subplot(7, 1, 4)
plt.plot(time_cD3, cD3[:n_samples//4], 'b')  # La longitud de cD3 es un cuarto de cD1
plt.title('Beta (16-32 Hz)')
plt.xlim(0, duration)

plt.subplot(7, 1, 5)
plt.plot(time_cD4, cD4[:n_samples//8], 'y')  # La longitud de cD4 es un octavo de cD1
plt.title('Alpha (8-16 Hz)')
plt.xlim(0, duration)

plt.subplot(7, 1, 6)
plt.plot(time_cD5, cD5[:n_samples//16], 'm')  # La longitud de cD5 es un dieciseisavo de cD1
plt.title('Theta (4-8 Hz)')
plt.xlim(0, duration)

plt.subplot(7, 1, 7)
plt.plot(time_cA5, cA5[:n_samples//32], 'c')  # La longitud de cA5 es un treintaidosavo de cD1
plt.title('Delta (0-4 Hz)')
plt.xlim(0, duration)

plt.tight_layout()
plt.show()
