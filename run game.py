"""
View my website at https://baileyswebsite.ddns.net/
Discord server: https://discord.gg/BPBrF37dBY

Update log:
Nextbots V11:
- Just redone everything, much cleaner and actually is code now instead of just an pile of shite

Known bugs:

- THERE NO ARE KNOWN BUGS :) - report any bugs to my discord server!

"""


from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
import random as ra
from panda3d.core import Loader
from direct.interval.IntervalGlobal import LerpHprInterval
from direct.actor.Actor import Actor
from ursina.prefabs.health_bar import HealthBar
import threading

class UI():
    def __init__(self):
        self.HardmodeEnabled=False
        self.EasymodeEnabled=False
        self.PeacefulmodeEnabled=False
        self.GenerativemodeEnabled=True
        
        self.load_bg=Entity(parent=camera.ui,model='quad',color=color.gray,scale=(100,100))
                
        self.start=Button(radius=.3,text='Start game',disabled=False,scale=(.2,.1),z=-100,text_color=color.black,color=color.white,visible=True,on_click=self.start_game)
        self.Respawn=Button(radius=.3,text='Respawn?',highlightcolor=color.orange,scale=(0.25,0.1),color=color.rgb(0,0,150),text_color=color.black,y=.2,enabled=False,on_click=self.RespawnPlayer)
        self.Quit=Button(radius=.3,text="Rage quit?",scale=(0.5,0.1),text_color=color.black,color=color.rgb(0,0,150),y=-.2,enabled=False,on_click=application.quit)
        self.Peaceful=Button(radius=.3,text='Peaceful mode off',y=-.3,scale_y=.1,scale_x=.2,x=-.5,on_click=self.Peacefulmode)
        self.Easy=Button(radius=.3,text='Easy mode off',y=-.3,scale_y=.1,scale_x=.2,x=.5,on_click=self.Easymode)
        self.Hard=Button(radius=.3,text='Hard mode off',y=-.3,scale_y=.1,scale_x=.2,on_click=self.Hardmode)
        self.Generative=Button(radius=.3,text='Special mode on',y=.4,scale_y=.1,scale_x=.2,on_click=self.Generatemode)
        self.BeginMenu = [self.start,self.Peaceful,self.Easy,self.Hard,self.Generative,self.load_bg]

        self.StaminaBar = HealthBar(enabled=False,bar_color=color.yellow, roundness=.5,value=1000,z=100,animation_duration = 0,max_value=1000)
        self.StaminaBar.text_entity.color = color.black
        
        self.NextbotDeathTextures = []
    def start_game(self):
        global GROUND,Harlod,HarlodCharacter
        GROUND = Entity(model='plane', scale=1000, texture='grass', texture_scale=(100,100), collider='box')
        Harlod=FirstPersonController()
        HarlodCharacter = Character()
        NextbotCreation()
        self.StaminaBar.enabled=True
        for e in self.BeginMenu:
            destroy(e)
            
    def RespawnPlayer(self):
        application.paused = False
        Harlod.position = (ra.uniform(-100,100), 3, ra.uniform(-100,100))
        mouse.locked=True
        self.Respawn.enabled=False
        self.Quit.enabled=False
        for e in self.NextbotDeathTextures:
            e.visible = False
        Sequence(Wait(2.5), Func(setattr, HarlodCharacter, "isDead", False),auto_destroy=True).start()
    
    def Peacefulmode(self):
        if self.PeacefulmodeEnabled:
            self.PeacefulmodeEnabled=False
            self.Peaceful.text='Peaceful mode off'
        else:
            self.EasymodeEnabled=False
            self.PeacefulmodeEnabled=True
            self.GenerativemodeEnabled=False
            self.HardmodeEnabled=False
            self.Hard.text='Hard mode off'
            self.Easy.text='Easy mode off'
            self.Generative.text='Special mode off'
            self.Peaceful.text='Peaceful mode on'
    def Easymode(self):
        if self.EasymodeEnabled:
            self.EasymodeEnabled=False
            self.Easy.text='Easy mode off'
        else:
            self.EasymodeEnabled=True
            self.PeacefulmodeEnabled=False
            self.GenerativemodeEnabled=False
            self.HardmodeEnabled=False
            self.Hard.text='Hard mode off'
            self.Easy.text='Easy mode on'
            self.Generative.text='Special mode off'
            self.Peaceful.text='Peaceful mode off'
    def Hardmode(self):
        if self.HardmodeEnabled:
            self.HardmodeEnabled=False
            self.Hard.text='Hard mode off'
        else:
            self.EasymodeEnabled=False
            self.PeacefulmodeEnabled=False
            self.GenerativemodeEnabled=False
            self.HardmodeEnabled=True
            self.Hard.text='Hard mode on'
            self.Easy.text='Easy mode off'
            self.Generative.text='Special mode off'
            self.Peaceful.text='Peaceful mode off'
    def Generatemode(self):
        if self.GenerativemodeEnabled:
            self.GenerativemodeEnabled=False
            self.Generative.text='Special mode off'
        else:
            self.EasymodeEnabled=False
            self.PeacefulmodeEnabled=False
            self.GenerativemodeEnabled=True
            self.HardmodeEnabled=False
            self.Hard.text='Hard mode off'
            self.Easy.text='Easy mode off'
            self.Generative.text='Special mode on'
            self.Peaceful.text='Peaceful mode off'

