import subprocess
import sys

###########################################################################################
### Function: main                                                                      ###
### Description: This function serves as the main entry point for the program.          ###
### It pre-fills variables, executes an external executable, prompts the user for       ###
### further actions, and initiates statistical tests or configuration based on user     ###
### input. Additionally, it reads parameters from a parameters file or the command      ###
### line to configure the analysis process.                                             ###
###                                                                                     ###
###########################################################################################

def main():
    if len(sys.argv) != 1:
        print("Do not add any arguments (pre-filled variables): python3 launch_toy_example.py")
        sys.exit(1)

    input_folder = "./input/multivariate_example/"
    output_folder = "./input/CSV_output_example/"
    anonymized_folder = "./output/anonymized_example/"
    number_patient = 50

    # Execute the generated executable
    executable_path = "../anonym_meth/exe/executable.exe"
    command = [executable_path, input_folder, output_folder, anonymized_folder, str(number_patient)]

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
        # Read parameters from the parameters.txt file
        with open("parameters_example.txt", "r") as param_file:
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
        no_interface_path = "../anonym_meth/dtai_module/NoInterface.py"
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