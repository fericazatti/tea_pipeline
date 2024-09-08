import pandas as pd
import os
import glob

# Ruta base donde se encuentran los archivos de los sujetos
base_dir = '/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/processed'

# Obtener una lista de todos los archivos CSV en los subdirectorios
csv_files = glob.glob(os.path.join(base_dir, '*/merged_output.csv'))
csv_files.sort() #order data 

# Lista para almacenar los DataFrames de cada archivo
data_frames = []

# Procesar cada archivo CSV
for file_path in csv_files:
    # Extraer el nombre del directorio del sujeto (por ejemplo, '01', '02', etc.)
    subject_id = os.path.basename(os.path.dirname(file_path))
    
    # Leer el archivo CSV
    df = pd.read_csv(file_path)
    
    # Agregar una columna para el identificador del sujeto
    df['Subject'] = subject_id
    
    # Agregar el DataFrame a la lista
    data_frames.append(df)

# Concatenar todos los DataFrames en uno solo
combined_df = pd.concat(data_frames, ignore_index=True)

# Guardar el DataFrame combinado en un nuevo archivo CSV
combined_df.to_csv('combined_eeg_data.csv', index=False)

print("Archivos fusionados y guardados en 'combined_eeg_data.csv'")
