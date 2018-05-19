import random, math, sys, threading, time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Line, Color, Rectangle, Ellipse, InstructionGroup
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from kivy.core.text import LabelBase

from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from os.path import join
from kivy.core.audio import SoundLoader


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

class Game(Widget):
    def __init__(self, **kwargs):
        
        super (Game, self).__init__(**kwargs)
        self.layout = FloatLayout(size=Window.size)
        self.add_widget(self.layout)
        self.background = Background()
        self.layout.add_widget(self.background)
        self.missileList = []
        self.speed = 1
        self.score = 0
        self.scoreLabel = Label(text=str(self.score),font_size = 45, font_name= "font", pos_hint = {"x": .0, 'y':.4})
        self.layout.add_widget(self.scoreLabel)
        self.startButton = Button(text="Start",font_size = 30, font_name= "font", size_hint=[0.25,0.15], pos_hint={'center_x':0.5, 'center_y':0.5})
        self.startButton.bind(on_press=self.start)
        self.layout.add_widget(self.startButton)
        self.running = False
        if store.exists('score'):
            best =  store.get('score')['best']
            self.best = Label(text="Best: " + str(best), font_size = 45, font_name= "font", pos_hint = {"x": -0.35, 'y':.4})
            self.layout.add_widget(self.best)
        else:
            store.put('score', best=0)
            self.best = Label(text="Best: 0", font_size = 45, font_name= "font", pos_hint = {"x": -0.35, 'y':.4})
            self.layout.add_widget(self.best)
	    
    def start(self, instance):
        self.layout.remove_widget(self.startButton)
        self.layout.remove_widget(self.best)
        self.summon()
        self.running = True
        Clock.schedule_interval(self.update, 1.0 /100.0)
        
    def summon(self):
        edgex = int ((0.25*game.layout.width)/2)
        edgey = int ((0.25*game.layout.height)/2)

        while 1:
            col = False
            locx = random.randint(edgex, game.layout.width-edgex)
            locy = random.randint(edgey, game.layout.height-edgey)
            for m in self.missileList:
                if ((m.pos[0]-2*edgex <= locx) and (locx <= (m.pos[0]+2*edgex))) and (((m.pos[1]-2*edgey) <= locy) and (locy <= (m.pos[1]+2*edgey))):
                    col = True
            if not col:
                break
            
        loc = [locx,locy]
        startSize = 0.05*self.layout.width
        msl = Missile ([startSize,startSize],loc)
        self.missileList.append(msl)
        self.layout.add_widget(msl)
        
    def update(self, dt):
        global second
        global third
        global fourth
        global fifth
        global speedFlag1m
        global speedFlag2m
        global speedFlag3m
        global speedFlag4m
        global speedFlag5m
        global speedFlag3
        global speedFlag4
        
        if self.score >= 5 and speedFlag1m:
            self.speed = 2
            speedFlag1m = False
            
        if self.score >= 10 and second:
            self.speed = 1
            self.summon()
            second = False
            
        if self.score >= 20 and speedFlag2m:
            self.speed = 2
            speedFlag2m = False
            
        if self.score >= 30 and third:
            self.speed = 1
            self.summon()
            third = False
            
        if self.score >= 50 and speedFlag3m:
            self.speed = 2
            speedFlag3m = False
            
        if self.score>=70 and fourth:
            self.speed = 1
            self.summon()
            fourth = False
            
        if self.score >= 100 and speedFlag4m:
            self.speed = 2
            speedFlag4m = False
            
        if self.score>=125 and fifth:
            self.speed = 1
            self.summon()
            fifth = False
            
        if self.score>=150 and speedFlag5m:
            self.speed = 2
            speedFlag5m = False

        if self.score >= 200 and speedFlag3:
            self.speed = 3
            speedFlag3 = False

        if self.score >= 250 and speedFlag4:
            self.speed = 4
            speedFlag4 = False
            
        for m in self.missileList:
            m.move()
            
        if not self.running:
            return False
        
    def on_touch_down(self, touch):
        if self.running:
            self.clickx = touch.x
            self.clicky = touch.y
            for m in self.missileList:
                if m.image.collide_point(touch.x,touch.y):
                    m.explode()
                    sound.play()
                    self.layout.remove_widget(m)
                    self.missileList.remove(m)
                    self.summon()
                   
                    self.score = self.score+1
                    
                    #self.layout.remove_widget(self.scoreLabel)
                    self.scoreLabel.text=str(self.score)
                    #self.layout.add_widget(self.scoreLabel)

                    self.add_widget(Target (touch.x, touch.y))
                    
                    break
        else:
            return super(Game, self).on_touch_down(touch)

    def over(self):
        with self.layout.canvas:
            Color(1., 0, 0, 0.3)
            self.redScreen = Rectangle(pos=(0, 0), size=self.layout.size)
        for m in self.missileList:
            if m.hit:
                self.layout.remove_widget(m)
                self.layout.add_widget(m)
        self.layout.remove_widget(self.scoreLabel)
        self.layout.add_widget(self.scoreLabel)
        self.overButton = Button(text="Play Again?",font_size = 30, font_name= "font", size_hint=[0.25,0.15], pos_hint={'center_x':0.5, 'center_y':0.5})
        self.overButton.bind(on_press=self.restart)
        self.layout.add_widget(self.overButton)
        best = store.get('score')['best']
        if self.score>best:
            store.put('score', best=self.score)
            best = self.score
            self.best = Label(text="Best: " + str(best), font_size = 45, font_name= "font", pos_hint = {"x": -0.35, 'y':.4})
        self.layout.add_widget(self.best)
        
    def restart(self, instance):
        global second
        global third
        global fourth
        global fifth
        global speedFlag1m
        global speedFlag2m
        global speedFlag3m
        global speedFlag4m
        global speedFlag5m
        global speedFlag3
        global speedFlag4

       
        self.layout.clear_widgets()
        self.layout.canvas.clear()
        self.clear_widgets()
        self.add_widget(self.layout)
        self.layout.add_widget(self.background)
