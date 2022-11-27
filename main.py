from kivy.lang import Builder
from kivy.core.window import Window
from kivy import platform
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.uix.recycleview import RecycleView
from kivy.storage.jsonstore import JsonStore
import webbrowser
from kivymd.uix.behaviors import TouchBehavior

from kivy.uix.image import AsyncImage
from scraper import *

#Neened by the Digital Library site..
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

if platform == "linux":
    Window.size = (450, 740)

def sanitize_url(url):
    if 'amp;' in url :
        url = url.replace("amp;","")
    while url.startswith("/"):
        url = url[1:]
    if url.startswith("www"):
        url = "https://"+url
    return url

# The main kv file is loaded indipendently because of naming rules [ call it like your App class instance less the final "App" eg: NavigationApp--> navigation.kv]
Builder.load_file("browse.kv")
Builder.load_file("search.kv")
Builder.load_file("image.kv")

store = JsonStore('db.json')
l = search_scraper(query="formaggio")

#j = json.dumps(l)
store.store_put("db",l)



store.store_sync()


class MainScreen(MDScreen):
    pass
class SDLCard(MDCard):
    link = StringProperty()
    img = StringProperty()
    title = StringProperty()
    cat = StringProperty()
    uid = StringProperty()

    def openlink(self, url):
        url = sanitize_url(url)
        webbrowser.open(url)



# Define the Recycleview class which is created in .kv file
class RecycleViewer(RecycleView):
    def __init__(self, **kwargs):
        super(RecycleViewer, self).__init__(**kwargs)
        self.data = store["db"]

class ImageScreen(MDScreen):
    res_link = StringProperty()
class IMG(AsyncImage,TouchBehavior):
    def on_double_tap(self, *args):
            print("<on_double_tap>", args)
            #app.play(root)

class SDLApp(MDApp):
    def __init__(self, **kwargs):
        super(SDLApp, self).__init__(**kwargs)
        self.res_link = ""
        self.previous = "bro_screen"


    def build(self):
        #self.theme_cls.theme_style = "Dark"
        return MainScreen()
    def go_back(self):
        print("goback ", self.previous)
        self.root.ids.screen_manager.current = self.previous

    def play(self, root):
        if root.cat =="IMMAGINI":
            print("immagini")
            s_url = sanitize_url(root.link)
            res_o = res_scraper("IMMAGINI",s_url)
            self.root.ids.img_screen.ids.image.source = res_o["url"] 
            #print("res_o-->",res_o["url"])
            self.previous = "bro_screen"
            print("SCreens-->",self.root.ids.screen_manager.screens)
            self.root.ids.screen_manager.current = "img_screen" 

        elif root.cat == "VIDEO":
            print("Video")
                
        else:
            print("default")
                


SDLApp().run()