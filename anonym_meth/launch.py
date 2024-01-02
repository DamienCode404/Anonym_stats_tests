import subprocess
import sys

def main():
    if len(sys.argv) != 4:
        print("Il faut 3 arguments : python3 launch.py <dossierEntree> <dossierSortie> <dossierAnonyme>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    anonymized_folder = sys.argv[3]

    # Exécuter l'exécutable généré
    executable_path = "./exe/executable.exe"
    command = [executable_path, input_folder, output_folder, anonymized_folder]

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
        print("Exécution des tests statistiques")

        while True:
            # Demander à l'utilisateur s'il souhaite passer par une interface graphique
            run_interface = input("Voulez-vous passer par une interface graphique ? (O/n): ").strip().upper()

            if run_interface in ["O", "N"]:
                break
            else:
                print("Veuillez entrer une réponse valide.")
        
        if run_interface == "O":
            # Systeme d'interface graphique pour passer les paramètres
            stats_script_path = "./dtai_module/Main.py"
            stats_command = ["python3", stats_script_path]

            try:
                subprocess.run(stats_command, check=True)
            except subprocess.CalledProcessError:
                print("Erreur lors de l'exécution des tests stats.")
                sys.exit(1)

        elif run_interface == "N":
            # Systeme via le fichier texte pour passer les paramètres
            no_interface_path = "./dtai_module/NoInterface.py"
            execution_command = ["python3", no_interface_path]

            try:
                subprocess.run(execution_command, check=True)
            except subprocess.CalledProcessError:
                print("Erreur lors de l'exécution des tests stats.")
                sys.exit(1)

    else:
        print("Arrêt du programme")


if __name__ == "__main__":
    main()