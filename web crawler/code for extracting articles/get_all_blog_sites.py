from bs4 import BeautifulSoup as BS
from requests import get
import pickle


url = get('http://en.wikipedia.org/wiki/List_of_blogs')
# print(url.status_code)
soup = BS(url.content, 'html.parser')

url_list = {}

# print(soup.prettify())

table = soup.find_all('table', 'wikitable')[0].tbody

for tr in table.find_all('tr'):
	td = tr.find('td')
	# print(td)
	# print(type(td))
	try:
		url_list[td.find('a').text] = 'http://en.wikipedia.org'+td.find('a').get('href')
	except Exception:
		pass


for item in url_list:
	sp = BS(get(url_list[item]).content, 'html.parser')

	try:
		tab = sp.find('table', 'infobox').tbody
		# print(tab)
		url_list[item] = tab.find('td', 'url').find('a').get('href')
		# print(s)
	except Exception:
		 pass

url_pickle = open('dict_of_blog_sites.pickle', 'wb')

pickle.dump(url_list, url_pickle)

url_pickle.close()
