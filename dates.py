import requests
import lxml.html as lh
from helpers import find_dates

url = 'https://avalanche.state.co.us/caic/pub_bc_avo.php?zone_id=1'

response = requests.get(url)
tree = lh.document_fromstring(response.content)
value_script = tree.xpath("//div[@id='avalanche-forecast']/div[8]/ul/li[1]/script/text()")

values = find_dates(value_script)

for x in range(len(values['2015']['values'])):
    print(values['2015']['values'][x], values['2015']['texts'][x])