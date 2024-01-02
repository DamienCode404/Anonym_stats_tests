import tkinter as tk
from tkinter import filedialog
import customtkinter

from DataProcessor import DataProcessor
from AnalysisGenerator import AnalysisGenerator
from StatsTester import StatisticsTester


class ConfigGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Personnalisation de l'apparence
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        # Création de la fenêtre principale
        self.geometry("1200x800")  # Définition de la taille de la fenêtre
        self.title("Configuration du calcul")

        # Création d'un cadre dans la fenêtre
        frame = customtkinter.CTkFrame(master=self)
        frame.pack(pady=20, padx=60, fill="both",
                   expand=True)  # Placement du cadre

        # Création d'un titre dans la fenêtre
        label = customtkinter.CTkLabel(
            master=frame, text="Sélection des répertoires et paramètres", font=("Roboto", 24))
        label.pack(pady=30, padx=10)

        # Dossier patients réels
        dossier_non_anonyme_frame = customtkinter.CTkFrame(master=frame)
        dossier_non_anonyme_frame.pack(pady=5)
        customtkinter.CTkLabel(
            master=dossier_non_anonyme_frame, text="Dossier patients réels:", font=("Roboto", 18)).pack(side="left")
        self.dossier_non_anonyme_entry = customtkinter.CTkEntry(
            master=dossier_non_anonyme_frame, width=500)
        self.dossier_non_anonyme_entry.pack(side="left", padx=10)
        customtkinter.CTkButton(
            master=dossier_non_anonyme_frame, text="Parcourir", command=self.browse_non_anonymous_folder).pack(side="left", pady=10)

        # Dossier patients anonymes
        dossier_anonyme_frame = customtkinter.CTkFrame(master=frame)
        dossier_anonyme_frame.pack(pady=5)
        customtkinter.CTkLabel(
            master=dossier_anonyme_frame, text="Dossier patients anonymes:", font=("Roboto", 18)).pack(side="left")
        self.dossier_anonyme_entry = customtkinter.CTkEntry(
            master=dossier_anonyme_frame, width=500)
        self.dossier_anonyme_entry.pack(side="left", pady=5, padx=10)
        customtkinter.CTkButton(
            master=dossier_anonyme_frame, text="Parcourir", command=self.browse_anonymous_folder).pack(side="left", pady=10)

        # Dossier de sorties
        output_folder_frame = customtkinter.CTkFrame(master=frame)
        output_folder_frame.pack(pady=5)
        customtkinter.CTkLabel(
            master=output_folder_frame, text="Dossier de sorties:", font=("Roboto", 18)).pack(side="left")
        self.output_folder_entry = customtkinter.CTkEntry(
            master=output_folder_frame, width=500)
        self.output_folder_entry.pack(side="left", pady=5, padx=10)
        customtkinter.CTkButton(
            master=output_folder_frame, text="Parcourir", command=self.browse_output_folder).pack(side="left", pady=10)

        customtkinter.CTkLabel(
            master=frame, text="Taille échantillon patients réels pour calcul des distances:", font=("Roboto", 18)).pack(pady=(30, 5))
        # Label pour afficher la valeur du slider
        self.slider_value_label_1 = customtkinter.CTkLabel(
            master=frame, text="10", font=("Roboto", 18))
        self.slider_value_label_1.pack(pady=1)

        def slider_event(value):
            # Mettez à jour le label avec la valeur du curseur
            int_value = int(value)
            self.slider_value_label_1.configure(text=str(int_value))
            return int_value

        # Créer un slider pour sélectionner le nombre de patients
        self.num_samples_entry = customtkinter.CTkSlider(
            master=frame, from_=1, to=20, command=slider_event)
        self.num_samples_entry.pack(pady=10)

        customtkinter.CTkLabel(
            master=frame, text="Nombre total de patients anonymes:", font=("Roboto", 18)).pack(pady=5)

        # Label pour afficher la valeur du slider
        self.slider_value_label_2 = customtkinter.CTkLabel(
            master=frame, text="500", font=("Roboto", 18))
        self.slider_value_label_2.pack(pady=1)

        def slider_event(value):
            # Mettez à jour le label avec la valeur du curseur
            int_value = int(value)
            self.slider_value_label_2.configure(text=str(int_value))
            return int_value

        # Créer un slider pour sélectionner le nombre de patients
        self.num_anonymous_patients_entry = customtkinter.CTkSlider(
            master=frame, from_=1, to=1000, command=slider_event)
        self.num_anonymous_patients_entry.pack(pady=10)

        # Bouton pour soumettre la configuration
        customtkinter.CTkButton(master=frame, text="Calculer", font=("Roboto", 20), hover_color="green", border_spacing=10,
                                command=self.submit_config).pack(pady=20)

        self.mainloop()

    def browse_non_anonymous_folder(self):
        folder_path = filedialog.askdirectory()
        self.dossier_non_anonyme_entry.delete(0, tk.END)
        self.dossier_non_anonyme_entry.insert(0, folder_path)

    def browse_anonymous_folder(self):
        folder_path = filedialog.askdirectory()
        self.dossier_anonyme_entry.delete(0, tk.END)
        self.dossier_anonyme_entry.insert(0, folder_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_entry.delete(0, tk.END)
        self.output_folder_entry.insert(0, folder_path)

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


def main(dossier_non_anonyme, dossier_anonyme, output_folder, num_samples, num_anonymous_patients):
    # Créez une instance de DataProcessor
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
    # Lancez l'interface graphique de configuration
    config_gui = ConfigGUI()
    config_gui.mainloop()
