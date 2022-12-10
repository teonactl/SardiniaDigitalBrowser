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
from kivymd.uix.navigationdrawer.navigationdrawer import MDNavigationDrawerItem

from kivymd.uix.dialog import MDDialog


from kivy.uix.scatterlayout import ScatterLayout
from kivy.clock import Clock
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

categorie_str="""
VIDEO
    Cortometraggi
    Cinegiornali
    Concerti e festival
    Convegni e seminari
    Documentari
    Documenti multimediali
    Film
    Gare poetiche
    Interviste
    Programmi televisivi
    Rappresentazioni teatrali
    Spot
    Video istituzionali
IMMAGINI
    Ambiente e territorio
    Archeologia
    Architettura
    Arte
    Artigianato
    Atti di governo
    Economia e società
    Cartografia
    Enogastronomia
    Eventi
    Flora e fauna
    Letteratura
    Luoghi della cultura
    Spettacolo
    Sport
    Storia e tradizioni
AUDIO
    Canti a chitarra
    Canti a tenore
    Canti monodici
    Canti polivocali
    Canti sacri
    Discorsi
    Favole
    Gare poetiche
    Interviste
    Musica contemporanea
    Narrativa
    Poesie
    Strumenti
    Trasmissioni radiofoniche
TESTI
    Annuari
    Atti di convegno
    Brochure
    Cataloghi
    Dizionari - enciclopedie
    Documenti d'archivio
    Guide
    Epistolari
    Libretti
    Monografie - saggi
    Narrativa
    Periodici
    Poesie
ARGOMENTI
    Ambiente e territorio
    Archeologia
    Architettura
    Arte
    Artigianato
    Atti di governo
    Cartografia
    Economia e società
    Enogastronomia
    Eventi
    Flora e fauna
    Letteratura
    Lingua sarda
    Luoghi della cultura
    Musica
    Spettacolo
    Sport
    Storia e tradizioni
"""

welcome_string = """
Benvenuto! 
Quest app ti permette di accedere a tutti i contenuti di Sardegna Digital Library:
l'archivio digitale della Regione Sardegna.
Puoi cercare contenuti o scegliere le categorie dal menù laterale, puoi salvare i tuoi preferiti e condividerli con chi preferisci!
"""
info_string = """
[b]Autore[/b] teonactl
[b]Mail[/b] teonactl@hotmail.it
[b]Source[/b] https://github.com/teonactl/SardegnaDigitalExplorer
"""
#Welcome Dialog class
class Welcome(MDBoxLayout):
    text = StringProperty(welcome_string)
#Info Dialog class
class Info(MDBoxLayout):
    text = StringProperty(info_string)

class MyScatter(ScatterLayout):
    
    def on_touch_down(self, touch):
        self.app = MDApp.get_running_app()

        if self.collide_point(*touch.pos):
            self.pressed = touch.pos

            if self.pressed[1]> self.app.root.ids.topbar.y:
                return False
                
            return super(MyScatter, self).on_touch_down(touch)

