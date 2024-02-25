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

// Function to process files and perform anonymization
void processFiles(const string& inputFolder, const string& outputFolder, const string& anonymizedFolder, const int numberPatient) {
    // Initialize random seed
    srand(time(0));

    // Variable for anonymization method choice
    int anonymization_method_choice;
    bool loop = true;

    // Loop until a valid choice is made
    while(loop){
        cout << "Choose an anonymization method :" << endl;
        cout << "1 = Random different value for each patient" << endl;
        cout << "2 = Random value, the same for all patients " << endl;
        cout << "Enter your method : "; 
        cin >> anonymization_method_choice;

        // Check if input is valid
        if (cin.fail() || (anonymization_method_choice != 1 && anonymization_method_choice != 2)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Please type 1 or 2" << endl;
        } else {
            loop = false;
            break;
        }
    }

    // Progress bar initialization
    progressbar bar(numberPatient);
    cout << "Creation of " << numberPatient << " anonymised patients";
    bar.set_todo_char(" ");
    bar.set_done_char("█");
    bar.set_opening_bracket_char("|");
    bar.set_closing_bracket_char("|");

    // Initialize the second anonymization method
    // Create a random device object to obtain a source of hardware entropy
    random_device rd;
    // Initialize a random number generator with the value of the random device
    default_random_engine generator(rd());
    // Define a uniform distribution of real numbers between -0.2 and 0.2
    uniform_real_distribution<double> distribution(-0.2, 0.2);

    // Switch statement for anonymization method choice
    switch(anonymization_method_choice){
        // Random different value for each patient
        case 1:
            // Parallel loop for each patient
            #pragma omp parallel for
            for (int i = 1; i <= numberPatient; ++i) {
                // Update progress bar
                #pragma omp critical
                bar.update();

                // Variable for anonymization
                double anonymization_variable;
                // Randomly choose whether to increase or decrease the value
                if (rand() % 2 == 0) {
                    anonymization_variable = 1 + (-0.02 - (rand() % 81) * 0.001); 
                } else {
                    anonymization_variable = 1 + (0.02 + (rand() % 81) * 0.001); 
                }

                // Process series.txt and events.txt files
                ifstream seriesFile(inputFolder + to_string(i) + "_series.txt");
                ifstream eventsFile(inputFolder + to_string(i) + "_events.txt");

                ofstream sortiesCsv(outputFolder + to_string(i) + "_sorties.csv"); 
                ofstream anonymeCsv(anonymizedFolder + to_string(i) + "_anonyme.csv"); 

                // Check if files are opened successfully
                if (!seriesFile || !eventsFile || !sortiesCsv || !anonymeCsv) {
                    cerr << "Error opening files." << endl;
                    exit(1);
                }

                // Write headers to output files
                sortiesCsv << "Time,FC,PAS,PAM,PAD,events" << endl;
                anonymeCsv << "Time,FC,PAS,PAM,PAD,events" << endl;

                // Read data from events file
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

                // Read data from series file and perform anonymization
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
                        // Write anonymized data to file
                        sortiesCsv << fixed << setprecision(2) << data.Time << "," << data.FC << "," << data.PAS << "," << data.PAM << "," << data.PAD << "," << eventsValue << endl;
                        anonymeCsv << fixed << setprecision(2) << data.Time << "," << data.FC * anonymization_variable << "," << data.PAS * anonymization_variable << "," << data.PAM * anonymization_variable << "," << data.PAD * anonymization_variable << "," << eventsValue << endl;
                    }
                }

                // Close files
                seriesFile.close();
                eventsFile.close();
                sortiesCsv.close();
                anonymeCsv.close();
            }
            loop = false;
            break;
            
        // Random value, the same for all patients
        case 2:
            // Modifier for randomization
            double random_modifier;
            random_modifier = 1.0 + distribution(generator);

            // Parallel loop for each patient
            #pragma omp parallel for
            for (int i = 1; i <= numberPatient; ++i) {
                // Update progress bar
                #pragma omp critical
                bar.update();

                // Process series.txt and events.txt files
                ifstream seriesFile(inputFolder + to_string(i) + "_series.txt");
                ifstream eventsFile(inputFolder + to_string(i) + "_events.txt");

                ofstream sortiesCsv(outputFolder + to_string(i) + "_sorties.csv"); 
                ofstream anonymeCsv(anonymizedFolder + to_string(i) + "_anonyme.csv"); 

                // Check if files are opened successfully
                if (!seriesFile || !eventsFile || !sortiesCsv || !anonymeCsv) {
                    cerr << "Error opening files." << endl;
                    exit(1);
                }

                // Write headers to output files
                sortiesCsv << "Time,FC,PAS,PAM,PAD,events" << endl;
                anonymeCsv << "Time,FC,PAS,PAM,PAD,events" << endl;

                // Read data from events file
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

                // Read data from series file and perform anonymization
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

                        // Write anonymized data to file
                        sortiesCsv << fixed << setprecision(2) << data.Time << "," << data.FC << "," << data.PAS << "," << data.PAM << "," << data.PAD << "," << eventsValue << endl;
                        anonymeCsv << fixed << setprecision(2) << data.Time << "," << data.FC * random_modifier << "," << data.PAS * random_modifier << "," << data.PAM * random_modifier << "," << data.PAD * random_modifier << "," << eventsValue << endl;
                    }
                }

                // Close files
                seriesFile.close();
                eventsFile.close();
                sortiesCsv.close();
                anonymeCsv.close();
            }
            loop = false;
            break;

        default:
            cout << "Please enter a valid number" << endl;
            break;
    }
    cout << endl;
}