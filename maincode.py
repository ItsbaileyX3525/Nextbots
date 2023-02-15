"""
View my website at https://baileyswebsite.ddns.net/Home
Discord server: https://discord.gg/e8fKE7xAKz

Update log:
Nextbots V8:
- Added difficulties to the game
- Fixed a bug where Armstrong texture wouldnt work if phonk hadn't spawned yet
- Fixed the bug where sound would play of the nextbot for a split second at beginning
Known bugs:
- Player animations dont work if you hold down 'w' and then hold down 's' and release 's' it'll keep you idle does this with every combination
- Jumpscare bg are transparent (still cba making them not rn)

Notes:
If you can't hear the music you have the copyright-free version and you can find the songs you need in the songs.txt file
"""


from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
import random as ra
from direct.actor.Actor import Actor
from pandac.PandaModules import TransparencyAttrib
from ursina.prefabs.health_bar import HealthBar
from panda3d.core import Texture
from direct.interval.IntervalGlobal import LerpHprInterval, ActorInterval

window.title="Nextbots"

window.fullscreen=False
window.borderless=False
window.icon="assets/misc/papyrus.ico"





"""Character"""





class Character(Entity): # Player model, attaches to the Harlod (FPC)
    def __init__(self):
        super().__init__()
        self.actor=Actor("player.glb")
        self.actor.reparentTo(Harlod)
        self.actor.setScale(0.018)
        self.actor.setHpr(180,0,0)
        x,y,z=self.actor.getPos()
        self.actor.setPos(x,.9,1)
        self.idle=ActorInterval(self.actor, "idle")
        self.run=ActorInterval(self.actor, "run")
        self.runbackward=ActorInterval(self.actor, "run backwards")
        self.walk=ActorInterval(self.actor, "walk")
        self.walkbackward=ActorInterval(self.actor, "walk backwards")
        self.straferight=ActorInterval(self.actor, "strafe right")
        self.strafeleft=ActorInterval(self.actor, "strafe left")
        self.idle.loop()
        self.actor.ls()
    def input(self, key):
        if key == 'w' and not held_keys['shift']:
            self.walk.loop()
        elif key == 'w' and  held_keys['shift']:
            self.run.loop()
        elif held_keys['w'] and key=='shift':
            self.run.loop()
        elif key == 's' and not held_keys['shift']:
            self.walkbackward.loop()
        elif key=='s'  and held_keys['shift']:
            self.runbackward.loop()
        elif held_keys['s'] and key=='shift':
            self.runbackward.loop()
        elif key == 'a':
            self.strafeleft.loop()
        elif key == 'd':
            self.straferight.loop()
        elif key == 'd up':
            self.idle.loop()
        elif key == 'a up':
            self.idle.loop()
        elif key == 's up':
            self.idle.loop()
        elif key == 'w up':
            self.idle.loop()
        elif key=='shift up' and held_keys['w']:
            self.walk.loop()
        elif key=='shift up' and held_keys['s']:
            self.walkbackward.loop()




"""Character"""




