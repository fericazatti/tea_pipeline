import mne
import pywt
import numpy as np
import antropy as ant
import pandas as pd
import gc
import nolds

for i in range(53,57):
    subject = i
    file_path = f'/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/interim/{subject}Abby_Resting.edf'
    raw = mne.io.read_raw_edf(file_path, preload=True)

    # Lista de electrodos a analizar
    electrodes = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'PO3', 'P4']

    # Obtener la frecuencia de muestreo
    sfreq = raw.info['sfreq']

    # Duración de los segmentos a analizar (60 segundos)
    duration = 60  # segundos
    n_samples = int(duration * sfreq)

    # Calcular las métricas usando nolds
    def calculate_nolds_metrics(segment, min_tsep=10):
        hurst = nolds.hurst_rs(segment)
        dfa = nolds.dfa(segment)
        lyap_r = nolds.lyap_r(segment, min_tsep=min_tsep)
        sampen = nolds.sampen(segment)
        corr_dim = nolds.corr_dim(segment, emb_dim=10)
        return hurst, dfa, lyap_r, sampen, corr_dim

    # Crear la cabecera del archivo CSV
    header = ['Electrode', 'Band', 'Hurst', 'DFA', 'Lyapunov', 'Sample Entropy', 'Correlation Dimension']

    # Procesar cada electrodo y cada banda de frecuencia, guardando los resultados en archivos CSV separados
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

            # Calcular métricas para cada coeficiente y guardar en archivos separados
            for key, segment in segments.items():
                try:
                    hurst, dfa, lyap_r, sampen, corr_dim = calculate_nolds_metrics(segment, min_tsep=10)
                    row = [electrode, key, hurst, dfa, lyap_r, sampen, corr_dim]

                    # Crear un DataFrame con los resultados
                    df = pd.DataFrame([row], columns=header)

                    # Guardar los resultados en un archivo CSV separado para cada banda de frecuencia de cada electrodo
                    output_file = f'data/processed/{subject}/eeg_metrics_{electrode}_{key}.csv'
                    df.to_csv(output_file, index=False, mode='a', header=not pd.io.common.file_exists(output_file))

                    # Liberar memoria después de cada banda de frecuencia
                    del df, row
                    gc.collect()

                except Exception as e:
                    print(f"Error processing electrode {electrode} and band {key}: {e}")

            # Liberar memoria después de cada electrodo
            del eeg_data, coeffs, segments
            gc.collect()

        except Exception as e:
            print(f"Error processing electrode {electrode}: {e}")

    print(f'Paciente {subject} procesado correctamente')