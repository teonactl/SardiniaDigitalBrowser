from kivymd.uix.card import MDCard
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivy.storage.jsonstore import JsonStore
import webbrowser
from utils import *
from kivymd.toast import toast
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton,MDFloatingActionButton
from kivymd.uix.menu import MDDropdownMenu
from kivy import platform

import threading , time

if platform == 'android':
    from jnius import autoclass           

store = JsonStore('db.json')


class SDLCard(RecycleDataViewBehavior, MDCard):
    link = StringProperty()
    img = StringProperty()
    title = StringProperty()
    cat = StringProperty()
    uid = StringProperty()
    re_link = None
    

    def __init__(self, **kwargs):
        super(SDLCard, self).__init__(**kwargs)

       
        menu_items = [
                    {
                        "viewclass": "OneLineListItem",
                        "text": "Apri sul browser",
                        "height": dp(56),
                        "on_release":  lambda x ="web" : self.menu_callback(x),
                     }, {
                        "viewclass": "OneLineListItem",
                        "text": "Condividi",
                        "icon": "share",
                        "height": dp(56),
                        "on_release": lambda x="share" :self.menu_callback(x),

                     }
                ]
        self.menu = MDDropdownMenu( items=menu_items,width_mult=4)       

    def menu_callback(self, btype):
        self.app = MDApp.get_running_app()
        if btype == "web":
            self.app.openlink(self.re_link)
        elif btype == "share":
            self.share("SDE",self.re_link)
        self.menu.dismiss()
        self.re_link = None

    def open_menu(self, button):
        #print("button for -->", button.link)
        self.re_link = button.link
        self.menu.caller = button
        self.menu.open()

    def share(self, title, text):

        if platform == 'android':
            

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')
            intent = Intent()
            intent.setAction(Intent.ACTION_SEND)
            intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(text)))
            intent.setType('text/plain')
            chooser = Intent.createChooser(intent, String(title))
            PythonActivity.mActivity.startActivity(chooser)
        else :
            toast("Non implementato...")


    def store_preferito(self, obj):
        self.app = MDApp.get_running_app()
        rv = self.app.root.ids.bro_screen.ids.rv
        prv = self.app.root.ids.pre_screen.ids.prv
        manager  = self.app.root.ids.screen_manager
        tabs = self.app.root.ids.tabs
        store.store_load()
        pref = store["preferiti"]
        self.app.last_tab = tabs.get_current_tab().title
       # print(self.app.last_tab)
        if any(ob['uid'] == obj.uid for ob in pref):
            if manager.current == "bro_screen":
                return toast("E' già nei Preferiti!")
            elif manager.current == "pre_screen":
                for o in store["preferiti"]:
                    if o["uid"] == obj.uid:
                        pref.pop(pref.index(o))
                        store.store_put("preferiti", pref)
                        store.store_sync()
                        #print(self.app.last_tab)

                        prv.update()
                        self.app.tab_switch(self.app.last_tab)

                        toast("Eliminato dai Preferiti")
                        return


       
        pref.append({"link": obj.link, "img":obj.img, "title":obj.title,"cat":obj.cat,"uid":obj.uid })
        store.store_put("preferiti", pref)
        store.store_sync()
        tabs.switch_tab(self.app.last_tab)

        #rv.update()
        #print(self.app.last_tab)
        toast(f"Aggiunto ai preferiti!")
        return
      




class Tab(MDFloatLayout, MDTabsBase):
    pass

# Define the Recycleview class which is created in .kv file
class BrowseViewer(RecycleView):
    def __init__(self, **kwargs):
        super(BrowseViewer, self).__init__(**kwargs)
        self.data = store["db"]
        self.app = MDApp.get_running_app()
        self.lastscroll = 0
        self.loading = False

    def update(self):
        store.store_load()
        self.data = store["db"]
        self.refresh_from_data()

    def load_new_page(self, b):
        store.store_load()
        if self.app.a_page+1 <= store["n_pages"]:
            x = threading.Thread(target=self.thread_load)
            x.start()
        else:
             toast("Contenuti completi!")
        self.app.root.ids.bro_screen.remove_widget(b)
           

    def thread_load(self):
        self.loading = True
        store.store_load()
        m_toast("Caricando altri contenuti..")

        new_page , n = self.app.s_scraper(query=store["a_query"], page=store["a_page"]+1)
        #print("adding elements ->",len(new_page))

        if self.app.last_tab == "Tutti":
            #print("reloafing for TUTTI")
            n_pr_el = len(self.data)
            n_el = len(new_page)
            if n_el == 0:
                m_toast(f"Nessun nuovo contenuto!")
            else :
                m_toast(f"Caricate altre {n_el} risorse! ")
     
        else : 
            #print("RELOADING FOR", self.app.last_tab)
            n_pr_el = len([ i for i in self.data if i["cat"] ==self.app.last_tab.upper()])
            n_el = len([ i for i in new_page if i["cat"] == self.app.last_tab.upper()])

            if n_el == 0:
                m_toast(f"Nessun contenuto per la categoria {self.app.last_tab}.\n Continua a caricare, ancora {self.app.n_pages-self.app.a_page } pagine disponibili..")
            else :
                m_toast(f"Caricati altri {n_el} {self.app.last_tab} ")
        self.app.a_page =self.app.a_page+1
            
        store.store_put("db", self.data+new_page)
        store.store_put("a_page", self.app.a_page)
        store.store_sync()
        self.data = self.data + new_page
        scroll_index = 1- (n_pr_el / (n_pr_el+ n_el) )
        self.app.root.ids.tabs.switch_tab(self.app.last_tab)
        self.app.tab_switch("blabla", self.app.last_tab)
        self.scroll_y = scroll_index
        self.loading = False


    def on_scroll_stop(self, *args) :
        if self.scroll_y <= 0.01 :
            #print("nElements->",self.app.root.ids.bro_screen.children)
            if len(self.app.root.ids.bro_screen.children) ==1 and  not self.loading :

                but =   MDFloatingActionButton(
                                        icon ="refresh",
                                        pos_hint={"x":0.45, "y":0},
                                        on_press = self.load_new_page,
                                        )

                self.app.root.ids.bro_screen.add_widget(but)
                


        return super().on_scroll_stop(*args)

class PreferitiViewer(RecycleView):
    def __init__(self, **kwargs):
        super(PreferitiViewer, self).__init__(**kwargs)
        self.data = store["preferiti"]

    def update(self):
        store.store_load()
        self.data = store["preferiti"]
        self.refresh_from_data()        


class MyFButton(MDIconButton):
    pass