class Nextbot(Entity): #Nextbot class for creating new nextbots
    def __init__(self, texture, chase_sound, death_sound, death_texture,chase_speed,wonder_speed, **kwargs):
        super().__init__(parent=sus, model='quad', texture=texture, scale_y=3,scale_x=3, collider='box', y=2, double_sided=True, **kwargs)
        self.chase_sound = chase_sound
        self.speed=chase_speed
        self.speed2=wonder_speed
        self.death_sound = death
        self.killed_sound = death_sound
        self.death_texture = death_texture
        self.move=None
        self.in_range=None
        self.dist=0
        self.max_distance = 30 #How far away audio plays from the nextbot
        self.Nextbot_rotate()
        self.chase_sound.volume=0
        self.chase_sound.play()

    def update(self):
        self.dist = distance(Harlod.position, self.position)
        volume = max(1 - self.dist / self.max_distance, 0)
        self.chase_sound.volume = volume
        if self.dist > 1.2 and self.dist < 18:
            self.move=False
            self.in_range=True
            self.look_at_2d(Harlod.position, 'y')
            self.position += self.forward * time.dt * self.speed
        elif self.dist < 1.2:
            if not self.killed_sound.playing:
                global nomove
                self.killed_sound.play()
                PhonkDeath = Entity(model='quad', texture=self.death_texture, parent=camera.ui, scale_x=2)
                nomove = True
                Harlod.y = 70
                obungaafterscarexpos = Harlod.x - 20
                self.x = obungaafterscarexpos
                def playerdeath():
                    global playerdeath, deathL
                    destroy(PhonkDeath)
                    self.death_sound.play()
                    editor_camera.enabled = True
                    respawn_screen()
                    deathL = editor_camera.add_script(SmoothFollow(target=Harlod, offset=(0,2,-10)))
                    playerdeath = True
                invoke(playerdeath, delay=2)
        if self.dist > 18:
            self.in_range=False
        if self.move:
            self.position += self.forward * time.dt * self.speed2
    def Nextbot_move(self):
        if self.dist > 18:
            self.move=True
        invoke(self.Nextbot_rotate, delay=ra.uniform(1,3))

    def Nextbot_rotate(self):
        self.move=False
        delay = ra.uniform(1, 3)
        if self.dist > 18:
            if not self.in_range:
                rotate_interval = LerpHprInterval(self, delay, (ra.uniform(0,260),0,0))
                rotate_interval.start()
        invoke(self.Nextbot_move, delay=delay)



app=Ursina()


editor_camera = EditorCamera(enabled=False)
sus=Entity()


health_bar_1 = HealthBar(bar_color=color.yellow, roundness=.5,value=100,z=100)
health_bar_2 = HealthBar(bar_color=color.red, roundness=.5,value=100,y=-66,x=-.8,z=100,scale=(.3,.015),show_text=False)
health_bar_1.animation_duration = 0
health_bar_2.animation_duration = 0

HardmodeEnabled=False
EasymodeEnabled=True
PeacefulmodeEnabled=False
GenerativemodeEnabled=False

def Peacefulmode():
    global EasymodeEnabled,HardmodeEnabled,PeacefulmodeEnabled,GenerativemodeEnabled
    if PeacefulmodeEnabled:
        PeacefulmodeEnabled=False
        Peaceful.text='Peaceful mode off'
    else:
        EasymodeEnabled=False
        PeacefulmodeEnabled=True
        GenerativemodeEnabled=False
        HardmodeEnabled=False
        Hard.text='Hard mode off'
        Easy.text='Easy mode off'
        Generative.text='Special mode off'
        Peaceful.text='Peaceful mode on'
def Easymode():
    global EasymodeEnabled,HardmodeEnabled,PeacefulmodeEnabled,GenerativemodeEnabled
    if EasymodeEnabled:
        EasymodeEnabled=False
        Easy.text='Easy mode off'
    else:
        EasymodeEnabled=True
        PeacefulmodeEnabled=False
        GenerativemodeEnabled=False
        HardmodeEnabled=False
        Hard.text='Hard mode off'
        Easy.text='Easy mode on'
        Generative.text='Special mode off'
        Peaceful.text='Peaceful mode off'
def Hardmode():
    global EasymodeEnabled,HardmodeEnabled,PeacefulmodeEnabled,GenerativemodeEnabled
    if HardmodeEnabled:
        HardmodeEnabled=False
        Hard.text='Hard mode off'
    else:
        EasymodeEnabled=False
        PeacefulmodeEnabled=False
        GenerativemodeEnabled=False
        HardmodeEnabled=True
        Hard.text='Hard mode on'
        Easy.text='Easy mode off'
        Generative.text='Special mode off'
        Peaceful.text='Peaceful mode off'
def Generatemode():
    global EasymodeEnabled,HardmodeEnabled,PeacefulmodeEnabled,GenerativemodeEnabled
    if GenerativemodeEnabled:
        GenerativemodeEnabled=False
        Hard.text='Special mode off'
    else:
        EasymodeEnabled=False
        PeacefulmodeEnabled=False
        GenerativemodeEnabled=True
        HardmodeEnabled=False
        Hard.text='Hard mode off'
        Easy.text='Easy mode off'
        Generative.text='Special mode on'
        Peaceful.text='Peaceful mode off'

