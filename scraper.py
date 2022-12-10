import requests
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import uuid
from utils import * 

from markdownify import MarkdownConverter

def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)

#A Scraper for the Search Mode
def search_scraper(query="", page=0):
	query = "%20".join(query.split(" "))
	#print("SCRAPERACTIVATED________searching... ",query, "page-_>", page)
	f_page = requests.get("https://www.sardegnadigitallibrary.it/index.php?xsl=2435&ric=2&c1="+query+"&c=4459&ti=")
	fsoup = BeautifulSoup(f_page.content, "html.parser")
	n_results = fsoup.find("span", class_="badge bg-primary disabled")
	base_url = "https://www.sardegnadigitallibrary.it"
	#print(f"n_ results{n_results.text}") 
	#print("page size-->",100)
	try :
		n_pages = int((int(n_results.text)/100))+1
	except :
		m_toast("Nessun Risultato !")
		return [], 0
	#print("num pages-->", n_pages)
	res_list = []
	paging_url = "https://www.sardegnadigitallibrary.it/index.php?xsl=2451&tipo=0&o=1&c1="+query+"&n=100&p="+str(page)
	page = requests.get(paging_url)
	soup = BeautifulSoup(page.content, "html.parser")


	result_container = soup.find_all("div", class_="col-md-3 col-sm-6 col-xs-12 tmargin")

	for res in result_container:
		res_o = {}
		cat = res.find("span", class_="text-primary")
		link = res.find("a", class_="img-wrapper")
		#print("link-->",link["href"])
		#print("cat-->",cat.text)
		img = res.find("img",class_="img-responsive")
		#print("img-->",img["src"])
		#print("title-->",img["title"])
		res_o["link"]=sanitize_url(link["href"])
		res_o["img"]= sanitize_url(img["src"]) #base_url +img["src"] if img["src"].startswith("/") else sanitize_url(img["src"])
		res_o["title"]=img["title"]#.replace("\"","\'") #.replace("\'","\`" )
		res_o["cat"]=cat.text
		res_o["uid"]= str(abs(hash( res_o["link"]+res_o["title"]))) #uuid.uuid1().__str__()
		res_o["preferito"]= False
		res_list.append(res_o)
	#print("res_list len->",len(res_list))
	return res_list, n_pages



#A Scraper for Browsing the site
def browse_scraper():
	pass


#A Scraper for a single resource
def res_scraper(res_type,url):
	res_o = {}
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	if res_type== "IMMAGINI":
		par = soup.find_all("ul", class_="dropdown-menu")
		par1 = par[0].find_all("a")
		res_o["url"] = par1[-1]["href"]
		desc = soup.find("div", {"class":"row clear-fix"})
		res_o["desc"] = md(desc,strip=['a'])
		return res_o

	elif res_type == "VIDEO":
		v_el =soup.find("video", {"id": "video"})
		s_el = v_el.find("source")
		desc = soup.find("div", {"class":"row clear-fix"})
		res_o["desc"] = md(desc,strip=['a'])
		res_o["poster"] = v_el["poster"]
		res_o["url"] = s_el["src"]
		return res_o

	elif res_type == "AUDIO":
		a_el =soup.find("a", {"title": "versione mp3"})
		desc = soup.find("div", {"class":"row clear-fix"})
		res_o["desc"] = md(desc,strip=['a'])
		res_o["url"] = a_el["href"]
		return res_o
	elif res_type == "TESTI":
		t_el =soup.find("a", {"class": "titlet r-space"})["href"]
		desc = soup.find("div", {"class":"row clear-fix"})
		res_o["url"] = t_el
		res_o["desc"] =md(desc,strip=['a'])
		return res_o
	


	#print(res_o)

#res_scraper("TESTI", "https://www.sardegnadigitallibrary.it/index.php?xsl=2436&s=17&v=9&c=4463&id=205666")


