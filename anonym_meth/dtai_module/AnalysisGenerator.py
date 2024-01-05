import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from dtaidistance import dtw


class AnalysisGenerator:
    def __init__(self, output_folder, data_processor):
        self.output_folder = output_folder
        self.data_processor = data_processor

    def generate_dtw_analysis(self):
        min_dtwm_list = []

        for i in tqdm(range(1, self.data_processor.num_anonymous_patients + 1), desc="Generating DTW Analysis"):
            data_anonymous = self.data_processor.load_patient_data(
                i, is_anonymous=True)
            data_real = self.data_processor.load_patient_data(
                i, is_anonymous=False)

            if data_anonymous is not None and data_real is not None:
                dtw_univariate_list = []
                min_dtwm_temp = float('inf')

                for j in range(self.data_processor.num_samples):
                    patient_real = data_real.sample()

                    dtw_univariate = []
                    for feature in ['FC', 'PAS', 'PAM', 'PAD']:
                        if feature in data_anonymous.columns and feature in patient_real.columns:
                            if not data_anonymous[feature].empty and not patient_real[feature].empty:
                                dtw_univariate.append(self.calculate_dtw(
                                    data_anonymous[feature], patient_real[feature]))

                    dtw_m = np.mean(dtw_univariate)
                    dtw_univariate_list.append(dtw_m)

                    if dtw_m < min_dtwm_temp:
                        min_dtwm_temp = dtw_m

                min_dtwm_list.append(min_dtwm_temp)

        if min_dtwm_list:
            E = np.mean(min_dtwm_list)
            S = np.std(min_dtwm_list)

            min_dtwm_normalized = [(dtw_m - E) / S for dtw_m in min_dtwm_list]

            # Arrondir les valeurs à deux chiffres après la virgule
            min_dtwm_normalized = [round(value, 2) for value in min_dtwm_normalized]

            self.save_to_csv('distri_dissim_norm_meth.csv', {
                            'dissim_norm': min_dtwm_normalized})
            self.generate_boxplot('boxplot_meth.png', min_dtwm_normalized)


    def calculate_dtw(self, series1, series2):
        return dtw.distance_fast(np.asarray(series1), np.asarray(series2))

    def generate_physio_stats(self):
        physio_parameters = ['FC', 'PAS', 'PAM', 'PAD']
        statistics = ['avg', 'std', 'med', 'min', 'max']

        for param_physio in physio_parameters:
            for stat in statistics:
                anonym_list, real_list = [], []

                for i in tqdm(range(1, self.data_processor.num_anonymous_patients + 1), desc=f"anonyme [{param_physio} - {stat}]"):                    
                    data_anonymous = self.data_processor.load_patient_data(i, is_anonymous=True)
                    if data_anonymous is not None:
                        anonym_list.append(self.calculate_statistic(
                            data_anonymous[param_physio], stat))

                for i in tqdm(range(1, self.data_processor.num_anonymous_patients + 1), desc=f"real [{param_physio} - {stat}]"):
                    data_real = self.data_processor.load_patient_data(i, is_anonymous=False)
                    if data_real is not None:
                        # Assurez-vous que les données réelles ne sont pas vides
                        if not data_real[param_physio].empty:
                            real_list.append(self.calculate_statistic(
                                data_real[param_physio], stat))
                        else:
                            print(f"Warning: Data for {param_physio} and {stat} is empty for patient {i}")

                df = pd.DataFrame({f"{stat}_anonym": anonym_list,
                                f"{stat}_real": real_list})

                output_file = f"stats/{stat}_values_meth_{param_physio}.csv"
                self.save_to_csv(output_file, df)

                # Comparaison et sauvegarde du graphique
                plt.figure(figsize=(10, 6))
                plt.plot(df[f"{stat}_anonym"], label='Anonyme', marker='o')
                plt.plot(df[f"{stat}_real"], label='Réel', marker='o')
                plt.title(f'Comparaison des valeurs {stat} pour {param_physio}')
                plt.xlabel('Patients')
                plt.ylabel(f'Valeurs {stat}')
                plt.legend()
                plt.grid(True)

                graph_output_file = f"comparison_{param_physio}_{stat}.png"
                graph_output_path = os.path.join(self.output_folder, "graphs", graph_output_file)
                os.makedirs(os.path.dirname(graph_output_path), exist_ok=True)
                plt.savefig(graph_output_path)
                plt.close()

    def calculate_statistic(self, data, stat):
        if stat == 'avg':
            return round(data.mean(), 2)
        elif stat == 'std':
            return round(data.std(), 2)
        elif stat == 'med':
            return round(data.median(), 2)
        elif stat == 'min':
            return round(data.min(), 2)
        elif stat == 'max':
            return round(data.max(), 2)

    def save_to_csv(self, filename, data):
        output_file = os.path.join(self.output_folder, filename)
        pd.DataFrame(data).to_csv(output_file, index=False)

    def generate_boxplot(self, filename, data):
        plt.figure(figsize=(8, 8))
        sns.boxplot(y=data, color='skyblue', width=0.3)
        plt.title('Distribution des distances normalisées', fontsize=16)
        plt.xlabel('Patients Anonymes', fontsize=14)
        plt.ylabel('DTWm_min Normalisée', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.savefig(os.path.join(self.output_folder,
                    filename), bbox_inches='tight')
        # plt.show() // Affichage du boxplot