import re
from datetime import datetime
import requests
import lxml.html as lh

############################## string_to_datetime ##############################

#takes a string in format "day_of_week, month day, year at time meridiem" and return datetime format
def string_to_datetime(string):
    #strips newlines, tabs, and spaces
    string = re.sub('\s+',' ',string)
    #strips white space
    string = string.strip()
    string = string.split(",")
    #gets month, day, year
    month = string[1].split(' ')[1]
    day = string[1].split(' ')[2]
    year = string[2].split(" ")[1]

    #gets time and meridian
    # time = string[2].split(" ")[3]
    # meridiem = string[2].split(" ")[4]

    #join to form date string
    date = year + " " + month + " " + day
    #format into date_time object
    datetime_object = datetime.strptime(date, '%Y %b %d').date()

    return datetime_object

############################## find_dates ##############################

def find_dates(cdata_script_string):
    with open(".in_temp.txt", "w") as file:
        file.write(cdata_script_string[0])

    with open('.in_temp.txt') as infile, open('./.out_temp.txt', 'w') as outfile:
        copy = False
        for line in infile:
            if line.strip() == "_hs_options['arc_bc_avo_fx_sel'] = [":
                copy = True
                continue
            elif line.strip() == "];":
                copy = False
                continue
            elif copy:
                outfile.write(line)

    with open('./.out_temp.txt', 'r') as file:
        data = file.read()

    dict_values = eval(data)

    return dict_values

# Converts avi_danger to an integer corresponding with level of danger
# No Rating = 0, Low = 1, Moderate = 2, Considerable = 3, High = 4, Extreme = 5
def danger_to_int(danger):
    x = 0
    if danger == 'Low (1)':
        x = 1
    elif danger == 'Moderate (2)':
        x = 2
    elif danger == 'Considerable (3)':
        x = 3
    elif danger == 'High (4)':
        x = 4
    elif danger == 'Extreme (5)':
        x = 5
    
    return x

if __name__ == "__main__":
    main()



