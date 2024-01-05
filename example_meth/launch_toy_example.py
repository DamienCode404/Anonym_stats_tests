import subprocess
import sys

def main():
    if len(sys.argv) != 1:
        print("Il ne faut pas ajouter d'arguments (variables préremplis) : python3 launch_toy_example.py")
        sys.exit(1)

    input_folder = "./input/multivariate_example/"
    output_folder = "./input/CSV_output_example/"
    anonymized_folder = "./output/anonymized_example/"
    number_patient = 50

    # Exécuter l'exécutable généré
    executable_path = "../anonym_meth/exe/executable.exe"
    command = [executable_path, input_folder, output_folder, anonymized_folder, str(number_patient)]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Erreur lors de l'exécution de l'exécutable.")
        sys.exit(1)

    while True:
        # Demander à l'utilisateur s'il souhaite effectuer des tests stats
        run_stats_tests = input("Voulez-vous effectuer des tests stats ? (O/n): ").strip().upper()

        if run_stats_tests in ["O", "N"]:
            break
        else:
            print("Veuillez entrer une réponse valide.")

    if run_stats_tests == "O":
        # Lecture des paramètres depuis le fichier parametres.txt
        with open("parametres_example.txt", "r") as param_file:
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

        # Systeme via le fichier texte pour passer les paramètres
        no_interface_path = "../anonym_meth/dtai_module/NoInterface.py"
        execution_command = ["python3", no_interface_path, dossier_non_anonyme, dossier_anonyme, output_folder, str(num_samples), str(num_anonymous_patients)]

        try:
            subprocess.run(execution_command, check=True)
        except subprocess.CalledProcessError:
            print("Erreur lors de l'exécution des tests stats.")
            sys.exit(1)

    else:
        print("Arrêt du programme")


if __name__ == "__main__":
    main()