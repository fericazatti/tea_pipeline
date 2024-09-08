import pandas as pd

""" this file reorded merged files of antropy metrics """

subject = 1
for subject in range(10,57):
    path = f'/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/processed/{subject}/'

    # Cargar los archivos CSV en DataFrames
    data = pd.read_csv(f'{path}eeg_metrics_antropy_all.csv')

    # Definir el nuevo orden de las bandas
    band_order = ["cA5", "cD1", "cD2", "cD3", "cD4", "cD5"]

    # Convertir la columna 'Band' a categórica con el orden deseado
    data['Band'] = pd.Categorical(data['Band'], categories=band_order, ordered=True)

    # Agrupar por Electrode y luego ordenar las bandas dentro de cada grupo sin alterar el orden original de los electrodos
    data['Electrode'] = pd.Categorical(data['Electrode'], categories=data['Electrode'].unique(), ordered=True)
    data = data.sort_values(['Electrode', 'Band']).reset_index(drop=True)


    # Guardar el DataFrame reordenado en un nuevo archivo CSV
    data.to_csv(f'{path}eeg_metrics_antropy_all_reorded.csv', index=False)

    print(f"Datos del sujeto {subject} reordenados y guardados en 'reordered_eeg_data.csv'")
