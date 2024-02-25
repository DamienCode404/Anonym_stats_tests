import tkinter as tk
from tkinter import filedialog
import customtkinter

from DataProcessor import DataProcessor
from AnalysisGenerator import AnalysisGenerator
from StatsTester import StatisticsTester

###########################################################################################
### Class: ConfigGUI                                                                    ###
### Description: This class represents a graphical user interface (GUI) for configuring ###
### parameters related to the calculation process. It provides options to select        ###
### directories for real patients, anonymous patients, and the output folder.           ###
### Additionally, the user can specify the number of real patients and anonymous        ###
### patients for the calculation. The configuration can be submitted using the          ###
### "Calculate" button.                                                                 ###
###########################################################################################

class ConfigGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Customizing the appearance
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        # Creating the main window
        self.geometry("1200x800")  # Defining the window size
        self.title("Configuration Calculation")

        # Creating a frame within the window
        frame = customtkinter.CTkFrame(master=self)
        frame.pack(pady=20, padx=60, fill="both",
                   expand=True)  # Placing the frame

        # Creating a title within the window
        label = customtkinter.CTkLabel(
            master=frame, text="Selecting directories and settings", font=("Roboto", 24))
        label.pack(pady=30, padx=10)

        # Real patients folder
        dossier_non_anonyme_frame = customtkinter.CTkFrame(master=frame)
        dossier_non_anonyme_frame.pack(pady=5)
        customtkinter.CTkLabel(
            master=dossier_non_anonyme_frame, text="Real patients folder:", font=("Roboto", 18)).pack(side="left")
        self.dossier_non_anonyme_entry = customtkinter.CTkEntry(
            master=dossier_non_anonyme_frame, width=500)
        self.dossier_non_anonyme_entry.pack(side="left", padx=10)
        customtkinter.CTkButton(
            master=dossier_non_anonyme_frame, text="Browse", command=self.browse_non_anonymous_folder).pack(side="left", pady=10)

        # Anonymous patients folder
        dossier_anonyme_frame = customtkinter.CTkFrame(master=frame)
        dossier_anonyme_frame.pack(pady=5)
        customtkinter.CTkLabel(
            master=dossier_anonyme_frame, text="Anonymised patients folder:", font=("Roboto", 18)).pack(side="left")
        self.dossier_anonyme_entry = customtkinter.CTkEntry(
            master=dossier_anonyme_frame, width=500)
        self.dossier_anonyme_entry.pack(side="left", pady=5, padx=10)
        customtkinter.CTkButton(
            master=dossier_anonyme_frame, text="Browse", command=self.browse_anonymous_folder).pack(side="left", pady=10)

        # Output folder
        output_folder_frame = customtkinter.CTkFrame(master=frame)
        output_folder_frame.pack(pady=5)
        customtkinter.CTkLabel(
            master=output_folder_frame, text="Output folder:", font=("Roboto", 18)).pack(side="left")
        self.output_folder_entry = customtkinter.CTkEntry(
            master=output_folder_frame, width=500)
        self.output_folder_entry.pack(side="left", pady=5, padx=10)
        customtkinter.CTkButton(
            master=output_folder_frame, text="Browse", command=self.browse_output_folder).pack(side="left", pady=10)

        customtkinter.CTkLabel(
            master=frame, text="Number of real patients for calculating distances:", font=("Roboto", 18)).pack(pady=(30, 5))
        # Label to display the value of the slider
        self.slider_value_label_1 = customtkinter.CTkLabel(
            master=frame, text="10", font=("Roboto", 18))
        self.slider_value_label_1.pack(pady=1)

        def slider_event(value):
            # Update the label with the slider value
            int_value = int(value)
            self.slider_value_label_1.configure(text=str(int_value))
            return int_value

        # Create a slider to select the number of patients
        self.num_samples_entry = customtkinter.CTkSlider(
            master=frame, from_=1, to=20, command=slider_event)
        self.num_samples_entry.pack(pady=10)

        customtkinter.CTkLabel(
            master=frame, text="Number of anonymous patients:", font=("Roboto", 18)).pack(pady=5)

        # Label to display the value of the slider
        self.slider_value_label_2 = customtkinter.CTkLabel(
            master=frame, text="500", font=("Roboto", 18))
        self.slider_value_label_2.pack(pady=1)

        #########################################
        
        def slider_event(value):
            # Update the label with the slider value
            int_value = int(value)
            self.slider_value_label_2.configure(text=str(int_value))
            return int_value

        # Create a slider to select the number of patients
        self.num_anonymous_patients_entry = customtkinter.CTkSlider(
            master=frame, from_=1, to=1000, command=slider_event)
        self.num_anonymous_patients_entry.pack(pady=10)

        # Button to submit the configuration
        customtkinter.CTkButton(master=frame, text="Calculate", font=("Roboto", 20), hover_color="green", border_spacing=10,
                                command=self.submit_config).pack(pady=20)

        self.mainloop()

    #########################################
    
    def browse_non_anonymous_folder(self):
        folder_path = filedialog.askdirectory()
        self.dossier_non_anonyme_entry.delete(0, tk.END)
        self.dossier_non_anonyme_entry.insert(0, folder_path)
    
    #########################################
    
    def browse_anonymous_folder(self):
        folder_path = filedialog.askdirectory()
        self.dossier_anonyme_entry.delete(0, tk.END)
        self.dossier_anonyme_entry.insert(0, folder_path)

    #########################################
        
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_entry.delete(0, tk.END)
        self.output_folder_entry.insert(0, folder_path)

    #########################################
    
    def submit_config(self):
        # Get values from entry widgets
        dossier_non_anonyme = self.dossier_non_anonyme_entry.get()
        dossier_anonyme = self.dossier_anonyme_entry.get()
        output_folder = self.output_folder_entry.get()
        num_samples = int(self.num_samples_entry.get())
        num_anonymous_patients = int(self.num_anonymous_patients_entry.get())

        # Close the configuration window
        self.destroy()

        # Call the main function with the obtained parameters
        main(dossier_non_anonyme, dossier_anonyme,
             output_folder, num_samples, num_anonymous_patients)

###########################################################################################
### Function: main                                                                      ###
### Description: This function serves as the main entry point for the calculation       ###
### process. It takes input parameters obtained from user input through the graphical   ###
### user interface. It initializes instances of DataProcessor and AnalysisGenerator     ###
### classes, performs dynamic time warping (DTW) analysis, generates physiological      ###
### statistics, and executes statistical tests.                                         ###
###                                                                                     ###
### Parameters (obtained from user input):                                              ###
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

    # Generate analyses
    analysis_generator = AnalysisGenerator(output_folder, data_processor)
    analysis_generator.generate_dtw_analysis()
    analysis_generator.generate_physio_stats()

    # Create an instance of StatisticsTester
    statistics_tester = StatisticsTester(output_folder, data_processor)
    
    # Generate statistics
    statistics_tester.generate_statistical_tests()

if __name__ == "__main__":
    # Launch the configuration GUI
    config_gui = ConfigGUI()
    config_gui.mainloop()
