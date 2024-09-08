from mne import io
import mne
import numpy as np

from mne_connectivity import spectral_connectivity_epochs
from mne_connectivity.viz import plot_connectivity_circle

import matplotlib.pyplot as plt
import networkx as nx

for i in range(26,57):
    

    directory = "/home/ferna96/Documents/Proyectos/TMS_autism/Software/ML_model/autismdata/data/" 

    #from utils.preprocessing import convert_to_bipolar
    #read data
    raw = io.read_raw_eeglab(directory + 'raw/signaturesAutismDatabase/{}Abby_Resting.set'.format(i), preload= True)

    #filtrado

    #notch filtering to raw data - #detrend filtering - delete continuos component
    eeg_picks = mne.pick_types(raw.info, eeg=True)
    freqs = (50, 100, 150, 200)
    raw_filt = raw.copy().notch_filter(freqs=freqs, picks=eeg_picks)
    cutoff = 0.2
    raw_filt.filter(l_freq=cutoff, h_freq=None)

    #aplicar montaje referencial
    raw_avg = raw_filt.copy().set_eeg_reference(ref_channels='average')
    raw_avg.drop_channels(raw_avg.info['bads'])

    # Definir la frecuencia de muestreo y la duración del registro
    sfreq = raw_avg.info['sfreq']
    duration = raw_avg.times[-1]

    pre_name = raw_avg._filenames[0].split('/')[-1]
    name = pre_name.split('.')[0]
    
    raw_avg.plot()

    mne.export.export_raw(directory + 'interim/' + name + '.edf', raw_avg)


file_names = [
    '1Abby_Resting.edf',    
    '3Abby_Resting.edf',
    '4Abby_Resting.edf',
    '5Abby_Resting.edf',
    '6Abby_Resting.edf',    
    '8Abby_Resting.edf',
    '9Abby_Resting.edf',
    '12Abby_Resting.edf',        
    '13Abby_Resting.edf',
    '14Abby_Resting.edf',
    '15Abby_Resting.edf',
    '16Abby_Resting.edf',
    '17Abby_Resting.edf',
    '18Abby_Resting.edf',
    '19Abby_Resting.edf',
    '20Abby_Resting.edf',
    '21Abby_Resting.edf',    
    '24Abby_Resting.edf',
    '25Abby_Resting.edf',    
]