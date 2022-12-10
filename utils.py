from kivy.clock import  mainthread
from kivymd.toast import toast



@mainthread
def m_toast(text):
    toast(text)



def sanitize_url(url):
    #print("before sani-_>",url)
    if 'amp;' in url :
        url = url.replace("amp;","")
    if url.startswith("/"):
        url = "https://www.sardegnadigitallibrary.it"+ url
    if url.startswith("//"):
        url = url[1:]
    if url.startswith("www"):
        url = "https://"+url
    if url.startswith("http://"):
        url = "https://"+url[7:] 
    if url.startswith("https://www.sardegnadigitallibrary.it//www.sardegnadigitallibrary.it"):
        url = "https://"+ url[39:]
    #print("sanitized-->",url)

    return url