class Nextbot(Entity):
    def __init__(self, texture, chase_sound, death_sound, death_texture, chase_speed, wonder_speed, **kwargs):
        super().__init__(parent=scene,model='quad',texture=texture,scale=(3, 3),collider='box',y=2,double_sided=True,**kwargs)
        self.chase_sound = chase_sound
        self.speed = chase_speed
        self.speed2 = wonder_speed
        self.death_sound = death_sound
        self.killed_sound = death_sound
        self.death_texture = death_texture
        self.move = None
        self.in_range = None
        self.dist = 0
        self.max_distance = 30
        self.Nextbot_rotate()
        self.chase_sound.volume = 0
        self.chase_sound.play()
        self.DeathTexture = Entity(visible=False, model='quad', texture=self.death_texture, parent=camera.ui, scale=(2, 2))
        menu.NextbotDeathTextures.append(self.DeathTexture)

    def update(self):
        self.dist = distance(Harlod.position, self.position)
        volume = max(1 - self.dist / self.max_distance, 0)
        self.chase_sound.volume = volume
        
        if 1.2 < self.dist < 18 and not HarlodCharacter.isDead:
            #Chase
            self.move = False
            self.in_range = True
            self.look_at_2d(Harlod.position, 'y')
            self.position += self.forward * time.dt * self.speed
            
        elif self.dist < 1.2 and not HarlodCharacter.isDead:
            #Death
            if not self.killed_sound.playing:
                self.killed_sound.play()
            HarlodCharacter.isDead=True
            self.DeathTexture.visible=True
            menu.Respawn.enabled=True
            menu.Quit.enabled=True
            mouse.locked=False
            application.paused=True
                
        elif self.dist > 18:
            self.in_range = False
        if self.move:
            self.position += self.forward * time.dt * self.speed2
    def Nextbot_move(self):
        if self.dist > 18:
            self.move = True
        invoke(self.Nextbot_rotate, delay=ra.uniform(1, 3))

    def Nextbot_rotate(self):
        self.move = False
        delay = ra.uniform(1, 3)
        if self.dist > 18 and not self.in_range:
            rotate_interval = LerpHprInterval(self, delay, (ra.uniform(0, 260), 0, 0))
            rotate_interval.start()
        invoke(self.Nextbot_move, delay=delay)

