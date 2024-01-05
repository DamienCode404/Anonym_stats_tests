// Anonymization.cpp
#include "Anonymization.h"
#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <limits>
#include <random>
#include <omp.h>

#include "progressbar.hpp"

using namespace std;

void processFiles(const string& inputFolder, const string& outputFolder, const string& anonymizedFolder, const int numberPatient) {
    srand(time(0));

    int choix_anonymization_meth;
    bool boucle = true;

    while(boucle){
        cout << "Choisissez une méthode d'anonymisation :" << endl;
        cout << "1 = Valeur aléatoire différente pour chaque patient" << endl;
        cout << "2 = Valeur aléatoire unique pour tout les patients" << endl;
        cout << "Entrez votre méthode choisie : "; 
        cin >> choix_anonymization_meth;

        if (cin.fail() || (choix_anonymization_meth != 1 && choix_anonymization_meth != 2)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Veuillez entrer 1 ou 2" << endl;
        } else {
            boucle = false;
            break;
        }
    }

    progressbar bar(numberPatient);
    cout << "Creation de "<< numberPatient << " patients anonymes";
    bar.set_todo_char(" ");
    bar.set_done_char("█");
    bar.set_opening_bracket_char("|");
    bar.set_closing_bracket_char("|");

    // Initialisation de la deuxième méthode d'anonymisation
    // Création d'un objet random_device pour obtenir une source d'entropie matériellement aléatoire
    random_device rd;
    // Initialisation d'un générateur de nombres aléatoires avec la valeur du random_device
    default_random_engine generator(rd());
    // Définition d'une distribution uniforme de nombres réels entre -0.2 et 0.2
    uniform_real_distribution<double> distribution(-0.2, 0.2);

    switch(choix_anonymization_meth){
        case 1:
            #pragma omp parallel for
            for (int i = 1; i <= numberPatient; ++i) {
                #pragma omp critical
                bar.update();
                double anonymization_variable;
                if (rand() % 2 == 0) {
                    anonymization_variable = 1 + (-0.02 - (rand() % 81) * 0.001); 
                } else {
                    anonymization_variable = 1 + (0.02 + (rand() % 81) * 0.001); 
                }

                // Traitement des fichiers series.txt
                ifstream seriesFile(inputFolder + to_string(i) + "_series.txt");
                ifstream eventsFile(inputFolder + to_string(i) + "_events.txt");

                ofstream sortiesCsv(outputFolder + to_string(i) + "_sorties.csv"); 
                ofstream anonymeCsv(anonymizedFolder + to_string(i) + "_anonyme.csv"); 

                if (!seriesFile || !eventsFile || !sortiesCsv || !anonymeCsv) {
                    cerr << "Erreur lors de l'ouverture des fichiers." << endl;
                    exit(1);
                }

                sortiesCsv << "Time,FC,PAS,PAM,PAD,events" << endl;
                anonymeCsv << "Time,FC,PAS,PAM,PAD,events" << endl;

                string line;
                vector<SeriesData> seriesData;
                vector<EventsData> eventsData;
                int lineCount = 0;

                while (getline(eventsFile, line)) {
                    lineCount++;
                    if (lineCount >= 2) {
                        stringstream ss(line);
                        EventsData data;
                        ss >> data.Time;
                        ss.ignore(); 
                        getline(ss, data.Event);
                        eventsData.push_back(data);
                    }
                }

                lineCount = 0;

                while (getline(seriesFile, line)) {
                    lineCount++;
                    if (lineCount >= 3) {
                        stringstream ss(line);
                        SeriesData data;
                        char comma; 
                        ss >> data.Time >> comma >> data.FC >> comma >> data.PAS >> comma >> data.PAM >> comma >> data.PAD;

                        string eventsValue = "NULL"; 
                        for (const auto& event : eventsData) {
                            if (event.Time == data.Time) {
                                eventsValue = event.Event;
                                break; 
                            }
                        }
                        // fixed format sera en notation décimale fixe
                        // setprecision(2) limite le nombre de chiffres après la virgule à deux
                        sortiesCsv << fixed << setprecision(2) << data.Time << "," << data.FC << "," << data.PAS << "," << data.PAM << "," << data.PAD << "," << eventsValue << endl;
                        anonymeCsv << fixed << setprecision(2) << data.Time << "," << data.FC * anonymization_variable << "," << data.PAS * anonymization_variable << "," << data.PAM * anonymization_variable << "," << data.PAD * anonymization_variable << "," << eventsValue << endl;
                    }
                }

                seriesFile.close();
                eventsFile.close();
                sortiesCsv.close();
                anonymeCsv.close();
            }
            boucle = false;
            break;
            
        case 2:
            double random_modifier;
            random_modifier = 1.0 + distribution(generator);

            #pragma omp parallel for
            for (int i = 1; i <= numberPatient; ++i) {
                #pragma omp critical
                bar.update();

                // Traitement des fichiers series.txt
                ifstream seriesFile(inputFolder + to_string(i) + "_series.txt");
                ifstream eventsFile(inputFolder + to_string(i) + "_events.txt");

                ofstream sortiesCsv(outputFolder + to_string(i) + "_sorties.csv"); 
                ofstream anonymeCsv(anonymizedFolder + to_string(i) + "_anonyme.csv"); 

                if (!seriesFile || !eventsFile || !sortiesCsv || !anonymeCsv) {
                    cerr << "Erreur lors de l'ouverture des fichiers." << endl;
                    exit(1);
                }

                sortiesCsv << "Time,FC,PAS,PAM,PAD,events" << endl;
                anonymeCsv << "Time,FC,PAS,PAM,PAD,events" << endl;

                string line;
                vector<SeriesData> seriesData;
                vector<EventsData> eventsData;
                int lineCount = 0;

                while (getline(eventsFile, line)) {
                    lineCount++;
                    if (lineCount >= 2) {
                        stringstream ss(line);
                        EventsData data;
                        ss >> data.Time;
                        ss.ignore(); 
                        getline(ss, data.Event);
                        eventsData.push_back(data);
                    }
                }

                lineCount = 0;

                while (getline(seriesFile, line)) {
                    lineCount++;
                    if (lineCount >= 3) {
                        stringstream ss(line);
                        SeriesData data;
                        char comma; 
                        ss >> data.Time >> comma >> data.FC >> comma >> data.PAS >> comma >> data.PAM >> comma >> data.PAD;

                        string eventsValue = "NULL"; 
                        for (const auto& event : eventsData) {
                            if (event.Time == data.Time) {
                                eventsValue = event.Event;
                                break; 
                            }
                        }

                        sortiesCsv << fixed << setprecision(2) << data.Time << "," << data.FC << "," << data.PAS << "," << data.PAM << "," << data.PAD << "," << eventsValue << endl;
                        anonymeCsv << fixed << setprecision(2) << data.Time << "," << data.FC * random_modifier << "," << data.PAS * random_modifier << "," << data.PAM * random_modifier << "," << data.PAD * random_modifier << "," << eventsValue << endl;
                    }
                }

                seriesFile.close();
                eventsFile.close();
                sortiesCsv.close();
                anonymeCsv.close();
            }
            boucle = false;
            break;

        default:
            cout << "Veuillez entrer un nombre valide" << endl;
            break;
    }
    cout << endl;
}
