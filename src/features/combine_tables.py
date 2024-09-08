import pandas as pd

# Leer la tabla con información adicional de los electrodos
table_path  = '/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/external/autism_state.csv'
table_info_df = pd.read_csv(table_path)

combined_df = pd.read_csv('/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/combined_eeg_data.csv')

# Fusionar los DataFrames basados en la columna 'Electrode'
# on es el nombre de la columna que quiere agregarse al dato completo
combined_df = pd.merge(combined_df, table_info_df, on='Subject', how='left')

# Guardar el DataFrame combinado en un nuevo archivo CSV
combined_df.to_csv('/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/processed/data_to_analysis.csv', index=False)

print("Archivos fusionados y guardados en 'combined_eeg_data_with_electrode_info.csv'")