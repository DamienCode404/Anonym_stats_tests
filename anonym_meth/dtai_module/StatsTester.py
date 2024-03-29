import os
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, wilcoxon

###########################################################################################
### Class: StatisticsTester                                                             ###
### Description: This class is responsible for performing statistical tests on the      ###
### physiological data obtained from both anonymous and real patients. It utilizes      ###
### methods to load data, save results to CSV files, and perform statistical tests      ###
### such as Kolmogorov-Smirnov and Wilcoxon rank-sum. The results are then saved in     ###
### CSV files for further analysis and comparison.                                      ###
###                                                                                     ###
###########################################################################################

class StatisticsTester:
    def __init__(self, output_folder, data_processor):
        self.output_folder = output_folder
        self.data_processor = data_processor

    #########################################
        
    """
    Load statistical data from CSV files for a specified physiological 
    parameter and statistic. If the file is not found, returns None.
    """
        
    def load_data(self, param_physio, stat, is_anonymous=True):
        filename = os.path.join(
            self.output_folder, f"stats/{stat}_values_meth_{param_physio}.csv")

        if os.path.exists(filename):
            return pd.read_csv(filename, sep=',').reset_index(drop=True)
        else:
            return None

    #########################################
    
    """
    Save data to a CSV file in the specified subdirectory within the output
    folder. Creates the subdirectory if it doesn't exist.
    """

    def save_to_csv(self, filename, data, subdirectory="tests"):
        output_file = os.path.join(self.output_folder, subdirectory, filename)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        pd.DataFrame(data).to_csv(output_file, index=False)

    #########################################
    
    """
    Perform statistical tests (KS and WMW) on the provided anonymous and real
    patient data. Returns the test statistics and p-values.
    """

    def perform_statistical_tests(self, data_anonymous, data_real):
        statKS, pvalKS = ks_2samp(data_anonymous, data_real)

        try:
            statWMW_p, pvalWMW_p = wilcoxon(
                data_anonymous, data_real, zero_method='pratt', alternative='two-sided')
        except ValueError:
            statWMW_p, pvalWMW_p = np.nan, np.nan

        statWMW_up, pvalWMW_up = wilcoxon(
            data_anonymous, data_real, zero_method='pratt', alternative='two-sided')

        diste_avg = np.sqrt(np.mean((np.mean(data_anonymous) - np.mean(data_real))**2))
        diste_std = np.sqrt(np.mean((np.std(data_anonymous) - np.std(data_real))**2))
        diste_med = np.sqrt(np.mean((np.median(data_anonymous) - np.median(data_real))**2))
        diste_min = np.sqrt(np.mean((np.min(data_anonymous) - np.min(data_real))**2))
        diste_max = np.sqrt(np.mean((np.max(data_anonymous) - np.max(data_real))**2))

        return statKS, pvalKS, statWMW_p, pvalWMW_p, statWMW_up, pvalWMW_up, diste_avg, diste_std, diste_med, diste_min, diste_max

    #########################################

    """
    Iterate over physiological parameters and statistics, load data, and
    perform statistical tests. Save the results in CSV files for comparison.
    """

    def generate_statistical_tests(self):
        statistics = ['avg', 'std', 'med', 'min', 'max']

        for param_physio in self.data_processor.param_physiologiques:
            for stat in statistics:
                data = self.load_data(param_physio, stat)
                anonym_list = data[f"{stat}_anonym"]
                real_list = data[f"{stat}_real"]

                if anonym_list is not None and real_list is not None:
                    resultats = self.perform_statistical_tests(
                        anonym_list, real_list)

                    output_data = pd.DataFrame({
                        'param_physio': [param_physio],
                        'statKS': [round(resultats[0], 2)],
                        'pvalKS': [round(resultats[1], 2)],
                        'statWMW_p': [round(resultats[2], 2)],
                        'pvalWMW_p': [round(resultats[3], 2)],
                        'statWMW_up': [round(resultats[4], 2)],
                        'pvalWMW_up': [round(resultats[5], 2)],
                        'diste_avg': [round(resultats[6], 2)],
                        'diste_std': [round(resultats[7], 2)],
                        'diste_med': [round(resultats[8], 2)],
                        'diste_min': [round(resultats[9], 2)],
                        'diste_max': [round(resultats[10], 2)],
                    })

                    output_file = f"tests_meth_{param_physio}_{stat}.csv"
                    self.save_to_csv(output_file, output_data)

