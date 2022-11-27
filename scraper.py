import requests
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import uuid



#A Scraper for the Search Mode
def search_scraper(query=""):
	page_size = "100"
	#query = "nuraghe"
	page = "1"

	#f_page = requests.get("https://www.sardegnadigitallibrary.it/index.php?xsl=2435&ric=2&c1="+query+"&c=4459&ti=")
	#soup = BeautifulSoup(f_page.content, "html.parser")
	#n_results = soup.find("span", class_="badge bg-primary disabled")
	#print(n_results)
	base_url = "https://www.sardegnadigitallibrary.it"
	paging_url = "https://www.sardegnadigitallibrary.it/index.php?xsl=2451&tipo=0&o=1&c1="+query+"&n="+page_size+"&p="+page
	page = requests.get(paging_url)
	soup = BeautifulSoup(page.content, "html.parser")


	result_container = soup.find_all("div", class_="col-md-3 col-sm-6 col-xs-12 tmargin")
	print("result_container",result_container)
	#print(f"{len(result_container)}/{n_results.text}") 
	res_list = []
	
	for res in result_container:
		res_o = {}
		cat = res.find("span", class_="text-primary")
		link = res.find("a", class_="img-wrapper")
		print("link-->",link["href"])
		print("cat-->",cat.text)
		img = res.find("img",class_="img-responsive")
		print("img-->",img["src"])
		print("title-->",img["title"])
		res_o["link"]=link["href"]
		res_o["img"]=base_url +img["src"] if img["src"].startswith("/") else img["src"]
		res_o["title"]=img["title"]#.replace("\"","\'") #.replace("\'","\`" )
		res_o["cat"]=cat.text
		res_o["uid"]= uuid.uuid1().__str__()
		res_list.append(res_o)
	return res_list



#A Scraper for Browsing the site
def browse_scraper():
	pass


#A Scraper for a single resource
def res_scraper(res_type,url):
	res_o = {}

	if res_type== "IMMAGINI":
		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")
		par = soup.find_all("ul", class_="dropdown-menu")
		par1 = par[0].find_all("a")
		#print(par1)
		res_o["url"] = par1[-1]["href"]
		res_o["desc"] = soup.find("div",class_="row clear-fix").text
		return res_o
	#print(res_o)


#res_scraper("IMMAGINI", "https://www.sardegnadigitallibrary.it/index.php?xsl=2436&s=17&v=9&c=4461&id=174652")