from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.screen import MDScreen
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty

class ImageScreen(MDScreen):
    res_link = StringProperty()

class IMG(ButtonBehavior,AsyncImage):

    def on_release(self, *args):
        print("released", args  )
    def on_press(self, *args):
        print("pressed", args  )
