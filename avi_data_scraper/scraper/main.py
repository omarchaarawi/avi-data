import requests
import lxml.html as lh
from helpers import string_to_datetime, find_dates, danger_to_int
import time

# assign url
x = 0
url = 'https://avalanche.state.co.us/caic/pub_bc_avo.php?zone_id=' + str(x)

# get values for avi forecasts by day return values
response = requests.get(url)
tree = lh.document_fromstring(response.content)
value_script = tree.xpath("//div[@id='avalanche-forecast']/div[8]/ul/li[1]/script/text()")
values = find_dates(value_script)

# iterate over dates using nested loop year 2013 through 2020
years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

for year in years:
    for day in values[year]['values']:
        form_data = {
                '_qf__arc_form' : '',
                'arc_bc_avo_fx_sel[0]': year,
                'arc_bc_avo_fx_sel[1]': day,
        }

        response = requests.post(url, data=form_data)
        # if the request does not yield a 200 status code, wait 1 minute and try again
        # this should keep the server from getting overwhelmed
        while response.status_code != 200:
            time.sleep(60)
            response = requests.post(url, data=form_data)
        # GATHER DATA:
        tree = lh.document_fromstring(response.content)
        # date_time
        date_time = string_to_datetime(tree.xpath("//div[@id='avalanche-forecast']/table[1]/thead/tr/td[1]/h2/text()")[0])
        # avi_danger(above, near, and at below treeline) saved as list in that order
        danger_above = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[1]/td[3]/strong/text()")[0])
        danger_near = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[1]/td[5]/strong/text()")[0])
        danger_below = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[3]/td[3]/strong/text()")[0])
        avi_danger = [danger_above, danger_near, danger_below]


        data = str(date_time), avi_danger
        with open("test.txt", "a") as file:
            file.write(str(data) + "\n")