##        for m in self.missileList:
##            self.layout.remove_widget(m)
##        self.layout.remove_widget(self.overButton)
        self.missileList = []
        self.speed = 1
        self.score = 0
##        self.layout.remove_widget(self.scoreLabel)
        self.scoreLabel.text=str(self.score)
        self.layout.add_widget(self.scoreLabel)
        self.running = True
        self.summon()
        second = True
        third = True
        fourth = True
        fifth = True
        speedFlag1m = True
        speedFlag2m = True
        speedFlag3m = True
        speedFlag4m = True
        speedFlag5m = True
        speedFlag3 = True
        speedFlag4 = True
##        self.layout.canvas.remove(self.redScreen)
##        self.layout.remove_widget(self.best)
        Clock.schedule_interval(self.update, 1.0 / 100.0)
        
                
class Target(Widget):
    def __init__(self, tx, ty, **kwargs):
        super (Target, self).__init__(**kwargs)
        self.rad = 500
        self.tx = tx
        self.ty = ty
        self.once = True
        Clock.schedule_interval(self.draw, 1.0 / 100.0)

        angle1 = random.randint(0,360)
        self.theta1 = math.radians (angle1)

        if (angle1+120)>360:
            angle2 = 120-(360-angle1)
        else:
            angle2 = angle1+120
            
        self.theta2 = math.radians (angle2)
        
        if (angle2+120)>360:
            angle3 = 120-(360-angle2)
        else:
            angle3 = angle2+120

        self.theta3 = math.radians (angle3)


        
    def draw(self, dt):
        if self.rad <= 0.05*game.layout.width:
            self.canvas.clear()
            game.remove_widget(self)
            return False
        else:
            
            if self.once:
                self.ins = InstructionGroup()
                self.ins.add(Color (0.365, 0.678, 0.886, .8))
                
                pt1 = (self.tx+self.rad*math.cos(self.theta1), self.ty+(self.rad*math.sin(self.theta1)))
                pt2 = (self.tx+self.rad*math.cos(self.theta2), self.ty+(self.rad*math.sin(self.theta2)))
                pt3 = (self.tx+self.rad*math.cos(self.theta3), self.ty+(self.rad*math.sin(self.theta3)))

                ed1 = (self.tx+game.layout.width*math.cos(self.theta1), self.ty+(game.layout.width*math.sin(self.theta1)))
                ed2 = (self.tx+game.layout.width*math.cos(self.theta2), self.ty+(game.layout.width*math.sin(self.theta2)))
                ed3 = (self.tx+game.layout.width*math.cos(self.theta3), self.ty+(game.layout.width*math.sin(self.theta3)))
                
                self.ins.add(Line (circle = (self.tx, self.ty, self.rad), width = 1))
                self.ins.add(Line (points=[pt1[0],pt1[1],ed1[0],ed1[1]],width=1))
                self.ins.add(Line (points=[pt2[0],pt2[1],ed2[0],ed2[1]],width=1))
                self.ins.add(Line (points=[pt3[0],pt3[1],ed3[0],ed3[1]],width=1))
                self.canvas.add(self.ins) 
                self.once = False
            else:
                self.canvas.remove(self.ins)
                self.rad -= 20
                self.ins = InstructionGroup()
                self.ins.add(Color (0.365, 0.678, 0.886, .8))

                pt1 = (self.tx+self.rad*math.cos(self.theta1), self.ty+(self.rad*math.sin(self.theta1)))
                pt2 = (self.tx+self.rad*math.cos(self.theta2), self.ty+(self.rad*math.sin(self.theta2)))
                pt3 = (self.tx+self.rad*math.cos(self.theta3), self.ty+(self.rad*math.sin(self.theta3)))

                ed1 = (self.tx+game.layout.width*math.cos(self.theta1), self.ty+(game.layout.width*math.sin(self.theta1)))
                ed2 = (self.tx+game.layout.width*math.cos(self.theta2), self.ty+(game.layout.width*math.sin(self.theta2)))
                ed3 = (self.tx+game.layout.width*math.cos(self.theta3), self.ty+(game.layout.width*math.sin(self.theta3)))
                
                self.ins.add(Line (circle = (self.tx, self.ty, self.rad), width = 1))
                self.ins.add(Line (points=[pt1[0],pt1[1],ed1[0],ed1[1]],width=1))
                self.ins.add(Line (points=[pt2[0],pt2[1],ed2[0],ed2[1]],width=1))
                self.ins.add(Line (points=[pt3[0],pt3[1],ed3[0],ed3[1]],width=1))
                
                self.canvas.add(self.ins) 
              
