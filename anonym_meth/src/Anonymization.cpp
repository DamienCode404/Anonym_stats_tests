// Anonymization.cpp
#include "Anonymization.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <omp.h>

using namespace std;

void processFiles(const string& inputFolder, const string& outputFolder, const string& anonymizedFolder, const int numberPatient) {
    srand(time(0));

    #pragma omp parallel for
    for (int i = 1; i <= numberPatient; ++i) {
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

                sortiesCsv << data.Time << "," << data.FC << "," << data.PAS << "," << data.PAM << "," << data.PAD << "," << eventsValue << endl;
                anonymeCsv << data.Time << "," << data.FC * anonymization_variable << "," << data.PAS * anonymization_variable << "," << data.PAM * anonymization_variable << "," << data.PAD * anonymization_variable << "," << eventsValue << endl;
            }
        }

        seriesFile.close();
        eventsFile.close();
        sortiesCsv.close();
        anonymeCsv.close();
    }
}
