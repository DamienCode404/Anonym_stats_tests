import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from dtaidistance import dtw

###########################################################################################
### Class: AnalysisGenerator                                                            ###
### Description: This class is designed for generating various analyses related to      ###
### physiological data. It includes methods for Dynamic Time Warping (DTW) analysis,    ###
### calculation of physiological statistics, and visualization of the results.          ###
###                                                                                     ###
###########################################################################################

class AnalysisGenerator:
    def __init__(self, output_folder, data_processor):
        # Initialize the AnalysisGenerator object with output folder and data processor
        self.output_folder = output_folder
        self.data_processor = data_processor
    
    #########################################
        
    def generate_dtw_analysis(self):
        # Initialize an empty list to store minimum DTW values
        min_dtwm_list = []

        # Iterate over each anonymous patient for DTW analysis
        for i in tqdm(range(1, self.data_processor.num_anonymous_patients + 1), desc="Generating DTW Analysis"):
            # Load anonymous and real patient data
            data_anonymous = self.data_processor.load_patient_data(i, is_anonymous=True)
            data_real = self.data_processor.load_patient_data(i, is_anonymous=False)

            # Check if data is available for both anonymous and real patients
            if data_anonymous is not None and data_real is not None:
                dtw_univariate_list = []
                min_dtwm_temp = float('inf')

                # Iterate over each sample for DTW calculation
                for j in range(self.data_processor.num_samples):
                    # Randomly select a real patient data sample
                    patient_real = data_real.sample()

                    dtw_univariate = []
                    # Calculate DTW for each physiological feature
                    for feature in ['FC', 'PAS', 'PAM', 'PAD']:
                        if feature in data_anonymous.columns and feature in patient_real.columns:
                            if not data_anonymous[feature].empty and not patient_real[feature].empty:
                                dtw_univariate.append(self.calculate_dtw(
                                    data_anonymous[feature], patient_real[feature]))

                    # Calculate mean DTW for the sample
                    dtw_m = np.mean(dtw_univariate)
                    dtw_univariate_list.append(dtw_m)

                    # Update minimum DTW if necessary
                    if dtw_m < min_dtwm_temp:
                        min_dtwm_temp = dtw_m

                # Append the minimum DTW for the patient to the list
                min_dtwm_list.append(min_dtwm_temp)

        # If minimum DTW values are obtained, proceed with analysis
        if min_dtwm_list:
            E = np.mean(min_dtwm_list)
            S = np.std(min_dtwm_list)

            # Normalize minimum DTW values
            min_dtwm_normalized = [(dtw_m - E) / S for dtw_m in min_dtwm_list]

            # Round the normalized values to two decimal places
            min_dtwm_normalized = [round(value, 2) for value in min_dtwm_normalized]

            # Save the normalized values to a CSV file
            self.save_to_csv('distri_dissim_norm_meth.csv', {
                            'dissim_norm': min_dtwm_normalized})
            # Generate and save a boxplot for the normalized values
            self.generate_boxplot('boxplot_meth.png', min_dtwm_normalized)

    #########################################
            
    def calculate_dtw(self, series1, series2):
        # Calculate Dynamic Time Warping (DTW) distance between two time series
        return dtw.distance_fast(np.asarray(series1), np.asarray(series2))
    
    #########################################

    def generate_physio_stats(self):
        # Define physiological parameters and statistics to be calculated
        physio_parameters = ['FC', 'PAS', 'PAM', 'PAD']
        statistics = ['avg', 'std', 'med', 'min', 'max']

        # Iterate over each physiological parameter and statistic for analysis
        for param_physio in physio_parameters:
            for stat in statistics:
                anonym_list, real_list = [], []

                # Iterate over each anonymous patient for statistical analysis
                for i in tqdm(range(1, self.data_processor.num_anonymous_patients + 1), desc=f"anonymised [{param_physio} - {stat}]"):                    
                    data_anonymous = self.data_processor.load_patient_data(i, is_anonymous=True)
                    if data_anonymous is not None:
                        # Calculate the specified statistic for the anonymous patient data
                        anonym_list.append(self.calculate_statistic(
                            data_anonymous[param_physio], stat))

                # Iterate over each real patient for statistical analysis
                for i in tqdm(range(1, self.data_processor.num_anonymous_patients + 1), desc=f"real [{param_physio} - {stat}]"):
                    data_real = self.data_processor.load_patient_data(i, is_anonymous=False)
                    if data_real is not None:
                        # Ensure that real patient data is not empty
                        if not data_real[param_physio].empty:
                            # Calculate the specified statistic for the real patient data
                            real_list.append(self.calculate_statistic(
                                data_real[param_physio], stat))
                        else:
                            print(f"Warning: Data for {param_physio} and {stat} is empty for patient {i}")

                # Create a DataFrame to store the statistical values
                df = pd.DataFrame({f"{stat}_anonym": anonym_list,
                                f"{stat}_real": real_list})

                # Define the output file path for the statistical values
                output_file = f"stats/{stat}_values_meth_{param_physio}.csv"
                # Save the statistical values to a CSV file
                self.save_to_csv(output_file, df)

                # Generate and save a comparison graph for the statistical values
                plt.figure(figsize=(10, 6))
                plt.plot(df[f"{stat}_anonym"], label='Anonymised', marker='o')
                plt.plot(df[f"{stat}_real"], label='Real', marker='o')
                plt.title(f'Comparing values {stat} for {param_physio}')
                plt.xlabel('Patients')
                plt.ylabel(f'Values {stat}')
                plt.legend()
                plt.grid(True)

                # Define the output file path for the comparison graph
                graph_output_file = f"comparison_{param_physio}_{stat}.png"
                graph_output_path = os.path.join(self.output_folder, "graphs", graph_output_file)
                os.makedirs(os.path.dirname(graph_output_path), exist_ok=True)
                # Save the comparison graph
                plt.savefig(graph_output_path)
                plt.close()

    #########################################
                
    def calculate_statistic(self, data, stat):
        # Calculate specified statistic for the given data
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

    #########################################
        
    def save_to_csv(self, filename, data):
        # Save data to a CSV file
        output_file = os.path.join(self.output_folder, filename)
        pd.DataFrame(data).to_csv(output_file, index=False)

    #########################################
    
    def generate_boxplot(self, filename, data):
        # Generate and save a boxplot for the given data
        plt.figure(figsize=(8, 8))
        sns.boxplot(y=data, color='skyblue', width=0.3)
        plt.title('Distribution of standardised distances', fontsize=16)
        plt.xlabel('Anonymised patients', fontsize=14)
        plt.ylabel('DTWm_min standardised', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.savefig(os.path.join(self.output_folder,
                    filename), bbox_inches='tight')
        # plt.show() // Display the boxplot