TEA pipeline
=========================


Este repositorio contiene el proyecto de análisis de señales EEG en autismo mediante Machine Learning. 

## Data 
Para  el diseño del pipeline y generación de pruebas preliminares se utilizó la base de datos linkeada con el articulo "Electrophysiological signatures of brain aging in autism spectrum disorder" [1]

## Procedimiento

En primer lugar los registros se convitieron de .fdt (EEGlab) a .edf. Luego, cada uno de los canales definidos de acuerdo al estandar 10-20 se convirtieron a montaje referencial. 

### Preprocesamiento

De cada registro se tomaron segmentos de 60 segundos de adquisición que fueron descompuestos en sus bandas frecuenciales utilizando Wavelet. El enfoque se explica con mas detalle en el trabajo de Flemning et al. [2]. 

### Obtención de caracteristicas
Para cada registro se obtienen caracteristicas no lineales de cada una de las banadas frecuenciales a lo largo de todos los canales.  
Para la obtención de estas métricas se utilizaron los paquetes [NOLDS](https://github.com/CSchoel/nolds/tree/main) y [EntroPy](https://github.com/raphaelvallat/entropy)
. En la siguiente tabla se muestran de manera resumida las métricas utilizadas. 

| **Variable no lineal**                         | **Acrónimo** | **Descripción**                                                                 | **Paquete** |
|------------------------------------------------|--------------|---------------------------------------------------------------------------------|-------------|
| Detrended fluctuation analysis                 | `DF`          | Long-range correlation of the physiological time series                         | NOLDS       |
| Sample entropy                                 | `Samp`        | Irregularity of physiological time series without self-matches                  | NOLDS       |
| Hurst exponent                                 | `Hurst`       | Long-term memory processes of a time series                                     | NOLDS       |
| Lyapunov exponent                              | `Lyap`        | Chaotic or periodic properties of a time series                                 | NOLDS       |
| Permutation entropy                            | `Perm`        | Information content of a given time series based on probability distribution    | EntroPy     |
| Spectral entropy                               | `Spec`        | Degree of skewness in the frequency distribution                                | EntroPy     |
| Singular value decomposition entropy           | `SVD`         | Dimensionality of a time series                                                 | EntroPy     |
| Approximate entropy                            | `App`         | Regularity of times series fluctuations                                         | EntroPy     |
| Higuchi fractal dimension                      | `HF`          | Self-similarity in time series using increasingly distanced samples in time     | EntroPy     |
| Katz fractal dimension                         | `KF`          | Complexity and self-similarity in time series using consecutive time points     | EntroPy     |


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------
## References 

1. Dickinson, A., Jeste, S., & Milne, E. (2022). Electrophysiological signatures of brain aging in autism spectrum disorder. Cortex, 148, 139-151.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
