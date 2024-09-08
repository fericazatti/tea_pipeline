import pandas as pd

def fuse_data(subject):
    path = f'/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/processed/{subject}/'

    # Cargar los archivos CSV en DataFrames
    df1 = pd.read_csv(f'{path}merged_eeg_metrics.csv')
    df2 = pd.read_csv(f'{path}eeg_metrics_antropy_all_reorded.csv')

    # Descartar las primeras dos columnas del segundo DataFrame
    df2 = df2.iloc[:, 2:]

    # Fusionar los DataFrames horizontalmentee
    df_merged = pd.concat([df1, df2], axis=1)

    # Guardar el DataFrame fusionado en un nuevo archivo CSV
    df_merged.to_csv(f'{path}merged_output.csv', index=False)

for subject in range(10,57):
    try:
        fuse_data(subject)
    except:
        print(f'Error en subject: {subject}')