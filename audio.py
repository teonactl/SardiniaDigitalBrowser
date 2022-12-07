import time
import kivy
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.slider import Slider
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDIconButton
from kivy.clock import Clock
from kivy.core.window import Window

from kivymd.uix.label import MDLabel

from kivy.uix.scrollview import ScrollView
if kivy.platform =="android":
    from jnius import autoclass
else :
    from kivy.core.audio import SoundLoader



md = """


**Titolo:**  Conversazioni teatrali : n. 9  
**Autore:**  Meazza Donatella  
**Regia:**  Meazza Donatella

**Editore:**  Rai Sardegna  
**Data di trasmissione:**  2019/10/03  
**Emittente:**  Radio Rai Sardegna  
**Data di creazione:**  2019/10/03

**Programma:**  Conversazioni teatrali  
**Conduttore:**  Meazza Donatella  
**Raccolta:**  Archivio Rai


**Tipologia:**  trasmissioni radiofoniche  
**Argomento:**  Economia e società, Spettacolo  
**Lingua:**  italiano  
**Diritti:**  © RAI – Radiotelevisione Italiana  
**Condizioni di utilizzo:**  Alcuni diritti riservati  
**Licenza:**  Creative Commons: Attribuzione - Non commerciale - Condividi allo stesso modo 4.0 Internazionale (CC BY-NC-SA 4.0)


**Descrizione:**  A tu per tu con i grandi protagonisti della scena teatrale sarda

**Note:**  E' intervenuta: Maria Grazia Sughi

**ID:** 681404  
**Link risorsa:** //www.sardegnadigitallibrary.it/index.php?xsl=2436&id=681404  




""".replace("** ", "[/b]").replace("**","[b]")
class MySlider(Slider):

    def __init__(self, **kwargs):
        super(MySlider, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.parent.parent.position(self.value)
            touch.ungrab(self)
            return True



class MusicPlayer(MDRelativeLayout):
    def __init__(self, **kwargs):
        self.last_time = None
        self.startload = None     
        self.mdlabel  = kwargs.pop("innerlabel")
        self.mdlabel = self.mdlabel.replace("** ", "[/b]").replace("**","[b]")
        self.audio_track = kwargs.pop("audio_track")
        self.poster = kwargs.pop("poster")
        self.sound = SoundLoader.load(self.audio_track)
        self.song_title = self.mdlabel[15:].split("[b]Autore:")[0]
        super(MusicPlayer, self).__init__(**kwargs)

    def build(self):
        layout = MDRelativeLayout()
        self.songlabel = Label(pos_hint={'center_x':0.5, 'center_y':.96},
                               size_hint=(1,1),
                               font_size=18)
        
        self.currenttime = Label(text = "00:00",
                               pos_hint={'center_x':.16, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18) 

        self.load_lab = Label(text = "",
                               pos_hint={'center_x':.46, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
        self.totaltime = Label(text = time.strftime('%M:%S', time.gmtime(self.sound.length)),
                               pos_hint={'center_x':0.84, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
   
        self.progressbar = MySlider(min = 0,
                                       pos_hint={'center_x':0.5, 'center_y':0.12},
                                       size_hint=(.8,.03),
                                       )
        self.playbutton = MDIconButton(pos_hint={'center_x':0.3, 'center_y':0.05},
                                       icon="play",
                                       on_press = self.playaudio)
        
        self.pausebutton = MDIconButton(pos_hint={'center_x':0.45, 'center_y':0.05},
                                       icon="pause",
                                       on_press = self.pauseaudio, disabled=True)
        self.stopbutton = MDIconButton(pos_hint={'center_x':0.6, 'center_y':0.05},
                                       icon="stop",
                                       on_press = self.stopaudio,
                                       disabled=False)
        self.id = "player"
        self.ids['slider_id'] = self.progressbar   
        self.ex_box = MDBoxLayout(orientation="vertical",
                                pos_hint={'center_x':0.5, 'center_y':0.65},
                                size_hint= (.9,.75),
                                
                                )
        self.innerlabel = MDLabel(markup= True, 
                                size_hint= (1, None),
                                text = self.mdlabel,
                                padding= (10, 10),
                                adaptive_height= True
                                )  

        self.s_view = ScrollView()

        self.ids['label_id'] = self.innerlabel


        self.in_box = MDBoxLayout(orientation= "vertical",
                               size_hint= (.8,None),
                               adaptive_height= True
                                #height = self.innerlabel.height# + 500
                               )
        self.in_box.add_widget(self.innerlabel)
        self.s_view.add_widget(self.in_box)
        self.ex_box.add_widget(self.s_view)
        layout.add_widget(self.ex_box)
        #layout.add_widget(self.songlabel)
        layout.add_widget(self.currenttime)
        layout.add_widget(self.totaltime)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.load_lab)
        layout.add_widget(self.playbutton)  
        layout.add_widget(self.pausebutton)
        layout.add_widget(self.stopbutton)
        self.add_widget(layout)
        self.progressbar.max = self.sound.length
        return layout


    def position(self, pos):
        self.pauseaudio(self)
        self.sound.seek(pos)
        self.load_lab.text = "Loading..."
        self.startload = pos
        self.playaudio("nolast")
        self.updateprogressbar(pos)
        
    def playaudio(self,obj):
        if self.last_time :
            if obj != "nolast":
                self.sound.seek(self.last_time)
                self.sound.play()
            else:
                self.sound.play()
        
            self.timeEvent = Clock.schedule_interval(self.settime,1)
            self.playbutton.disabled = True
            self.pausebutton.disabled = False
            return 

        self.playbutton.disabled = True
        self.pausebutton.disabled = False
        #self.songlabel.text = self.song_title
        self.sound.volume = 1
        self.sound.play()
        self.timeEvent = Clock.schedule_interval(self.settime,1)


    def updateprogressbar(self,value):
        self.progressbar.value =value
        if int(self.progressbar.value) == int(self.sound.length):
            self.stopaudio(self)
            
    def settime(self,t):
        if self.startload:
            if int(self.startload) <= int(self.sound.get_pos()):
                self.load_lab.text = ""
                self.startload = None
            self.currenttime.text = ''
            return
        self.currenttime.text =  time.strftime('%M:%S', time.gmtime(self.sound.get_pos()))
        self.totaltime.text = time.strftime('%M:%S', time.gmtime(self.sound.length))

        self.updateprogressbar(self.sound.get_pos())

    def pauseaudio(self,obj):
        current_time = time.strftime('%M:%S', time.gmtime(self.sound.get_pos()))
        self.last_time = self.sound.get_pos()
        self.playbutton.disabled = False
        self.pausebutton.disabled = True
        self.sound.stop()
        if self.timeEvent:

            self.timeEvent.cancel()
        self.progressbar.value = self.sound.get_pos()

    def stopaudio(self,obj):
        self.last_time = 0
        self.sound.stop()
        if self.timeEvent:

            self.timeEvent.cancel()
        self.progressbar.value = 0
        self.currenttime.text = "00:00"
        self.playbutton.disabled = False
        self.pausebutton.disabled = True







class MusicPlayerAndroid(MDRelativeLayout):

    def __init__(self, **kwargs):
        self.prevstop = False
        self.last_time = None
        self.startload = None        

        self.mdlabel  = kwargs.pop("innerlabel")
        self.mdlabel = self.mdlabel.replace("** ", "[/b]").replace("**","[b]")
        self.audio_track = kwargs.pop("audio_track")
        self.poster = kwargs.pop("poster")
        MediaPlayer = autoclass('android.media.MediaPlayer')
        self.sound = MediaPlayer()
        self.sound.setDataSource(self.audio_track)
        self.sound.prepare()         
        super(MusicPlayerAndroid, self).__init__(**kwargs)

    def build(self):
        layout = MDRelativeLayout()
        self.songlabel = Label(pos_hint={'center_x':0.5, 'center_y':.96},
                               size_hint=(1,1),
                               font_size=18)
        self.albumimage = AsyncImage(pos_hint={'center_x':0.5, 'center_y':0.55},
                               size_hint=(.8,.75))
        self.currenttime = Label(text = "00:00",
                               pos_hint={'center_x':.16, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
        self.load_lab = Label(text = "",
                               pos_hint={'center_x':.46, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
        self.totaltime = Label(text = time.strftime('%M:%S', time.gmtime(self.sound.getDuration()/1000)),
                               pos_hint={'center_x':0.84, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
   
        self.progressbar = MySlider(min = 0,
                                       pos_hint={'center_x':0.5, 'center_y':0.12},
                                       size_hint=(.8,.03),
                                       )
        self.playbutton = MDIconButton(pos_hint={'center_x':0.3, 'center_y':0.05},
                                       icon="play",
                                       on_press = self.playaudio)
        
        self.pausebutton = MDIconButton(pos_hint={'center_x':0.45, 'center_y':0.05},
                                       icon="pause",
                                       on_press = self.pauseaudio, disabled=True)
        self.stopbutton = MDIconButton(pos_hint={'center_x':0.6, 'center_y':0.05},
                                       icon="stop",
                                       on_press = self.stopaudio,
                                       disabled=False)
        self.id = "player"
        self.ids['slider_id'] = self.progressbar
        self.ex_box = MDBoxLayout(orientation="vertical",
                                pos_hint={'center_x':0.5, 'center_y':0.65},
                                size_hint= (.9,.75),
                                
                                )
        self.innerlabel = MDLabel(markup= True, 
                                size_hint= (1, None),
                                text = self.mdlabel,
                                padding= (10, 10),
                                adaptive_height= True
                                )  

        self.s_view = ScrollView()

        self.ids['label_id'] = self.innerlabel


        self.in_box = MDBoxLayout(orientation= "vertical",
                               size_hint= (.8,None),
                               adaptive_height= True
                                #height = self.innerlabel.height# + 500
                               )
        self.in_box.add_widget(self.innerlabel)
        self.s_view.add_widget(self.in_box)
        self.ex_box.add_widget(self.s_view)
        layout.add_widget(self.ex_box)
        #layout.add_widget(self.songlabel)
        #layout.add_widget(self.albumimage)
        layout.add_widget(self.currenttime)
        layout.add_widget(self.totaltime)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.load_lab)
        layout.add_widget(self.playbutton)  
        layout.add_widget(self.pausebutton)
        layout.add_widget(self.stopbutton)
        self.add_widget(layout)
        self.progressbar.max = self.sound.getDuration()/1000
        return layout


    def position(self, pos):
        self.pauseaudio(self)
        self.sound.seekTo(pos*1000, 1)
        self.load_lab.text = "Loading..."
        self.startload = pos*1000
        self.playaudio("nolast")
        self.updateprogressbar(pos)
        
    def playaudio(self,obj):
        print("play")
        self.pausebutton.disabled = True
        if self.prevstop:
            self.sound.prepare()
            self.prevstop = False     

        if self.last_time:
            if obj != "nolast":
                self.sound.seekTo(self.last_time, 1)
                self.sound.start()
            else:
                self.sound.start()

            self.timeEvent = Clock.schedule_interval(self.settime,1)
            self.playbutton.disabled = True
            self.pausebutton.disabled = False
            self.stopbutton.disabled = False
            return 
        self.playbutton.disabled = True
        self.stopbutton.disabled = False
        self.pausebutton.disabled = False
        #self.song_title = self.audio_track
        #self.songlabel.text = self.song_title
       # self.albumimage.source = self.poster
        self.sound.start()
        self.timeEvent = Clock.schedule_interval(self.settime,1)


    def updateprogressbar(self,value):
        self.progressbar.value =value
        if int(self.progressbar.value) == int(self.sound.getDuration()/1000):
            self.stopaudio(self)
            
    def settime(self,t):
        if self.startload:
            if int(self.startload) <= int(self.sound.getCurrentPosition()):
                self.load_lab.text = ""
                self.startload = None
            self.currenttime.text = ''
            return
        self.currenttime.text =  time.strftime('%M:%S', time.gmtime(self.sound.getCurrentPosition()/1000))
        self.totaltime.text = time.strftime('%M:%S', time.gmtime(self.sound.getDuration()/1000))
        self.updateprogressbar(self.sound.getCurrentPosition()/1000)

    def pauseaudio(self,obj):
        print("pause at",self.sound.getCurrentPosition())
        current_time = time.strftime('%M:%S', time.gmtime(self.sound.getCurrentPosition()/1000))
        self.last_time = self.sound.getCurrentPosition()#/1000
        self.playbutton.disabled = False
        self.pausebutton.disabled = True
        self.stopbutton.disabled = True
        self.sound.pause()
        if self.timeEvent:
            self.timeEvent.cancel()

        self.progressbar.value = self.sound.getCurrentPosition()/1000

    def stopaudio(self,obj):
        print("stop")
        self.prevstop = True
        self.pausebutton.disabled = True
        self.last_time = 0
        self.sound.stop()
        if self.timeEvent:
            self.timeEvent.cancel()

        self.progressbar.value = 0
        self.currenttime.text = "00:00"
        self.playbutton.disabled = False
        self.stopbutton.disabled = True
