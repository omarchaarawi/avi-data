import re
from datetime import datetime, date
import requests
import lxml.html as lh
from helpers import getAviData
import time

# Iterate through all zones
for i in range(0,10):
    # Might as well time this to see how long each pull per zone takes
    start = int(time.time())
    
    # This is the work-horse that gets the data
    getAviData(i)
    
    finish = int(time.time())
    elapsed_time = (finish - start)/60
    print("zone {0} took {1:.2f} minutes".format(i, elapsed_time))
    with open(str(date.today())+"_time_to_collect_data.txt", "a") as file:
        file.write("zone {0} took {1:.2f} minutes\n".format(i, elapsed_time))
    
    # Sleep 5 minutes between pulls to give CAIC servers a break
    # I don't know if this helps...
    if(i != 9):
        time.sleep(300)