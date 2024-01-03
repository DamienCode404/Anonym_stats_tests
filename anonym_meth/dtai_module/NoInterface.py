import sys

from DataProcessor import DataProcessor
from AnalysisGenerator import AnalysisGenerator
from StatsTester import StatisticsTester

def main(dossier_non_anonyme, dossier_anonyme, output_folder, num_samples, num_anonymous_patients):
    # Utilisez les variables correctement
    data_processor = DataProcessor(
        dossier_non_anonyme, dossier_anonyme, num_anonymous_patients, num_samples)

    # Génération des analyses
    analysis_generator = AnalysisGenerator(output_folder, data_processor)
    analysis_generator.generate_dtw_analysis()
    analysis_generator.generate_physio_stats()

    # Créez une instance de StatisticsTester
    statistics_tester = StatisticsTester(output_folder, data_processor)
    
    # Génération des statistiques
    statistics_tester.generate_statistical_tests()

if __name__ == "__main__":
    # Lire les paramètres depuis la ligne de commande
    dossier_non_anonyme = sys.argv[1]
    dossier_anonyme = sys.argv[2]
    output_folder = sys.argv[3]
    num_samples = int(sys.argv[4])
    num_anonymous_patients = int(sys.argv[5])

    # Appel de la fonction main avec les paramètres
    main(dossier_non_anonyme, dossier_anonyme, output_folder, num_samples, num_anonymous_patients)
