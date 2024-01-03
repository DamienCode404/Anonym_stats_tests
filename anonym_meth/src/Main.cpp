// Main.cpp
#include "Anonymization.h"
#include <iostream>

using namespace std;

int main(int argc, char** argv) {
    if (argc != 5) {
        cerr << "Il faut 4 arguments : " << argv[0] << " <dossierEntree> <dossierSortie> <dossierAnonyme> <nombrePatients>" << endl;
        return 1;
    }

    const string inputFolder = "./" + string(argv[1]) + "/";
    const string outputFolder = "./" + string(argv[2]) + "/";
    const string anonymizedFolder = "./" + string(argv[3]) + "/";
    const int numberPatient = atoi(argv[4]);

    processFiles(inputFolder, outputFolder, anonymizedFolder, numberPatient);

    return 0;
}