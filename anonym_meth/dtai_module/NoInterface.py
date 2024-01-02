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
    # Lire les paramètres depuis le fichier parametres.txt
    with open("parametres.txt", "r") as param_file:
        lines = param_file.readlines()

    # Assurez-vous qu'il y a suffisamment de lignes dans le fichier
    if len(lines) < 5:
        print("Le fichier de paramètres doit contenir au moins 5 lignes.")
        sys.exit(1)

    # Récupérez les paramètres à partir du fichier
    dossier_non_anonyme = lines[0].strip()
    dossier_anonyme = lines[1].strip()
    output_folder = lines[2].strip()
    num_samples = int(lines[3].strip())
    num_anonymous_patients = int(lines[4].strip())

    # Appelez la fonction main avec les paramètres
    main(dossier_non_anonyme, dossier_anonyme, output_folder, num_samples, num_anonymous_patients)
