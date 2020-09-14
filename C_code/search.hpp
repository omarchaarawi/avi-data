#pragma once 

#include <iostream>
#include <vector>
#include <string>

using namespace std;


// incident data type containing data about the incident
struct incident{  // incidents are stores as csv in the format: date, zone_id, activity, caught, buried, killed
    string date = "";
    int zone_id = -1;
    string activity = "";
    int caught = -1;
    int buried = -1;
    int killed = -1;
};

// each zone contains a vector of incidents
struct zone {
    vector<incident> incidents;
};

class Accidents {
    private: 
        vector<zone*> accidentList;

    public:
        void readCSV(string csvFile);
        void prettyPrint();
        void init_accidentList() {
            for(int i = 0; i < 10; i++) {
                accidentList[i] = NULL;
            }
        }
};