Peaceful=Button(text='Peaceful mode off',y=-.3,scale_y=.1,scale_x=.2,x=-.5,on_click=Peacefulmode)
Easy=Button(text='Easy mode on',y=-.3,scale_y=.1,scale_x=.2,x=.5,on_click=Easymode)
Hard=Button(text='Hard mode off',y=-.3,scale_y=.1,scale_x=.2,on_click=Hardmode)
Generative=Button(text='Special mode off',y=.4,scale_y=.1,scale_x=.2,on_click=Generatemode)
ObungaNextbot=None
PhonkNextbot=None
TycreatureNextbot=None
AndrewNextbot=None
AngymunciNextbot=None
ArmstrongNextbot=None
def game_begin():
    global EasymodeEnabled,HardmodeEnabled,PeacefulmodeEnabled,GenerativemodeEnabled,load_bg,start,health_bar_2,health_bar_1,nextbot1_1,nextbot1_2,nextbot1_3,nextbot1_4,nextbot1_5,nextbot1_6,PhonkNextbot,ArmstrongNextbot,ArmstrongNextbot,ObungaNextbot,TycreatureNextbot,AndrewNextbot,AngymunciNextbot
    if not EasymodeEnabled and not HardmodeEnabled and not PeacefulmodeEnabled and not GenerativemodeEnabled:
        EasymodeEnabled=True
    Harlod.speed=8
    ButtonClick.play()
    load_bg.enabled=False
    Hard.disabled=False
    Hard.visible=False
    Easy.disabled=False
    Easy.visible=False
    Generative.disabled=False
    Generative.visible=False
    Peaceful.disabled=False
    Peaceful.visible=False
    start.disabled=True
    start.visible=False
    mouse.locked=True
    health_bar_2.z=0
    health_bar_1.z=0
    #Nextbot setup
    nextbot1_1=False
    nextbot1_2=False
    nextbot1_3=False
    nextbot1_4=False
    nextbot1_5=False
    nextbot1_6=False
    if HardmodeEnabled:
        PhonkNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=death, death_texture='assets/textures/phonk.gif',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        ObungaNextbot=Nextbot(texture='assets/textures/obunga.png', chase_sound=obungachase, death_sound=death, death_texture='assets/textures/obunga.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        TycreatureNextbot=Nextbot(texture='assets/textures/saddydaddy.png', chase_sound=AutismCreatureChase, death_sound=Yippedeath, death_texture='assets/textures/saddydaddy.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        AndrewNextbot=Nextbot(texture='assets/textures/andrew.png', chase_sound=tateyChase, death_sound=death, death_texture='assets/textures/andrew.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        AngymunciNextbot=Nextbot(texture='assets/textures/angy munci.png', chase_sound=muncichase, death_sound=death, death_texture='assets/textures/angy munci.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        ArmstrongNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=armstrongchase, death_sound=death, death_texture='assets/textures/armstrong.gif',chase_speed=14,wonder_speed=10,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    elif PeacefulmodeEnabled:
        pass
    elif EasymodeEnabled:
        num1=ra.randint(1,3)
        num2=ra.randint(1,3)
        if num1==1:
            PhonkNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=death, death_texture='assets/textures/phonk.gif',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        elif num1==2:
            ObungaNextbot=Nextbot(texture='assets/textures/obunga.png', chase_sound=obungachase, death_sound=death, death_texture='assets/textures/obunga.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        elif num1==3:
            TycreatureNextbot=Nextbot(texture='assets/textures/saddydaddy.png', chase_sound=AutismCreatureChase, death_sound=Yippedeath, death_texture='assets/textures/saddydaddy.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        if num2==1:
            AndrewNextbot=Nextbot(texture='assets/textures/andrew.png', chase_sound=tateyChase, death_sound=death, death_texture='assets/textures/andrew.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        elif num2==2:
            AngymunciNextbot=Nextbot(texture='assets/textures/angy munci.png', chase_sound=muncichase, death_sound=death, death_texture='assets/textures/angy munci.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        elif num2==3:
            ArmstrongNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=armstrongchase, death_sound=death, death_texture='assets/textures/armstrong.gif',chase_speed=14,wonder_speed=10,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    elif GenerativemodeEnabled:
        Entity(update=specialmode)
        ObungaNextbot=Nextbot(texture='assets/textures/obunga.png', chase_sound=obungachase, death_sound=death, death_texture='assets/textures/obunga.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
timer=0

def specialmode():
    global timer,PhonkNextbot,ArmstrongNextbot,ArmstrongNextbot,ObungaNextbot,TycreatureNextbot,AndrewNextbot,AngymunciNextbot
    timer+=time.dt
    if timer>=10:
        if PhonkNextbot==None:
            PhonkNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=death, death_texture='assets/textures/phonk.gif',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if timer>=20:
        if TycreatureNextbot==None:
            TycreatureNextbot=Nextbot(texture='assets/textures/saddydaddy.png', chase_sound=AutismCreatureChase, death_sound=Yippedeath, death_texture='assets/textures/saddydaddy.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if timer>=30:
        if AndrewNextbot==None:
            AndrewNextbot=Nextbot(texture='assets/textures/andrew.png', chase_sound=tateyChase, death_sound=death, death_texture='assets/textures/andrew.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if timer>=40:
        if ArmstrongNextbot==None:
            ArmstrongNextbot=Nextbot(texture='assets/textures/phonk.png', chase_sound=armstrongchase, death_sound=death, death_texture='assets/textures/armstrong.gif',chase_speed=14,wonder_speed=10,x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if timer>=50:
        if AngymunciNextbot==None:
            AngymunciNextbot=Nextbot(texture='assets/textures/angy munci.png', chase_sound=muncichase, death_sound=death, death_texture='assets/textures/angy munci.png',chase_speed=10,wonder_speed=8,x=ra.uniform(-80,80),z=ra.uniform(-80,80))

armstrong_texture = Animation('assets/textures/armstrong.gif',y=-4)
armstrong_texture1 = Animation('assets/textures/armstrong.gif',y=-4)
phonk_texture = Animation('assets/textures/phonk.gif',y=-4)
phonk_texture1 = Animation('assets/textures/phonk.gif',y=-4)
def gif_applier(): #Makes the double-sided gif work for the nextbots
    global ArmstrongNextbot,PhonkNextbot
    try:
        phonk_texture.position = PhonkNextbot.position
        phonk_texture.scale = PhonkNextbot.scale
        phonk_texture.rotation=PhonkNextbot.rotation
        phonk_texture1.position = PhonkNextbot.position
        phonk_texture1.scale = PhonkNextbot.scale
        phonk_texture1.rotation_y=PhonkNextbot.rotation_y - 180
    except Exception:
        pass
    try:
        armstrong_texture.position = ArmstrongNextbot.position
        armstrong_texture.scale = ArmstrongNextbot.scale
        armstrong_texture.rotation=ArmstrongNextbot.rotation
        armstrong_texture1.position = Vec3(ArmstrongNextbot.position)
        armstrong_texture1.scale = ArmstrongNextbot.scale
        armstrong_texture1.rotation_y=ArmstrongNextbot.rotation_y + 180   
    except Exception:
        pass
Entity(update=gif_applier)
#Audios
Yippedeath=Audio('assets/audio/bong',loop=False,autoplay=False)
armstrongchase=Audio('assets/audio/armstrong',loop=True,autoplay=False)
muncichase=Audio('assets/audio/vacent1',loop=True,autoplay=False,volume=.8)
obungachase=Audio('assets/audio/prowler',autoplay=False,loop=True)
sanschase=Audio('assets/audio/megalovania',autoplay=False,loop=True)
PhonkChase=Audio('assets/audio/Phonk',autoplay=False,loop=True)
tateyChase=Audio('assets/audio/tate2',autoplay=False,loop=True)
AutismCreatureChase=Audio('assets/audio/saddyclose',autoplay=False,loop=True)
death=Audio('assets/audio/death',autoplay=False,loop=False,volume=2)
jumpscare=Audio('assets/audio/jumpscare',autoplay=False,loop=False)

ButtonClick=Audio('assets/audio/button-click',autoplay=False,loop=False)


#main menu
load_bg=Entity(parent=camera.ui,model='quad',color=color.black,scale=(100,100))
start=Button(text='Start game',disabled=False,scale=(.2,.1),z=-100,text_color=color.black,color=color.white,visible=True)
start.on_click=game_begin
window.color = color.white


Audio('welcome')
playerdeath=False

from fur_shader import Fur
#CakedGround = Entity(model="cube",collider='box', color=color.white, texture="grass",scale=(1000,0.1,1000),texture_scale=(31.6227766017,1,31.6227766017))
ground = Entity(model='plane', scale=1000, texture='grass', texture_scale=(31.6227766017,31.6227766017), collider='box')
#grass = Fur(entity=cube, scale=30000, layers=3, layerSize=0.005, shadow=20)

window.exit_button.visible=False
window.fps_counter.enabled=True

#Harlod/player stuff
Harlod=FirstPersonController()
HarlodModel=Character()
mouse.locked=False
Harlod.walkSpeed=6
Harlod.runSpeed=17
Harlod.jogSpeed=12
healthtext=Text(text=f'{health_bar_2.value}/{health_bar_2.max_value}',x=-.5,y=-.4)
healthtext1=Text(text='Health:',x=-.8,y=-.4)
healthbox=Entity(alpha=.5,color=color.yellow)

def healthupdate():
    healthtext.text=f'{health_bar_2.value}/{health_bar_2.max_value}'
Entity(update=healthupdate)
    
#crorbar innit
Crowbar1=Actor("crowbar.glb")
Crowbar1.reparentTo(camera)
Crowbar1.setScale(0.04)
Crowbar1.setHpr(20,0,0)
Crowbar1.setPos(.35,-.5,.8)
Crowbar1.loop("swing")


nomove=False
respawn=False
button=Button(icon=False,text='Respawn?',highlightcolor=color.orange,scale=(0.25,0.1),color=color.rgb(0,0,150),text_color=color.black,y=.2,disabled=True,visible=False)
button2=Button(icon=False,text="Rage quit?",scale=(0.5,0.1),text_color=color.black,color=color.rgb(0,0,150),y=-.2,disabled=True,visible=False)
def respawn_screen():
    global respawn,deathL,nomove
    respawn=True
    if respawn:
        button.visible=True
        button.disabled=False
        button2.visible=True
        button2.disabled=False
        Harlod.speed=0
        Harlod.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        def action():
            global nomove,Nextbotted1
            ButtonClick.play()
            editor_camera.enabled = not editor_camera.enabled
            Harlod.cursor.enabled = not editor_camera.enabled
            mouse.locked = not editor_camera.enabled
            editor_camera.scripts.remove(deathL)
            Harlod.x=ra.uniform(0,50)
            nomove=False
            Crowbar1.clearTransparency()
            button.visible=False
            button.disabled=True
            button2.visible=False
            button2.disabled=True
            Harlodypos=Harlod.y + .3
            Harlod.y=Harlodypos
        def quit():
            application.quit()
        button.on_click=action
        button2.on_click=quit
        respawn=False


playerdeath=False

Sky()


def input(key):
    if key=='f12':
        if window.fullscreen:
            window.fullscreen=False
        else:
            window.fullscreen=True
seq1=False

health_regen_timer = 0

def update():
    global playerdeath, seq1, health_regen_timer,respawn,Nextbotted1
    round(health_bar_1.value, 1)
    if playerdeath == True:
        if not seq1:
            Crowbar1.setTransparency(TransparencyAttrib.M_alpha)
            seq1 = True
            Harlod.position-=Harlod.forward
        if Harlod.y==1:
            playerdeath = False
            Harlod.position=2
    if held_keys['shift'] and held_keys['w'] and not nomove and not held_keys['s']:
        if health_bar_1.value == 0:
            Harlod.speed = Harlod.walkSpeed
        else:
            Harlod.speed = Harlod.runSpeed
            health_bar_1.value -= 0.25
            health_regen_timer = 0
    elif held_keys['shift'] and held_keys['s'] and not nomove and not held_keys['w']:
        if health_bar_1.value == 0:
            Harlod.speed = Harlod.walkSpeed
        else:
            Harlod.speed = Harlod.jogSpeed
            health_bar_1.value -= 0.25
            health_regen_timer = 0
    elif health_regen_timer >= 2:
        if health_bar_1.value < 100 and not nomove:
            health_bar_1.value += time.dt  * 10
            Harlod.speed = Harlod.walkSpeed
    else:
        Harlod.speed = Harlod.walkSpeed
        health_regen_timer += time.dt
    if nomove:
        Harlod.speed = 0



app.run()