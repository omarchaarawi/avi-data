#include <iostream>
#include "search.hpp"
#include <string>
#include <fstream>
#include <vector>
#include <sstream>

using namespace std;

void addIncidentHelper(incident inc, vector<zone*> accList);

void Accidents::readCSV(string csvFile){
    ifstream accidentsFile(csvFile);
    if(!accidentsFile.is_open()){
        cerr << "Could not open " << csvFile << endl;
        return;
    }
    else{
        string line, dataPoint;
        while(getline(accidentsFile, line)){
            stringstream x(line);
            int item = 0;
            string temp_array[6] = {"","","","","",""};
            while(getline(x, dataPoint, ',')){
                temp_array[item] = dataPoint;
                item++;
            }
            if(temp_array[1] != "zone_id") {   
                incident tempIncident;
                tempIncident.date = temp_array[0];
                tempIncident.zone_id = stoi(temp_array[1]);
                tempIncident.activity = temp_array[2];
                tempIncident.caught = stoi(temp_array[3]);
                tempIncident.buried = stoi(temp_array[4]);
                tempIncident.killed = stoi(temp_array[5]);    

                addIncidentHelper(tempIncident, accidentList);
            }
        }
    }
    accidentsFile.close();
}

void addIncidentHelper(incident inc, vector<zone*> accList) {
   zone* temp;
   temp->incidents.push_back(inc);
    int zoneID = inc.zone_id;
    accList[zoneID]->incidents.push_back(temp);
}

void Accidents::prettyPrint(){
    for(int i = 0; i < 10; i++){
        cout << "################# Zone " << i << " #################" << endl;
        for(int j = 0; j < accidentList[i]->incidents.size(); i++){
            cout << accidentList[i]->incidents[j].date
                << " " << accidentList[i]->incidents[j].zone_id
                << " " << accidentList[i]->incidents[j].activity
                << " " << accidentList[i]->incidents[j].caught
                << " " << accidentList[i]->incidents[j].buried
                << " " << accidentList[i]->incidents[j].killed << endl;
        }
    }
}

int main (int argc, char* argv[]){
    Accidents accident;
    accident.readCSV("accidents_.csv");
    accident.prettyPrint();
}

