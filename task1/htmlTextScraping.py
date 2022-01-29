import bs4
import codecs
from bs4 import BeautifulSoup

# read the html file
file = codecs.open('htmlTextScraping.html', 'r', 'utf-8')

# use beautifulsoup to structure initial data
soup = bs4.BeautifulSoup(file.read(), 'html.parser')
td_title = []
td_desc = []

# generate two lists - for week information and it's description
for table_data in soup.find_all('td'):
    if table_data['class'] == ['week']:
        td_title.append(table_data.get_text())
    else:
        td_desc.append(table_data.get_text())

# create a dictionary from the lists generated
schedule_dict = dict(zip(td_title, td_desc))

# print the dictionary as key value pairs
for key in schedule_dict:
    print(key, '\t', schedule_dict[key])
