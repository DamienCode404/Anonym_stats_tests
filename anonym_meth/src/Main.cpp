// Main.cpp
#include "Anonymization.h"
#include <iostream>

using namespace std;

int main(int argc, char** argv) {
    if (argc != 4) {
        cerr << "Il faut 3 arguments : " << argv[0] << " <dossierEntree> <dossierSortie> <dossierAnonyme>" << endl;
        return 1;
    }

    const string inputFolder = "./" + string(argv[1]) + "/";
    const string outputFolder = "./" + string(argv[2]) + "/";
    const string anonymizedFolder = "./" + string(argv[3]) + "/";

    processFiles(inputFolder, outputFolder, anonymizedFolder);

    return 0;
}