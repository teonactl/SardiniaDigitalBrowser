from kivymd.uix.card import MDCard
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty


from kivy.storage.jsonstore import JsonStore
import webbrowser
from utils import *

store = JsonStore('db.json')


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
class BrowseViewer(RecycleView):
    def __init__(self, **kwargs):
        super(BrowseViewer, self).__init__(**kwargs)
        self.data = store["db"]

    def update(self):
        print("updatingrv...",len(store["db"]))
        self.data = store["db"]
        self.refresh_from_data()

        