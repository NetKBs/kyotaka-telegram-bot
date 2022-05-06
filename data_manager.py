import urllib.request as request
from bs4 import BeautifulSoup

# BadConnection => Problems to connect
# NotData => Empty return
# BadHost => Invalid host provided from the app

def headers():
	""" To install headers to access to webpages"""
	opener = request.build_opener()
	opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
	request.install_opener(opener)	


def add(direct_link, host):
	"""To search and get the story to add"""
	headers()
		
	# Try to conenct
	try:
		html = request.urlopen(direct_link).read()
		soup = BeautifulSoup(html, "html.parser")
	except:
		return "BadConnection" 

	# get and return data
	# data : link, chapter, host
	if host == "manganato.com":
		panel_chapters = soup.find("div", class_="panel-story-chapter-list")
		current_chapter = panel_chapters.find("li", class_="a-h")
		chapter = current_chapter.a.text

		return {"link":direct_link, "chapter":chapter, "host":host}#

	elif host == "lectormanga.com":
		panel_chapters = soup.find("div", {"id" : "chapters"})
		direct_link = panel_chapters.find("a", class_="btn btn-default btn-sm")
		chapter = panel_chapters.find("h4", class_="mt-2 text-truncate").text

		return {"link":direct_link, "chapter":chapter, "host":host}

	else:
		return "BadHost"

def search(story_name, host):
	""" Search for stories results """
	url = ""

	# get the correct url for each host
	if host == "manganato.com":
		story_name = (story_name.strip()).replace(" ", "-") # replace spaces
		url = f"https://manganato.com/search/story/{story_name}"

	elif host == "lectormanga.com":
		story_name = (story_name.strip()).replace(" ", "+") # replace spaces
		url = f"https://lectormanga.com/library?title={story_name}&order_field=title&order_item=likes_count&order_dir=desc&type=&demography=&webcomic=&yonkoma=&amateur=&erotic=&genders%5B%5D=22"

	else: 
		return "BadHost"

	headers()
	# Try to conenct
	try:
		html = request.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")
	except:
		return "BadConnection"

	data = []
	stories = None

	if host =="manganato.com":
		stories = soup.find_all("div", class_="search-story-item")
	else: 
		stories = soup.find_all("div", class_="card-body p-0")

	# how many iterations to do
	count = len(stories)
	if count < 1:
		return "NotData"
	elif count > 4:
		 count = 4
	else:
		pass

	# Actually get the data
	if host == "manganato.com":
		for story in range(count):
			link = stories[story].find("a", class_="item-img")["href"]
			data.append(link)

	else:
		for story in range(count):
			link = stories[story].a["href"]
			data.append(link)

	return data  	

