// Anonymization.h
#ifndef ANONYMIZATION_H
#define ANONYMIZATION_H

#include <string>
#include <vector>
#include <iostream>

using namespace std;

struct SeriesData {
    int Time;
    double FC;
    double PAS;
    double PAM;
    double PAD;
};

struct EventsData {
    int Time;
    string Event;
};

void processFiles(const string& inputFolder, const string& outputFolder, const string& anonymizedFolder);

#endif // ANONYMIZATION_H
