import sys

from DataProcessor import DataProcessor
from AnalysisGenerator import AnalysisGenerator
from StatsTester import StatisticsTester

###########################################################################################
### Function: main                                                                      ###
### Description: This function serves as an alternative entry point for the calculation ###
### process when not using the graphical user interface. It takes input parameters      ###
### from the command line, initializes instances of DataProcessor and                   ###
### AnalysisGenerator classes, performs dynamic time warping (DTW) analysis,            ###
### generates physiological statistics, and executes statistical tests.                 ###
###                                                                                     ###
### Parameters (obtained from command line):                                            ###
###   - dossier_non_anonyme (str): The path to the folder containing data for real      ###
###     patients.                                                                       ###
###   - dossier_anonyme (str): The path to the folder containing data for anonymous     ###
###     patients.                                                                       ###
###   - output_folder (str): The path to the folder where the calculation results       ###
###     and analyses will be saved.                                                     ###
###   - num_samples (int): The number of real patients used for calculating distances.  ###
###   - num_anonymous_patients (int): The number of anonymous patients for the          ###
###     calculation.                                                                    ###
###                                                                                     ###
###########################################################################################

def main(dossier_non_anonyme, dossier_anonyme, output_folder, num_samples, num_anonymous_patients):
    # Create an instance of DataProcessor
    data_processor = DataProcessor(
        dossier_non_anonyme, dossier_anonyme, num_anonymous_patients, num_samples)
    
    # Create an instance of AnalysisGenerator
    analysis_generator = AnalysisGenerator(output_folder, data_processor)
    analysis_generator.generate_dtw_analysis()
    analysis_generator.generate_physio_stats()

    # Create an instance of StatisticsTester
    statistics_tester = StatisticsTester(output_folder, data_processor)
    statistics_tester.generate_statistical_tests()

if __name__ == "__main__":
    # Reads command-line parameters
    dossier_non_anonyme = sys.argv[1]
    dossier_anonyme = sys.argv[2]
    output_folder = sys.argv[3]
    num_samples = int(sys.argv[4])
    num_anonymous_patients = int(sys.argv[5])

    # Calls the main function with the provided inputs
    main(dossier_non_anonyme, dossier_anonyme, output_folder, num_samples, num_anonymous_patients)
