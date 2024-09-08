import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

path = '/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/processed/25/'

# Cargar el archivo CSV resultante
df = pd.read_csv(f"{path}merged_eeg_metrics.csv")
# Definir las métricas a graficar
# Definir las métricas a graficar
metrics = ['Hurst', 'DFA', 'Lyapunov', 'Sample Entropy', 'Correlation Dimension']

# Crear un diccionario para estilos de línea y marcadores
line_styles = ['-', '--', '-.', ':', '-']
markers = ['o', 's', 'D', '^', 'v']

# Crear el gráfico
plt.figure(figsize=(16, 10))

# Iterar sobre cada métrica y graficar
for i, metric in enumerate(metrics):
    sns.lineplot(data=df, x='Band', y=metric, hue='Electrode', style='Electrode', 
                 markers=markers[i], dashes=False, legend=False, linewidth=2)

# Añadir leyenda
plt.legend(title='Electrode', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.title("Distribuciones de los resultados diferenciados por canal y coeficiente wavelet")
plt.xlabel("Band")
plt.ylabel("Values")
plt.tight_layout()

# Mostrar el gráfico
plt.show()