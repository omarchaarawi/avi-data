import requests
import lxml.html as lh
from helpers import string_to_datetime, find_dates
import time

def main():
    x = 0
    url = 'https://avalanche.state.co.us/caic/pub_bc_avo.php?zone_id=' + str(x)

    response = requests.get(url)
    tree = lh.document_fromstring(response.content)

    danger_above = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[1]/td[3]/strong/text()")[0])
    danger_near = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[1]/td[5]/strong/text()")[0])
    danger_below = danger_to_int(tree.xpath("//div[@id='avalanche-forecast']/table[1]/tbody/tr[3]/td[3]/strong/text()")[0])
    avi_danger = [danger_above, danger_near, danger_below]

    print(avi_danger)

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




