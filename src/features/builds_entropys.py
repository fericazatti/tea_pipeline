import mne
import pywt
import numpy as np
import antropy as ant
import pandas as pd
import gc


# Cargar el archivo .edf
for subject in range(9,10):
    file_path = f'/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/interim/{subject}Abby_Resting.edf'
    raw = mne.io.read_raw_edf(file_path, preload=True)

    # Lista de electrodos a analizar
    electrodes = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'PO3', 'P4']

    # Obtener la frecuencia de muestreo
    sfreq = raw.info['sfreq']

    # Duración de los segmentos a analizar (60 segundos)
    duration = 60  # segundos
    n_samples = int(duration * sfreq)

    # Calcular las métricas usando antropy
    def calculate_antropy_metrics(segment):
        app_entropy = ant.app_entropy(segment)
        perm_entropy = ant.perm_entropy(segment)
        sample_entropy = ant.sample_entropy(segment)
        svd_entropy = ant.svd_entropy(segment)
        return app_entropy, perm_entropy, sample_entropy, svd_entropy

    # Crear la cabecera del archivo CSV
    header = ['Electrode', 'Band', 'Approximate Entropy', 'Permutation Entropy', 'Sample Entropy', 'SVD Entropy']

    # DataFrame global para almacenar todas las métricas
    all_metrics_df = pd.DataFrame(columns=header)

    # Procesar cada electrodo y cada banda de frecuencia, guardando los resultados en un DataFrame global
    for electrode in electrodes:
        try:
            # Extraer los datos del canal seleccionado
            eeg_data = raw.get_data(picks=[electrode])[0]

            # Descomponer la señal usando la Transformada Wavelet Discreta (DWT)
            wavelet = 'db4'
            coeffs = pywt.wavedec(eeg_data, wavelet, level=5)

            # Coeficientes de detalle (bandas de frecuencia)
            cA5, cD5, cD4, cD3, cD2, cD1 = coeffs

            # Obtener segmentos de interés para cada coeficiente
            segments = {
                "cD1": cD1[:n_samples],
                "cD2": cD2[:n_samples // 2],
                "cD3": cD3[:n_samples // 4],
                "cD4": cD4[:n_samples // 8],
                "cD5": cD5[:n_samples // 16],
                "cA5": cA5[:n_samples // 32]
            }

            # Calcular métricas para cada coeficiente y almacenar en el DataFrame global
            for key, segment in segments.items():
                try:
                    app_entropy, perm_entropy, sample_entropy, svd_entropy = calculate_antropy_metrics(segment)
                    row = [electrode, key, app_entropy, perm_entropy, sample_entropy, svd_entropy]
                    all_metrics_df.loc[len(all_metrics_df)] = row

                    # Liberar memoria después de cada banda de frecuencia
                    del row
                    gc.collect()

                except Exception as e:
                    print(f"Error processing electrode {electrode} and band {key}: {e}")

            # Liberar memoria después de cada electrodo
            del eeg_data, coeffs, segments
            gc.collect()

        except Exception as e:
            print(f"Error processing electrode {electrode}: {e}")


    # Guardar todas las métricas en un solo archivo CSV
    output_file = f'/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/processed/0{subject}/eeg_metrics_antropy_all.csv'
    all_metrics_df.to_csv(output_file, index=False)

    print("Metrics have been saved to a single CSV file.")