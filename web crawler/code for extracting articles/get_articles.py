import pickle
import requests
from bs4 import BeautifulSoup as BS
import re


get_all_months_from_archive = lambda soup, tag, attrib: [cont.get(attrib) for cont in soup.find_all(tag)]

# def get_all_months_from_archive(soup, tag, attrib):
# 	archive_month_list = []
# 	for link in soup.find_all(tag).get(attrib):
# 		archive_month_list.append(link)
# 	return archive_month_list

blog_site_dict = pickle.load(open('dict_of_blog_sites.pickle', 'rb'))

for w in blog_site_dict.keys():
		url = blog_site_dict[w]
		try:
			url = url if url.endswith('/') else url+ '/'
			requests.head(url+'archives')
		except requests.exceptions.ConnectionError:
			print(url)


def get_all_articles_recursively(link):
	#code logic for getting articles
	print(link)
	soup = BS(requests.get(link).content, 'html.parser')
	link = soup.find('a', class_=re.compile('next'))
	if link:
		get_all_articles_recursively(link.get('href'))
	else:
		pass

def get_all_articles_iteratively(link):
	#to get links for articles...
	soup = BS(requests.get(link).content, 'html.parser')
	
	next_link = soup.find('a', class_=re.compile('next'))
	last_link = next_link.find_previous_sibling('a')
	
	href_string = str(last_link.get('href'))
	page_index = href_string.rfind('/')+1
	print(type(page_index))
	last_page_no = int(href_string[page_index:])
	print(last_page_no)
	href_prefix = href_string[:page_index]
	
	link_list = [link]
	for i in range(1, last_page_no+1):
		link_list.append(href_prefix+str(i))
	print(link_list)



url = 'https://www.3quarksdaily.com'
try:
	request = requests.get(url+'/archives')
	soup = BS(request.content, 'html.parser')
	for i, a in enumerate(soup.find_all('div')):
		# print(i)
		if a.has_attr('class') and 'month' in str(a['class']):
			archive_month_list = get_all_months_from_archive(a, 'a', 'href')
			# print(archive_month_list)
			get_all_articles_recursively(archive_month_list[3])
		else:
			pass


except requests.exceptions.ConnectionError:
	pass