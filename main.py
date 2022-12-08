import os
os.environ["KIVY_VIDEO"] = "ffpyplayer"
os.environ['KIVY_AUDIO'] = "ffpyplayer"

import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import dp
from kivy.uix.stencilview import StencilView
from kivymd.app import MDApp
from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton




import webbrowser
from scraper import *
from browse import *
from image import *
from utils import *
from audio import *





#Needed by the Digital Library site..
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

if kivy.platform == "linux":
    Window.size = (450, 740)
    #Window.size = (740,450)



# The main kv file is loaded indipendently because of naming rules [ call it like your App class instance less the final "App" eg: NavigationApp--> navigation.kv]
Builder.load_file("browse.kv")
Builder.load_file("preferiti.kv")
Builder.load_file("image.kv")
Builder.load_file("video.kv")
Builder.load_file("audio.kv")
Builder.load_file("texts.kv")

store = JsonStore('db.json')



class MainScreen(MDScreen):
    pass
class MyScreenManager(MDScreenManager):
    pass

class BoxStencil(MDBoxLayout, StencilView):
    pass

class MyButton(MDIconButton):
    link = StringProperty()



class SDLApp(MDApp):
    def __init__(self, **kwargs):
        super(SDLApp, self).__init__(**kwargs)
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_hue = "800"
        #print("themes ",dir(self.theme_cls))
        self.res_link = ""
        self.previous = "bro_screen"
        self.left_action_items = []
        self.right_action_items = []
        self.store = store
        self.last_tab = "Tutti"

    def build(self):

        return MainScreen()


    def openlink(self, url):
        url = sanitize_url(url)
        webbrowser.open(url)

    def reload_browser(self):
        print("reload")
        l = search_scraper(query="formaggio")

        store.store_put("db",l)
        store.store_sync()
        self.root.ids.bro_screen.children[0].data = store["db"]



        
    def go_back(self, *args):
        #print("goback ", self.previous)
        self.root.ids.screen_manager.current = self.previous

    def go_back_src(self, *args):
        self.root.ids.topbar.remove_widget(self.root.ids.topbar.children[0])
        self.root.ids.topbar.left_action_items = self.left_action_items
        self.root.ids.topbar.right_action_items = self.right_action_items
        self.root.ids.screen_manager.current = self.previous
        print("goback to tab-> ", self.last_tab)
        self.tab_switch(self.last_tab)

    def tab_switch(self,*args):
        #print("switch->",args)
        #print("switch->",args[-1])
        new_l = []
        scr = self.root.ids.screen_manager.current
        store.store_load()
        if scr == "bro_screen":
            st = store["db"]
        elif scr == "pre_screen":
            st =store["preferiti"]

        #print("switching from", scr, args[-1])

        if args[-1]=="Tutti":

            self.root.ids.screen_manager.current_screen.children[0].data = st

            return

        for i in st:
             if i["cat"]==args[-1].upper():
                    new_l.append(i)
        store.store_sync()
        print("Last tab->", args[-1])
        self.last_tab = args[-1]
        self.root.ids.screen_manager.current_screen.children[0].data = new_l


    def research_contents(self,b):
        #self.root.ids.screen_manager.current = "img_screen" 

        #print("childtoolbar",self.root.ids.topbar.ids.headline_box.children)
        self.root.ids.topbar.remove_widget(self.root.ids.topbar.children[0])


        #self.root.ids.topbar.add_widget(la)
        self.root.ids.topbar.left_action_items = self.left_action_items
        self.root.ids.topbar.right_action_items = self.right_action_items

        #print("Query---> ",b.text)
        l = search_scraper(query=str(b.text))
        #print("len", len(l))
        store.store_load()

        store.store_put("db",l)
        store.store_sync()
        #print(self.root.ids.bro_screen.children)

        self.root.ids.bro_screen.children[0].data = store["db"]
        self.root.ids.tabs.switch_tab("Tutti")
        #self.root.ids.screen_manager.current = "bro_screen" 


    def search_prompt(self):
        self.left_action_items = self.root.ids.topbar.left_action_items
        self.right_action_items = self.root.ids.topbar.right_action_items
        self.root.ids.topbar.left_action_items = []
        self.root.ids.topbar.right_action_items = []
        boxlayout = MDBoxLayout(id = "headbox", orientation= "horizontal",padding=10)
        search_content = MDTextField(  icon_left='magnify',
                                          mode='line',
                                          #focus = True,
                                          line_color_normal=(1, 0, 1, 1),
                                          line_color_focus=(0, 0, 1, 1),
                                          text_color_focus=self.theme_cls.text_color,
                                          text_color_normal=self.theme_cls.text_color[0:3] + [0.7],
                                          hint_text='Cerca...',
                                          on_text_validate = self.research_contents
                                          )
        back_icon = MDIconButton( icon = "arrow-left",on_release=self.go_back_src )
        boxlayout.add_widget(search_content)
        boxlayout.add_widget(back_icon)
        self.root.ids.topbar.add_widget(boxlayout)
    def create_res_tbar(self):
        print("create_res_tbar")
        self.left_action_items = self.root.ids.topbar.left_action_items
        self.right_action_items = self.root.ids.topbar.right_action_items
        self.root.ids.topbar.left_action_items = []
        self.root.ids.topbar.right_action_items = []
        boxlayout = MDBoxLayout(id = "headbox", orientation= "horizontal",padding=10)

        back_icon = MDIconButton( icon = "arrow-left",on_release=self.go_back_src )
        boxlayout.add_widget(back_icon)
        self.root.ids.topbar.add_widget(boxlayout)


    def play(self, root):
        if root.cat =="IMMAGINI":
            print("IMMAGINI")
            s_url = sanitize_url(root.link)
            res_o = res_scraper("IMMAGINI",s_url)
            self.root.ids.img_screen.ids.image.source = sanitize_url(res_o["url"] )
            self.root.ids.img_screen.ids.img_label.text =res_o["desc"].replace("** ", "[/b]").replace("**","[b]")
            self.root.ids.img_screen.ids.size = (400, 400 )#/ self.image_ratio
            self.previous = self.root.ids.screen_manager.current
            self.root.ids.screen_manager.current = "img_screen" 
            return

        if root.cat == "AUDIO":
            print("original link", root.link)

            print("AUDIO")
            s_url = sanitize_url(root.link)
            self.root.ids.aud_screen.ids.aud_box.clear_widgets()
            res_o = res_scraper("AUDIO",sanitize_url(s_url))
            if kivy.platform == "android":
                mp = MusicPlayerAndroid(audio_track = sanitize_url(res_o["url"]), poster ="./res/audio.png", innerlabel = res_o["desc"])
                mp.build()
                #mp.playaudio("start")
                self.root.ids.aud_screen.ids.aud_box.add_widget(mp)
                self.previous = self.root.ids.screen_manager.current
                self.root.ids.screen_manager.current = "aud_screen"  
                #print("going to ", sanitize_url(res_o["url"]))
                return

            elif kivy.platform =="linux" :
                mp = MusicPlayer(audio_track = sanitize_url(res_o["url"]), poster ="./res/audio.png",innerlabel = res_o["desc"])
                mp.build()
                #mp.playaudio("start")
                self.root.ids.aud_screen.ids.aud_box.add_widget(mp)
                self.previous = self.root.ids.screen_manager.current
                self.root.ids.screen_manager.current = "aud_screen"  
                return


        if root.cat == "VIDEO":
            s_url = sanitize_url(root.link)
            res_o = res_scraper("VIDEO",s_url)
            self.root.ids.vid_screen.ids.video_player.source = sanitize_url(res_o["url"])
            self.root.ids.vid_screen.ids.video_player.thumbnail = sanitize_url(res_o["poster"])
            self.root.ids.vid_screen.ids.video_label.text =res_o["desc"].replace("** ", "[/b]").replace("**","[b]")
            self.previous = self.root.ids.screen_manager.current
            self.root.ids.screen_manager.current = "vid_screen"        
            return

        if root.cat == "TESTI":
            print("TESTI")
            s_url = sanitize_url(root.link)
            res_o = res_scraper("TESTI",s_url)
            self.root.ids.txt_screen.ids.txt_label.text = res_o["desc"].replace("** ", "[/b]").replace("**","[b]")
            self.root.ids.txt_screen.ids.txt_button.link = sanitize_url(res_o["url"])
            self.previous = self.root.ids.screen_manager.current
            self.root.ids.screen_manager.current = "txt_screen"        
            return
        
        else:
            print("default")
                







SDLApp().run()