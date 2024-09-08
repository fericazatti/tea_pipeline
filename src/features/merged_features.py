""" 
This script merged all nolds features stored in individual files
"""

import pandas as pd
import glob
for subject in range(2,10):
    path = f'/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/processed/0{subject}/'
    # Definir los electrodos y componentes
    electrodes = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'PO3', 'P4']
    components = ['cA5', 'cD1', 'cD2', 'cD3', 'cD4', 'cD5']

    # Inicializar una lista para almacenar los DataFrames
    data_frames = []
    try:
        # Iterar sobre cada electrodo y componente
        for electrode in electrodes:
            for component in components:
                # Construir el nombre del archivo
                file_name = f"{path}eeg_metrics_{electrode}_{component}.csv"
                try:
                    # Leer el archivo CSV en un DataFrame
                    df = pd.read_csv(file_name)
                    # Añadir columnas de Electrode y Band
                    df['Electrode'] = electrode
                    df['Band'] = component
                    # Añadir el DataFrame a la lista
                    data_frames.append(df)
                except FileNotFoundError:
                    print(f"Archivo {file_name} no encontrado. Continuando con el siguiente archivo.")

        # Concatenar todos los DataFrames en uno solo
        merged_df = pd.concat(data_frames, ignore_index=True)

    # Guardar el DataFrame resultante en un archivo CSV
    
        merged_df.to_csv(f"{path}merged_eeg_metrics.csv", index=False)
    except Exception as e:
        print(f'Problemas en subject: {subject}')