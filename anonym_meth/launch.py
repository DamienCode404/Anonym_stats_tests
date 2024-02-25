import subprocess
import sys

###########################################################################################
### Function: main                                                                      ###
### Description: This function serves as the main entry point for the program.          ###
### It executes an external executable, prompts the user for further actions,           ###
### and initiates statistical tests by a graphical interface based on                   ###
### user input. Additionally, it can reads parameters from a parameters file or the     ###
### command line to configure the analysis process.                                     ###
###                                                                                     ###
###########################################################################################

def main():
    if len(sys.argv) != 5:
        print("You need 4 arguments: python3 launch.py <InputFolder> <OutputFolderReal> <OutputFolderAnonymised> <PatientsNumber>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    anonymized_folder = sys.argv[3]
    number_patient = sys.argv[4]

    # Execute the generated executable
    executable_path = "./exe/executable.exe"
    command = [executable_path, input_folder, output_folder, anonymized_folder, number_patient]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Error while executing the executable.")
        sys.exit(1)

    while True:
        # Ask the user if they want to perform stats tests
        run_stats_tests = input("Do you want to perform stats tests? (Y/n): ").strip().upper()

        if run_stats_tests in ["Y", "N"]:
            break
        else:
            print("Please enter a valid response.")

    if run_stats_tests == "Y":
        
        while True:
            # Ask the user if they want to use a graphical interface
            run_interface = input("Do you want to use a graphical interface? (Y/n): ").strip().upper()

            if run_interface in ["Y", "N"]:
                break
            else:
                print("Please enter a valid response.")
        
        if run_interface == "Y":
            # Graphical interface system to pass parameters
            stats_script_path = "./dtai_module/Main.py"
            stats_command = ["python3", stats_script_path]

            try:
                subprocess.run(stats_command, check=True)
            except subprocess.CalledProcessError:
                print("Error while executing stats tests.")
                sys.exit(1)

        elif run_interface == "N":
            # Read parameters from the parameters.txt file
            with open("parameters.txt", "r") as param_file:
                lines = param_file.readlines()

            # Ensure there are enough lines in the file
            if len(lines) < 5:
                print("The parameters file must contain at least 5 lines.")
                sys.exit(1)

            # Retrieve parameters from the file
            dossier_non_anonyme = lines[0].strip()
            dossier_anonyme = lines[1].strip()
            output_folder = lines[2].strip()
            num_samples = int(lines[3].strip())
            num_anonymous_patients = int(lines[4].strip())

            # System via the text file to pass parameters
            no_interface_path = "./dtai_module/NoInterface.py"
            execution_command = ["python3", no_interface_path, dossier_non_anonyme, dossier_anonyme, output_folder, str(num_samples), str(num_anonymous_patients)]

            try:
                subprocess.run(execution_command, check=True)
            except subprocess.CalledProcessError:
                print("Error while executing stats tests.")
                sys.exit(1)

    else:
        print("Program terminated")


if __name__ == "__main__":
    main()