class SDLApp(MDApp):
    def __init__(self, **kwargs):
        super(SDLApp, self).__init__(**kwargs)
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.secondaryry_palette = "Orange"
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
        self.n_pages = store["n_pages"]
        self.s_scraper = search_scraper
        self.a_query = store["a_query"]
        self.a_page = store["a_page"]
        self.i_dialog = None
        self.w_dialog = None

    def welcome_dialog(self):
        #print(self.root.size)
        if not self.w_dialog:
            self.w_dialog = MDDialog(
                title="Benvenuto",
                type="custom",
                size= self.root.size,
                content_cls=Welcome(),
                buttons=[],
            )
        self.w_dialog.open()
    def info_dialog(self):
        if not self.i_dialog:
            self.i_dialog = MDDialog(
                title="Informazioni",
                type="custom",
                size= self.root.size,
                content_cls=Info(),
                buttons=[],
            )
        self.i_dialog.open()     

    def set_toolbar_title_halign(self, *args):
        self.root.ids.topbar.ids.label_title.halign = "center"
        print(self.root.ids.topbar.ids.label_title.text)

    def build(self):

        return MainScreen()
    def on_start(self):
        Clock.schedule_once(self.set_toolbar_title_halign)
        if not store["init"]:
            self.welcome_dialog()
            store.store_load()
            store.store_put("init",True)
            store.store_sync()

    def but_cb(self, b):
        print("res--->",b)
        self.research_contents(b)
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.bro_screen.ids.rv.scroll_y=1
        self.root.ids.screen_manager.current = "bro_screen"
        self.root.ids.topbar.title = b.text


        

    def openlink(self, url):
        url = sanitize_url(url)
        webbrowser.open(url)
    def go_back(self, *args):
        self.root.ids.screen_manager.current = self.previous

    def go_back_src(self, *args):
        print("removing first of",self.root.ids.topbar.children)
        self.root.ids.topbar.remove_widget(self.root.ids.topbar.children[0])
        self.root.ids.topbar.left_action_items = self.left_action_items
        self.root.ids.topbar.right_action_items = self.right_action_items
        self.root.ids.screen_manager.current = self.previous
        print("goback to tab-> ", self.last_tab)
        self.root.ids.topbar.title = self.a_query
        self.root.ids.topbar.ids.label_title.halign = "center"
        self.tab_switch(self.last_tab)

    def tab_switch(self,*args):
        new_l = []
        scr = self.root.ids.screen_manager.current
        store.store_load()
        if scr == "bro_screen":
            st = store["db"]
        elif scr == "pre_screen":
            st =store["preferiti"]
        self.last_tab = args[-1]

        if args[-1]=="Tutti":
            if self.root.ids.screen_manager.current == "bro_screen":
                self.root.ids.screen_manager.current_screen.ids.rv.data = st

            else : 

                self.root.ids.screen_manager.current_screen.children[0].data = st
            return

        for i in st:
             if i["cat"]==args[-1].upper():
                    new_l.append(i)
        store.store_sync()
        if self.root.ids.screen_manager.current == "bro_screen":
           self.root.ids.screen_manager.current_screen.ids.rv.data = new_l
        else :
            self.root.ids.screen_manager.current_screen.children[0].data = new_l


    def research_contents(self,b):
        #self.root.ids.screen_manager.current = "img_screen" 

        #print("childtoolbar",self.root.ids.topbar.ids.headline_box.children)
        if not isinstance(b, MDNavigationDrawerItem):
            print("NOTFROMDRAWER:..")

            #self.root.ids.topbar.add_widget(la)
            self.root.ids.topbar.remove_widget(self.root.ids.topbar.children[0])

            self.root.ids.topbar.left_action_items = self.left_action_items
            self.root.ids.topbar.right_action_items = self.right_action_items

        #print("Query---> ",b.text)
        l, n_pages = search_scraper(query=str(b.text))
        self.n_pages = n_pages
        self.a_query = str(b.text)
        #print("len", len(l))
        store.store_load()
        store.store_put("a_query", str(b.text))
        store.store_put("a_page", 0)
        store.store_put("n_pages", n_pages)
        store.store_put("db",l)
        store.store_sync()
        #print(self.root.ids.bro_screen.children)

        self.root.ids.bro_screen.children[0].data = store["db"]
        self.root.ids.tabs.switch_tab("Tutti")
        self.root.ids.topbar.title = b.text
        self.root.ids.topbar.ids.label_title.halign = "center"
        #self.root.ids.screen_manager.current = "bro_screen" 
        toast(f"Trovate {n_pages} Pagine..")


    def search_prompt(self):
        self.left_action_items = self.root.ids.topbar.left_action_items
        self.right_action_items = self.root.ids.topbar.right_action_items
        self.root.ids.topbar.left_action_items = []
        self.root.ids.topbar.right_action_items = []
        self.root.ids.topbar.title = ""
        boxlayout = MDBoxLayout(id = "headbox", orientation= "horizontal",padding=10)
        search_content = MDTextField(  icon_left='magnify',
                                          mode='round',
                                          #focus = True,
                                          #line_color_normal=(1, 0, 1, 1),
                                          #line_color_focus=(0, 0, 1, 1),
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
        print(self.root.ids.topbar.children)
        if len(self.root.ids.topbar.children)>2:
            pass
            self.root.ids.topbar.remove_widget(self.root.ids.topbar.children[0])

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
                try:
                    mp.build()
                except :
                    toast("Caricamento risorsa non riuscito...")
                    return
                #mp.playaudio("start")
                self.root.ids.aud_screen.ids.aud_box.add_widget(mp)
                self.previous = self.root.ids.screen_manager.current
                self.root.ids.screen_manager.current = "aud_screen"  
                #print("going to ", sanitize_url(res_o["url"]))
                return

            elif kivy.platform =="linux" :
                mp = MusicPlayer(audio_track = sanitize_url(res_o["url"]), poster ="./res/audio.png",innerlabel = res_o["desc"])
                try:
                    mp.build()
                except :
                    toast("Caricamento risorsa non riuscito...")
                    return
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