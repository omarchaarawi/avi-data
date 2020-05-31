import requests
import lxml.html as lh
from helpers import string_to_datetime, find_dates
import time

x = 0
url = 'https://avalanche.state.co.us/caic/pub_bc_avo.php?zone_id=' + str(x)

response = requests.get(url)
tree = lh.document_fromstring(response.content)
avi_problem_type = tree.xpath("//div[@id='avalanche-forecast']/div[3]/div[1]/div[2]/a/text()")[0]
foo = tree.xpath("//*[@id='avalanche-forecast']/div[3]/div[1]/div[2]/a/text()")[0]
bar = tree.xpath("//div[@id='avalanche-forecast']/div[4]/div[2]/div[2]/a/text()")[0]
baz = tree.xpath("//div[@id='avalanche-forecast']/div[5]/div[2]/div[2]/a/text()")[0]
print(foo, bar, baz)


tree = lh.document_fromstring(response.content)
value_script = tree.xpath("//div[@id='avalanche-forecast']/div[8]/ul/li[1]/script/text()")