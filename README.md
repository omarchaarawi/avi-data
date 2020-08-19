# avi-data

##Note: The scraper is not currently working because CAIC modifies their webpages during the off-season. Currently trying to find a work-around.
small python project parsing avi data from CAIC

I have been trying to figure out a pattern leading up to accidents related to backcountry travel in Colorado. So far I have developed a scraper that can extract all the historical forecast data for the past seven years. The scraper works by parsing html from CAIC's forecast archives. It takes between 20 and 60 minutes depending on server speeds to build the data for each forecast zone. (There are 10 in Colorado) I have also gathered all the data on accidents in Colorado over the past seven years and am now trying to figure out how to draw a correspondance between the two data sets.
