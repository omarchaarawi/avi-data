import re
from datetime import datetime
import requests
import lxml.html as lh
from datetime import date
import time

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

# Assign url and specify zone_id
def getAviData(zone_id):
    date_of_pull = str(date.today())
    url = 'https://avalanche.state.co.us/caic/pub_bc_avo.php?zone_id=' + str(zone_id)
    csv_file = date_of_pull + "_zone_" + str(zone_id) +"_aviDanger" + ".csv"
    with open(csv_file, "a") as file:
        file.write("date, danger_below, danger_near, danger_above" + "\n")

    # This code retrieves all the report_ids that have been archived
    response = requests.get(url)
    tree = lh.document_fromstring(response.content)
    value_script = tree.xpath("//*[@id='avalanche-forecast']/div[5]/ul/li[1]/script/text()")
    reports = find_dates(value_script)

    # Iterate over dates using nested loop year 2013 through 2020
    # This can be adjusted if just looking for specific dates. The current data goes back to 2013 though
    # This code builds the requests we are going to post
    # I had to submit a request for each report so that I could load the page associated with the report and then
    # parse the html from each page
    years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

    for year in years:
        for day in reports[year]['values']:
            form_data = {
                    '_qf__arc_form' : '',
                    'arc_bc_avo_fx_sel[0]': year,
                    'arc_bc_avo_fx_sel[1]': day,
            }

            response = requests.post(url, data=form_data)

            # Occasionally I would overload CAIC's server and get kicked off, so this bit of code 
            # gives their page a quick break if the page does not load

            # if the request does not yield a 200 status code, wait 1 minute and try again
            # this should keep the server from getting overwhelmed
            while response.status_code != 200:
                time.sleep(60)
                response = requests.post(url, data=form_data)

            # Sweet! So now we can get start parsing html
            # GATHER DATA:

            tree = lh.document_fromstring(response.content)

            # Here we snag the date and time of the reports and use a "string_to_datetime" helper function to get 
            # the data in a form that will be more useful later. I used a sql friendly format in case I wanted to 
            # save my data in a personal database
            date_time = string_to_datetime(tree.xpath("//div[@id='avalanche-forecast']/table[1]/thead/tr/td[1]/h2/text()")[0])

            # Snag the avi_danger rating
            # avi_danger(above, near, and at below treeline) saved as list in that order
            danger_above = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[1]/td[3]/strong/text()")[0])
            danger_near = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[1]/td[5]/strong/text()")[0])
            danger_below = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[3]/td[3]/strong/text()")[0])

            # save the data to a text file in the format ('2013-12-23 16:23:00', [3, 3, 2]) line by line
            with open(csv_file, "a") as file:
                file.write(str(date_time)+ "," + str(danger_below) + "," + str(danger_near) + "," + str(danger_above) + "\n")
                
                

if __name__ == "__main__":
    main()



