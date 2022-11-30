import os
os.environ["KIVY_VIDEO"] = "ffpyplayer"
os.environ['KIVY_AUDIO'] = "ffpyplayer"

import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import dp

from kivymd.app import MDApp

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



# The main kv file is loaded indipendently because of naming rules [ call it like your App class instance less the final "App" eg: NavigationApp--> navigation.kv]
Builder.load_file("browse.kv")
Builder.load_file("search.kv")
Builder.load_file("image.kv")
Builder.load_file("video.kv")
Builder.load_file("audio.kv")

store = JsonStore('db.json')



class MainScreen(MDScreen):
    pass
class MyScreenManager(MDScreenManager):
    pass




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
    def reload_browser(self):
        print("reload")
        l = search_scraper(query="formaggio")

        store.store_put("db",l)
        store.store_sync()
        self.root.ids.bro_screen.children[0].data = store["db"]



    def build(self):
        #self.theme_cls.theme_style = "Dark"
        return MainScreen()
    def go_back(self):
        print("goback ", self.previous)
        self.root.ids.screen_manager.current = self.previous
    def go_back_src(self, *args):
        self.root.ids.topbar.remove_widget(self.root.ids.topbar.children[0])
        self.root.ids.topbar.left_action_items = self.left_action_items
        self.root.ids.topbar.right_action_items = self.right_action_items


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
        #self.root.ids.bro_screen.children[0].update()
        #self.root.ids.screen_manager.current = "bro_screen" 


    def search_prompt(self):
        self.left_action_items = self.root.ids.topbar.left_action_items
        self.right_action_items = self.root.ids.topbar.right_action_items
        self.root.ids.topbar.left_action_items = []
        self.root.ids.topbar.right_action_items = []
        boxlayout = MDBoxLayout(id = "headbox", orientation= "horizontal",padding=10)
        search_content = MDTextField(icon_left='magnify',
                                          mode='round',
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
        sear_p = MDTextField(icon_right =  "magnify")
        sear_p.fill_color= [0, 0, 0, .4 ]
        sear_p.text_color= "black"
        sear_p.hint_text: 'Empty field'
        self.root.ids.topbar.add_widget(boxlayout)


    def play(self, root):
        if root.cat =="IMMAGINI":
            print("IMMAGINI")
            s_url = sanitize_url(root.link)
            res_o = res_scraper("IMMAGINI",s_url)
            self.root.ids.img_screen.ids.image.source = sanitize_url(res_o["url"] )
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
                mp = MusicPlayerAndroid()
                mp.load(sanitize_url(res_o["url"]))
                mp.build()
                #print("Mp ANDROID-->"*10,dir(mp))
                #mp.play()
                self.root.ids.aud_screen.ids.aud_box.add_widget(mp)
                self.previous = self.root.ids.screen_manager.current
                self.root.ids.screen_manager.current = "aud_screen"  
                #print("going to ", sanitize_url(res_o["url"]))
                return

            elif kivy.platform =="linux" :
                mp = MusicPlayer()
                #print("Mp LINUX-->"*10,dir(mp))
                mp.build( sanitize_url(res_o["url"]), "./res/audio.png")
                self.root.ids.aud_screen.ids.aud_box.add_widget(mp)
                self.previous = self.root.ids.screen_manager.current
                self.root.ids.screen_manager.current = "aud_screen"  
                #print("going to ", sanitize_url(res_o["url"]))
                return


        if root.cat == "VIDEO":
            #print("VIDEO")         
            s_url = sanitize_url(root.link)
            res_o = res_scraper("VIDEO",s_url)
            #player = VPlayer()
            #player.source = res_o["url"]
            #print(dir(player))
            #WHY is not working!!??
            #player.thumbnail=sanitize_url(res_o["poster"])#"https://pngimg.com/uploads/pineapple/pineapple_PNG2750.png"
            #player.fullscreen = True
            #player.state = "play"
            #self.root.ids.vid_screen.ids.vid_box.clear_widgets()
            #self.root.ids.vid_screen.ids.vid_box.add_widget(player)
            #player.do_layout()
            self.root.ids.vid_screen.ids.video_player.source = sanitize_url(res_o["url"])
            self.root.ids.vid_screen.ids.video_player.thumbnail = sanitize_url(res_o["poster"])
            self.previous = self.root.ids.screen_manager.current
            self.root.ids.screen_manager.current = "vid_screen"        
            return

        if root.cat == "TESTI":
            #print(root.link)
            print("TESTI")
        else:
            print("default")
                






SDLApp().run()