class Background(Widget):
    def __init__(self,  **kwargs):
        super (Background, self).__init__(**kwargs)
        self.image = Sprite(source='space.jpeg')
        self.add_widget(self.image)
    

class Missile (Widget):
    def __init__(self, relsize , position , **kwargs):
        super (Missile, self).__init__(**kwargs)
        self.image = Sprite(source='missile.png')
        self.size = relsize
        self.image.size = self.size
        self.image.center = position
        self.pos = position
        self.hit = False
        
        self.add_widget(self.image)
    def move(self):
        if self.image.width >= 0.25*game.layout.width:
            self.hit = True
            game.over()
            game.running=False
        else:
            self.image.size = [self.image.width+game.speed,self.image.height+game.speed]
            self.image.center = self.pos
    def explode(self):
        position = self.pos
        size = self.image.size
        game.layout.add_widget(Explosion(size, position))
        
class Explosion(Widget):
    def __init__(self, size, position,  **kwargs):
        super (Explosion, self).__init__(**kwargs)
        self.image = Sprite(source='explosion.png')
        self.image.size = size
        self.image.center = position
        self.add_widget(self.image)
        Clock.schedule_once(self.erase,0.25)
    def erase(self,dt):
        self.remove_widget(self.image)
        game.remove_widget(self)



store = JsonStore('user.json')

sound = SoundLoader.load('sound.wav')

LabelBase.register(name="font",fn_regular= "Exo2-RegularExpanded.otf")

game = Game()        
second = True
third = True
fourth = True
fifth = True
speedFlag1m = True
speedFlag2m = True
speedFlag3m = True
speedFlag4m = True
speedFlag5m = True
speedFlag3 = True
speedFlag4 = True


#data_dir = getattr(self, 'user_data_dir') #get a writable path to save the file


    

class GameApp(App):
    def build (self):        
        return game


if __name__ == "__main__":
    GameApp().run()
    
