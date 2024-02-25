import os
import pandas as pd

###########################################################################################
### Class: DataProcessor                                                                ###
### Description: This class is responsible for processing and loading physiological     ###
### data from both anonymous and non-anonymous patients. It includes methods for        ###
### initializing the object and loading patient data.                                   ###
###                                                                                     ###
###########################################################################################

class DataProcessor:
    def __init__(self, dossier_non_anonyme, dossier_anonyme, num_anonymous_patients, num_samples):
        self.dossier_non_anonyme = dossier_non_anonyme
        self.dossier_anonyme = dossier_anonyme
        self.num_anonymous_patients = num_anonymous_patients
        self.num_samples = num_samples
        self.param_physiologiques = ['FC', 'PAS', 'PAM', 'PAD']

    #########################################

    def load_patient_data(self, patient_id, is_anonymous=True):
        dossier = self.dossier_anonyme if is_anonymous else self.dossier_non_anonyme
        fichier = os.path.join(
            dossier, f"{patient_id}_anonyme.csv" if is_anonymous else f"{patient_id}_sorties.csv")

        if os.path.exists(fichier):
            return pd.read_csv(fichier).reset_index(drop=True)
        else:
            print(f"Warning: File not found for patient {patient_id}")
            return None

