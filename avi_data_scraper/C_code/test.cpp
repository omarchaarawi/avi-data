#include <iostream>
#include <string>
#include <fstream>
#include <vector>

using namespace std;

struct incident{  // incidents are stores as csv in the format: date, zone_id, activity, caught, buried, killed
    string date = "";
    int zone_id = -1;
    string activity = "";
    int caught = -1;
    int buried = -1;
    int killed = -1;
};

int main(){
    incident inc;
    string myString = "1";

     inc.zone_id = stoi(myString);

    cout << inc.zone_id << endl;
}

