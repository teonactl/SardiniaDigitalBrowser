import random
import time
import kivy
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform 
from kivy.logger import Logger
from kivymd.app import MDApp

if kivy.platform =="android":

    from jnius import autoclass

class MySlider(Slider):
    def on_touch_down(self, touch):
        #print("touch y-->",dir(touch),dir( MDApp.get_running_app().root.ids.aud_screen.ids.aud_box.children[0].ids.slider_id), touch.pos)
        touch.grab(self)
        print("touch " , touch.ppos)
        print("border",self.border_vertical)
        print("slider y", MDApp.get_running_app().root.ids.aud_screen.ids.aud_box.children[0].ids.slider_id.pos)
        return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            return True


class MusicPlayer(MDRelativeLayout):


    
    def build(self,audio_track,poster):
        self.last_time = None
        print("audio_track", audio_track)
        self.sound = SoundLoader.load(audio_track)

        self.audio_track = audio_track
        self.poster = poster
        layout = MDRelativeLayout(md_bg_color = [0,0.5,1,1])

        self.songlabel = Label(pos_hint={'center_x':0.5, 'center_y':.96},
                               size_hint=(1,1),
                               font_size=18)
        self.albumimage = AsyncImage(pos_hint={'center_x':0.5, 'center_y':0.55},
                               size_hint=(.8,.75))
        self.currenttime = Label(text = "00:00",
                               pos_hint={'center_x':.16, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
        self.totaltime = Label(text = "00:00",
                               pos_hint={'center_x':0.84, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
    
        self.progressbar = MySlider(max = 100,
                                       min = 0,
                                       pos_hint={'center_x':0.5, 'center_y':0.12},
                                       size_hint=(.8,.75),
                                       )
        self.volumeslider = Slider(
                                    min=0,
                                   max=1,
                                   value = 0.5,
                                   orientation = 'horizontal',
                                   pos_hint={'center_x':0.2, 'center_y':0.05},
                                   size_hint=(.2,.2))
        #self.switch = Switch(pos_hint={'center_x':0.75, 'center_y':0.05})
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
        layout.add_widget(self.songlabel)
        layout.add_widget(self.albumimage)
        layout.add_widget(self.currenttime)
        layout.add_widget(self.totaltime)
        layout.add_widget(self.progressbar)
        #layout.add_widget(b)
        #layout.add_widget(self.volumeslider)
        #layout.add_widget(self.switch)
        layout.add_widget(self.playbutton)  
        layout.add_widget(self.pausebutton)
        layout.add_widget(self.stopbutton)
        self.add_widget(layout)
        def mute(instance,value):
           if value == True:
              self.sound.volume = 0
           else:
              self.sound.volume = 1
        
        #self.switch.bind(active = mute)
        def volume(instance,value):
           #print(value)
           self.sound.volume = value

           
        #self.volumeslider.bind(value = volume)
        #self.progressbar.bind(value = self.ff)
        Clock.schedule_once(self.playaudio)
        
        return layout
    def ff(self,but, eve):
        #print("ff", inst, val, dir(inst),dir(val))
        #print("but ",but.pos)
        #print("eve ",eve.pos)
        #if eve.pos[0]>= but.pos[0]:
        print("inside")


    def position(self,inst, value):
        print("inst ", str(inst.value) +" / "+str(inst.max))
        percent = inst.value  
        duration = self.sound.length
        #print("goto ",str(percent)+" %  of "+str(duration))
        val = (duration/100) * percent
        self.sound.seek(val)
        self.updateprogressbar(float(self.sound.get_pos())/100)
        self.settime(inst.value)

    def playaudio(self,obj):
        if self.last_time != None:
            self.sound.seek(float(self.last_time))
            self.sound.play()
            self.progressbarEvent = Clock.schedule_interval(self.updateprogressbar,1)
            self.timeEvent = Clock.schedule_interval(self.settime,1)
            #print("Reload at-->", self.last_time)
            self.playbutton.disabled = True
            self.pausebutton.disabled = False
            return False

        self.playbutton.disabled = True
        self.pausebutton.disabled = False
        self.song_title = self.audio_track
        self.songlabel.text = self.song_title.split("/")[-1][:-4] 
        self.albumimage.source = self.poster
        self.sound.volume = 0.5
        self.sound.play()
        self.progressbarEvent = Clock.schedule_interval(self.updateprogressbar, self.sound.length/60 )
        self.timeEvent = Clock.schedule_interval(self.settime,1)
    
        #print("Playing ",self.song_title.split("/")[-1][:-4] )
        #print("Duration ",self.sound.length/60 )
        return False

    def updateprogressbar(self,value):
        #print("updateprogressbar ", self.sound.get_pos())
        #print("to---> ", value)
        self.progressbar.value =value
            
    def settime(self,t):
        #print(self.sound.get_pos())
        current_time = time.strftime('%M:%S', time.gmtime(self.sound.get_pos()))
        total_time = time.strftime('%M:%S', time.gmtime(self.sound.length))
        self.currenttime.text = current_time
        self.totaltime.text = total_time
        self.updateprogressbar(float((self.sound.length/100)*(self.sound.get_pos()/100)))
        #print("settime-->",current_time)

    def pauseaudio(self,obj):
        current_time = time.strftime('%M:%S', time.gmtime(self.sound.get_pos()))
        self.last_time = self.sound.get_pos()
        print("Pause at-->", current_time )
        print("Pause at-->", self.sound.get_pos() )
        self.playbutton.disabled = False
        self.pausebutton.disabled = True
        self.sound.stop()
        self.progressbarEvent.cancel()

        self.timeEvent.cancel()
        self.updateprogressbar(float((self.sound.length/100)*(self.sound.get_pos()/100)))
        return False

    def stopaudio(self,obj):
        self.sound.stop()
        self.progressbarEvent.cancel()
        self.updateprogressbar(0)
        self.progressbarEvent.cancel()
        self.timeEvent.cancel()

        self.currenttime.text = "00:00"
        self.playbutton.disabled = False
        self.pausebutton.disabled = True






class MusicPlayerAndroid(MDRelativeLayout):
    def __init__(self, **kwargs):
        super(MusicPlayerAndroid, self).__init__(**kwargs)
        print("init___android_mp")
        MediaPlayer = autoclass('android.media.MediaPlayer')
        self.mplayer = MediaPlayer()

        self.secs = 0
        self.actualsong = ''
        self.length = 0
        self.isplaying = False

    def __del__(self):
        self.stop()
        self.mplayer.release()
        Logger.info('mplayer: deleted')

    def load(self, filename):
        try:
            self.poster = "./src/audio.png"
            self.actualsong = filename
            self.secs = 0
            self.mplayer.setDataSource(filename)        
            self.mplayer.prepare()
            self.length = self.mplayer.getDuration() / 1000
            Logger.info('mplayer load: %s' %filename)
            Logger.info ('type: %s' %type(filename) )
            return True
        except:
            Logger.info('error in title: %s' % filename) 
            return False

    def unload(self):
        self.mplayer.reset()

    def playaudio(self, *args):
        self.playbutton.disabled = True
        self.stopbutton.disabled = False
        self.song_title = self.actualsong
        self.songlabel.text = self.song_title.split("/")[-1][:-4]
        self.albumimage.source = self.poster
        self.mplayer.setVolume(0.5, 0.5) 
        self.mplayer.start()
        self.progressbarEvent = Clock.schedule_interval(self.updateprogressbar,self.mplayer.getDuration()/60)
        self.timeEvent = Clock.schedule_interval(self.settime,1)
        self.isplaying = True
        Logger.info('mplayer: play')
    def updateprogressbar(self,value):
        if self.progressbar.value < 100:
            self.progressbar.value +=1
            
    def settime(self,t):
        current_time = time.strftime('%M:%S', time.gmtime(self.progressbar.value))
        total_time = time.strftime('%M:%S', time.gmtime(self.mplayer.getDuration()))
        self.currenttime.text = current_time
        self.totaltime.text = total_time

    def stopaudio(self, *args):
        self.playbutton.disabled = False
        self.stopbutton.disabled = True
        self.mplayer.reset()
        self.secs=0
        self.isplaying = False
        Logger.info('mplayer: stop')

    def seek(self,timepos_secs):
        self.mplayer.seek(float(timepos_secs * 1000))
        Logger.info ('mplayer: seek %s' %int(timepos_secs))

    def build(self):
        layout = MDRelativeLayout(md_bg_color = [0,0.5,1,1])

        self.songlabel = Label(pos_hint={'center_x':0.5, 'center_y':.96},
                               size_hint=(1,1),
                               font_size=18)
        self.albumimage = AsyncImage(pos_hint={'center_x':0.5, 'center_y':0.55},
                               size_hint=(.8,.75))
        self.currenttime = Label(text = "00:00",
                               pos_hint={'center_x':.16, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
        self.totaltime = Label(text = "00:00",
                               pos_hint={'center_x':0.84, 'center_y':.145},
                               size_hint=(1,1),
                               font_size=18)
    
        self.progressbar = ProgressBar(max = 100,
                                       value = 0,
                                       pos_hint={'center_x':0.5, 'center_y':0.12},
                                       size_hint=(.8,.75))
        self.volumeslider = Slider(min=0,
                                   max=1,
                                   value = 0.5,
                                   orientation = 'horizontal',
                                   pos_hint={'center_x':0.2, 'center_y':0.05},
                                   size_hint=(.2,.2))
        self.switch = Switch(pos_hint={'center_x':0.75, 'center_y':0.05})
        self.playbutton = MDIconButton(pos_hint={'center_x':0.4, 'center_y':0.05},
                                       icon="play",
                                       on_press = self.playaudio)
        
        self.stopbutton = MDIconButton(pos_hint={'center_x':0.55, 'center_y':0.05},
                                       icon="stop",
                                       on_press = self.stopaudio, disabled=True)
        layout.add_widget(self.songlabel)
        layout.add_widget(self.albumimage)
        layout.add_widget(self.currenttime)
        layout.add_widget(self.totaltime)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.volumeslider)
        layout.add_widget(self.switch)
        layout.add_widget(self.playbutton)
        layout.add_widget(self.stopbutton)
        self.add_widget(layout)
        def mute(instance,value):
           if value == True:
              self.mplayer.setVolume( 0, 0)
           else:
              self.mplayer.setVolume( 1, 1)
        
        self.switch.bind(active = mute)
        def volume(instance,value):
           #print(value)
           self.mplayer.setVolume(value, value)
           
        self.volumeslider.bind(value = volume)
        return layout