class Character(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jumpAmount = 1
        self.BhopTimer = 0
        self.StaminaBarRegenTimer = 0
        self.player_walkSpeed=6
        self.player_runSpeed=17
        self.isDead = False

    def update(self):
        global menu
        if any(held_keys[key] for key in ['w', 'a', 's', 'd']):
            if held_keys['shift'] and menu.StaminaBar.value > 0:
                Harlod.speed = self.player_runSpeed * self.jumpAmount
                self.StaminaBarRegenTimer = 0
                menu.StaminaBar.value -= 1
            else:
                Harlod.speed = self.player_walkSpeed
                
        if not held_keys['shift']:
            self.StaminaBarRegenTimer += time.dt
            Harlod.speed = self.player_walkSpeed
            if self.StaminaBarRegenTimer >= 3:
                menu.StaminaBar.value += 1
        
        if Harlod.grounded:
            self.BhopTimer += time.dt
        else:
            self.BhopTimer = 0
        if self.BhopTimer >= 0.2:
            self.jumpAmount = 1
    def input(self,key):
        if self.BhopTimer <= 0.19 and self.jumpAmount <= 3 and Harlod.grounded and held_keys['shift'] and menu.StaminaBar.value > 0:
            self.jumpAmount+=1
            print(Harlod.speed)

class NextbotCreation(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        threading.Thread(target=self.start_loading_animation).start()
        self.timer=0
        self.PhonkNextbot=None
        self.ArmstrongNextbot=None
        self.ObungaNextbot=None
        self.TycreatureNextbot=None
        self.AndrewNextbot=None
        self.AngymunciNextbot=None
        self.JohnNextbot=None
        if menu.HardmodeEnabled:
            self.PhonkNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=Springjumpscare, death_texture='assets/textures/phonk.gif',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            self.ObungaNextbot=Nextbot(texture='assets/textures/obunga.png', chase_sound=obungachase, death_sound=Springjumpscare, death_texture='assets/textures/obunga.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            self.TycreatureNextbot=Nextbot(texture='assets/textures/saddydaddy.png', chase_sound=AutismCreatureChase, death_sound=Yippedeath, death_texture='assets/textures/saddydaddy.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            self.AndrewNextbot=Nextbot(texture='assets/textures/andrew.png', chase_sound=tateyChase, death_sound=Springjumpscare, death_texture='assets/textures/andrew.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            self.AngymunciNextbot=Nextbot(texture='assets/textures/angy munci.png', chase_sound=muncichase, death_sound=Springjumpscare, death_texture='assets/textures/angy munci.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            self.ArmstrongNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=armstrongchase, death_sound=Springjumpscare, death_texture='assets/textures/armstrong.gif',chase_speed=14,wonder_speed=10,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        elif menu.EasymodeEnabled:
            num1=ra.randint(1,3)
            num2=ra.randint(1,3)
            if num1==1:
                self.PhonkNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=Springjumpscare, death_texture='assets/textures/phonk.gif',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            elif num1==2:
                self.ObungaNextbot=Nextbot(texture='assets/textures/obunga.png', chase_sound=obungachase, death_sound=Springjumpscare, death_texture='assets/textures/obunga.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            elif num1==3:
                self.TycreatureNextbot=Nextbot(texture='assets/textures/saddydaddy.png', chase_sound=AutismCreatureChase, death_sound=Yippedeath, death_texture='assets/textures/saddydaddy.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            if num2==1:
                self.AndrewNextbot=Nextbot(texture='assets/textures/andrew.png', chase_sound=tateyChase, death_sound=Springjumpscare, death_texture='assets/textures/andrew.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            elif num2==2:
                self.AngymunciNextbot=Nextbot(texture='assets/textures/angy munci.png', chase_sound=muncichase, death_sound=Springjumpscare, death_texture='assets/textures/angy munci.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            elif num2==3:
                self.ArmstrongNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=armstrongchase, death_sound=Springjumpscare, death_texture='assets/textures/armstrong.gif',chase_speed=14,wonder_speed=10,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        elif menu.PeacefulmodeEnabled:
            pass
    def SpecialMode(self):
        self.timer+=time.dt
        if self.timer>=10:
            if self.PhonkNextbot==None:
                self.PhonkNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=Springjumpscare, death_texture='assets/textures/phonk.gif',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        if self.timer>=20:
            if self.TycreatureNextbot==None:
                self.TycreatureNextbot=Nextbot(texture='assets/textures/saddydaddy.png', chase_sound=AutismCreatureChase, death_sound=Yippedeath, death_texture='assets/textures/saddydaddy.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        if self.timer>=30:
            if self.AndrewNextbot==None:
                self.AndrewNextbot=Nextbot(texture='assets/textures/andrew.png', chase_sound=tateyChase, death_sound=Springjumpscare, death_texture='assets/textures/andrew.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        if self.timer>=40:
            if self.ArmstrongNextbot==None:
                self.ArmstrongNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=armstrongchase, death_sound=Springjumpscare, death_texture='assets/textures/armstrong.gif',chase_speed=14,wonder_speed=10,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        if self.timer>=50:
            if self.AngymunciNextbot==None:
                self.AngymunciNextbot=Nextbot(texture='assets/textures/angy munci.png', chase_sound=muncichase, death_sound=Springjumpscare, death_texture='assets/textures/angy munci.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        if self.timer>=80:
            if self.JohnNextbot==None:
                camera.shake(duration=3,magnitude=5)
                johnspawned=Text(text='JOHN HAS BEEN SPAWNED RUN FOR YOUR LIFE',x=-.3,y=.3)
                destroy(johnspawned,delay=2)
                self.JohnNextbot=Nextbot(texture='assets/textures/john.png', chase_sound=muncichase, death_sound=Springjumpscare, death_texture='assets/textures/john.png',chase_speed=16,wonder_speed=12,x=ra.uniform(-80,80),z=ra.uniform(-80,80),scale=5)

    def start_loading_animation(self):
        self.armstrong_texture=Animation('assets/textures/armstrong.gif',y=-4)
        self.armstrong_texture1=Animation('assets/textures/armstrong.gif',y=-4)
        self.phonk_texture=Animation('assets/textures/phonk.gif',y=-4)
        self.phonk_texture1=Animation('assets/textures/phonk.gif',y=-4)
        
    def gif_applier(self):
        try:
            self.phonk_texture.position = self.PhonkNextbot.position
            self.phonk_texture.scale = self.PhonkNextbot.scale
            self.phonk_texture.rotation = self.PhonkNextbot.rotation
            self.phonk_texture1.position = self.PhonkNextbot.position
            self.phonk_texture1.scale = self.PhonkNextbot.scale
            self.phonk_texture1.rotation_y = self.PhonkNextbot.rotation_y - 180

            self.armstrong_texture.position = self.ArmstrongNextbot.position
            self.armstrong_texture.scale = self.ArmstrongNextbot.scale
            self.armstrong_texture.rotation = self.ArmstrongNextbot.rotation
            self.armstrong_texture1.position = Vec3(self.ArmstrongNextbot.position)
            self.armstrong_texture1.scale = self.ArmstrongNextbot.scale
            self.armstrong_texture1.rotation_y = self.ArmstrongNextbot.rotation_y + 180
        except:
            pass
    
    def update(self):
        self.gif_applier()
        self.SpecialMode()
        
        
#PhonkNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=jumpscare, death_texture='assets/textures/phonk.gif',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
window.title="Nextbots"
window.fullscreen=False
window.icon="assets/misc/papyrus.ico"
app=Ursina(borderless=False)
window.exit_button.visible=False
window.fps_counter.enabled=True
window.color = color.white

menu = UI()
def load_sky():
    Sky()
threading.Thread(target=load_sky).start()
# Variables
ObungaNextbot=None
PhonkNextbot=None
JohnNextbot=None
TycreatureNextbot=None
AndrewNextbot=None
AngymunciNextbot=None
ArmstrongNextbot=None
playerdeath=False

#Audio
tateyChase=Audio("assets/audio/tate2.ogg",autoplay=False,loop=True)
Yippedeath=Audio("assets/audio/bong.ogg",autoplay=False,loop=True)
armstrongchase=Audio("assets/audio/armstrong.ogg",autoplay=False,loop=True)
muncichase=Audio("assets/audio/vacent1.wav",autoplay=False,loop=True,volume=0.8)
obungachase=Audio("assets/audio/prowler.ogg",autoplay=False,loop=True)
sanschase=Audio("assets/audio/megalovania.ogg",autoplay=False,loop=True)
PhonkChase=Audio("assets/audio/Phonk.ogg",autoplay=False,loop=True)
AutismCreatureChase=Audio("assets/audio/saddyclose.ogg",autoplay=False,loop=True)
death=Audio("assets/audio/death.ogg",autoplay=False,loop=False,volume=2)
Springjumpscare=Audio("assets/audio/jumpscare.ogg",autoplay=False,loop=False)
ButtonClick=Audio("assets/audio/button-click.ogg",autoplay=False,loop=False)
app.run()