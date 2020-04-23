from PIL.ImageQt import rgb
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivy.config import Config
from kivy.clock import Clock
import datetime
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import Graph, MeshLinePlot, LinePlot
import numpy as np
import random
from kivy.utils import get_color_from_hex as rgb
from kivy.garden.knob import Knob
import itertools
import time
from kivy.uix.widget import Widget

from kivy.core.text import LabelBase

LabelBase.register(name="prototype", fn_regular="font/Prototype.ttf")

Config.set('graphics','width','960')
Config.set('graphics','height','780')

class MainWindow(Screen):

    def validate_user(self):
        username = self.ids.username.text
        password = self.ids.password.text
        if username == "adem" and password == "123456":
            print("başarı")
            self.manager.current = "second"
        else:
            print("basarisiz giriş ")


class SecondWindow(Screen):
    def deneme(self):
        print(self.ids.knob1.value)

class ThirdWindow(Screen):

    def __init__(self, **kwargs):
        super(ThirdWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.yap, 0)

    def yap(self,za):
        box = self.ids.deneme
        graph_theme = {
            'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
            'background_color': rgb('2b2b2b'),  # canvas background color
            'tick_color': rgb('7ba21d'),  # ticks and grid
            'border_color': rgb('000000')}  # border drawn around each graph
        self.graph = Graph(
            xlabel='Time (s)',
            ylabel='Temparature (°F)',
            x_ticks_major=10,
            y_ticks_major=10,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            #xmin=0,
            #ymin=0,
            **graph_theme)
        box.add_widget(self.graph)
        self.plot = LinePlot(line_width=2, color=[0.48, 0.63, 0.11, 1])
        self.graph.add_plot(self.plot)
        self.salise = 0
        self.saniye = 0
        self.dakika = 0
        self.values=[]

    def start(self):
        self.tan=Clock.schedule_interval(self.arttirici,0.5)
        self.zam = Clock.schedule_interval(self.zamanlayici, 0.1)

    def stop(self):
        if self.tan:
            Clock.unschedule(self.tan)
        self.ids.current_temp.text = ""
        self.ids.slider_temp.value = 0
        self.ids.slider_fan.value = 0
        self.salise = 0
        self.saniye = 0
        self.dakika = 0
        self.graph.remove_plot(self.plot)
        self.etiketteGoster()
        if self.zam:
            Clock.unschedule(self.zam)

    def zamanlayici(self,za):
        self.salise += 1
        if self.salise == 10:
            self.salise = 0
            self.saniye += 1
        if self.saniye == 60:
            self.saniye = 0
            self.dakika += 1
        self.etiketteGoster()

    def etiketteGoster(self):

        self.ids.etiket.text= "%s:%s:%s" % (self.dakika,str(self.saniye).zfill(2),str(self.salise).zfill(2))

    def arttirici(self,za):
        derece = self.ids.slider_temp.value
        fan_deger = self.ids.slider_fan.value
        self.son_deger =  derece - fan_deger / 2
        if len(self.values)>=100:
            self.values=[]
        self.values.append(self.son_deger)
        self.ids.current_temp.text = "%.2f" % self.son_deger
        self.plot.points = [(i, j) for i, j in enumerate(self.values)]


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class mainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    mainApp().run()



