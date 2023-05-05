"""
View my website at https://baileyswebsite.ddns.net/Home
Discord server: https://discord.gg/e8fKE7xAKz

Update log:
Nextbots V10:
- Removed my own class so its accessible with any ursina.
- Created "Nextbot_creation.py" so you can easily build a nextbot class.
- Added the option to add custom nextbots to the game (Only allows one at the moment).
- Cleaned up the entire code so its less messy.
- General other fixes to the game.
- Enjoy.

Known bugs:

- THERE NO ARE KNOWN BUGS :) - report any bugs to my discord server!

"""


from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
import random as ra
from panda3d.core import Loader
from direct.interval.IntervalGlobal import LerpHprInterval
from direct.interval.ActorInterval import LerpAnimInterval
from direct.actor.Actor import Actor
from ursina.prefabs.health_bar import HealthBar


LoadingText=Text(text='Loading assets',enabled=False,x=-.7,y=.45)


window.title="Nextbots"
window.fullscreen=False
window.icon="assets/misc/papyrus.ico"
app=Ursina(borderless=False)
window.exit_button.visible=False
window.fps_counter.enabled=True
window.color = color.white

with open("classes.load", "r") as f:
    exec(f.read())

with open("functions.load", "r") as f:
    exec(f.read())

with open("nextbots.load", "r") as f:
    exec(f.read())

with open("anim_nextbots.load", "r") as f:
    exec(f.read())

with open("audios.load", "r") as f:
    exec(f.read())

# Variables
seq1=False
health_regen_timer = 0
ObungaNextbot=None
PhonkNextbot=None
JohnNextbot=None
TycreatureNextbot=None
AndrewNextbot=None
AngymunciNextbot=None
ArmstrongNextbot=None
HardmodeEnabled=False
EasymodeEnabled=False
PeacefulmodeEnabled=False
GenerativemodeEnabled=True
timer=0
playerdeath=False
player_walkSpeed=6
player_runSpeed=17
player_jogSpeed=12
respawn=False
jump = 1
NextbotCustom1=''
GROUNDLEVEL = 1.0000001192092896
BhopTimer = 0

#Game stuff
app.taskMgr.add(LoadModel(model="player.glb",name="Player", actor=False))
editor_camera = EditorCamera(enabled=False)
sus=Entity()

#Health bars
health_bar_1 = HealthBar(bar_color=color.yellow, roundness=.5,value=100,z=100,animation_duration = 0)
health_bar_2 = HealthBar(bar_color=color.red, roundness=.5,value=100,y=-66,x=-.8,z=100,scale=(.3,.015),show_text=False,animation_duration = 0)

def Apply_Nextbot():
    global NextbotCustom
    NextbotCustom=NextbotCustom1.text

def CustomNextbot():
    if not NextbotCustom1.enabled:
        NextbotCustom1.enabled=True
    else:
        NextbotCustom1.enabled=False
    
NextbotCustom1=InputField(parent=camera.ui,y=.2,enabled=False,submit_on='enter',on_submit=Apply_Nextbot)

#main menu
load_bg=Entity(parent=camera.ui,model='quad',color=color.gray,scale=(100,100))
start=Button(text='Start game',disabled=False,scale=(.2,.1),z=-100,text_color=color.black,color=color.white,visible=True,on_click=game_begin)
custom_nextbot=Button(text='Upload custom nextbot',disabled=False,scale=(.2,.1),z=-100,text_color=color.white,visible=True,on_click=CustomNextbot,x=.4)
custom_nextbot.fit_to_text()


ground = Entity(model='plane', scale=1000, texture='grass', texture_scale=(100,100), collider='box')

#Harlod/player stuff
Harlod=FirstPersonController()
mouse.locked=False

healthtext=Text(text=f'{health_bar_2.value}/{health_bar_2.max_value}',x=-.5,y=-.4)
healthtext1=Text(text='Health:',x=-.8,y=-.4)
healthbox=Entity(alpha=.5,color=color.yellow)


#crorbar innit
Crowbar1=Actor("crowbar.glb")
Crowbar1.reparentTo(camera)
Crowbar1.setScale(0.04)
Crowbar1.setHpr(20,0,0)
Crowbar1.setPos(.35,-.5,.8)
Crowbar1.loop("swing")


button=Button(icon=False,text='Respawn?',highlightcolor=color.orange,scale=(0.25,0.1),color=color.rgb(0,0,150),text_color=color.black,y=.2,disabled=True,visible=False)
button2=Button(icon=False,text="Rage quit?",scale=(0.5,0.1),text_color=color.black,color=color.rgb(0,0,150),y=-.2,disabled=True,visible=False)



def input(key):
    global jump
    if key=='f12':
        if window.fullscreen:
            window.fullscreen=False
        else:
            window.fullscreen=True
    if key == 'space' and BhopTimer <= 0.49 and jump <= 3 and Harlod.grounded:
        jump+=1

def update():
    global playerdeath, seq1, health_regen_timer,respawn,BhopTimer,jump
    round(health_bar_1.value, 1)
    healthtext.text=f'{health_bar_2.value}/{health_bar_2.max_value}'
    if playerdeath == True:
        if not seq1:
            Crowbar1.setPos(.35,765675,.8)
            seq1 = True
            Harlod.position-=Harlod.forward
        if Harlod.y==1:
            playerdeath = False
            Harlod.position=2
    if Harlod.y == GROUNDLEVEL:
        BhopTimer+=time.dt
    else:
        BhopTimer = 0
    if BhopTimer >= 0.1:
        jump = 1

app.run()