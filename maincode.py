from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
import random as ra
from direct.stdpy import thread
from direct.actor.Actor import Actor
from pandac.PandaModules import TransparencyAttrib
from ursina.prefabs.health_bar import HealthBar
from panda3d.core import Texture, AnimControlCollection
from direct.interval.IntervalGlobal import LerpHprInterval

window.title="Nextbots"

window.fullscreen=False
window.borderless=False
window.icon="assets/misc/papyrus.ico"

dist = 0

class Nextbot(Entity):
    def __init__(self, texture, chase_sound, death_sound, death_texture, **kwargs):
        super().__init__(parent=sus, model='quad', texture=texture, scale_y=3,scale_x=3, collider='box', y=2, double_sided=True, **kwargs)
        self.chase_sound = chase_sound
        self.death_sound = death_sound
        self.death_texture = death_texture
        self.move=None
        self.in_range=None
        self.max_distance = 30
        self.chase_sound.play()
        self.Nextbot_rotate()


    def update(self):
        global dist
        dist = distance(Harlod.position, self.position)
        volume = max(1 - dist / self.max_distance, 0)
        self.chase_sound.volume = volume
        if dist > 1.2 and dist < 18:
            self.move=False
            self.in_range=True
            self.look_at_2d(Harlod.position, 'y')
            self.position += self.forward * time.dt * 10
        elif dist < 1.2:
            if not jumpscare.playing:
                global nomove
                jumpscare.play()
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
        if self.move:
            self.position += self.forward * time.dt * 8

    def Nextbot_move(self):
        if dist > 18:
            self.move=True
        invoke(self.Nextbot_rotate, delay=ra.uniform(1,3))

    def Nextbot_rotate(self):
        self.move=False
        delay = ra.uniform(1, 3)
        if dist > 18:
            if not self.in_range:
                rotate_interval = LerpHprInterval(self, delay, (ra.uniform(0,260),0,0))
                rotate_interval.start()
        invoke(self.Nextbot_move, delay=delay)

class LoadingWheel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.point = Entity(parent=self, model=Circle(24, mode='point', thickness=.03), color=color.light_gray, y=.75, scale=2, texture='circle')
        self.point2 = Entity(parent=self, model=Circle(12, mode='point', thickness=.03), color=color.light_gray, y=.75, scale=1, texture='circle')

        self.scale = .025
        self.text_entity = Text(world_parent=self, text='loading...', origin=(0,1.5), color=color.light_gray)
        self.y = -.25

        self.bg = Entity(parent=self, model='quad', scale_x=camera.aspect_ratio, color=color.black, z=1)
        self.bg.scale *= 400

        for key, value in kwargs.items():
            setattr(self, key ,value)


    def update(self):
        self.point.rotation_y += 5
        self.point2.rotation_y += 3


app=Ursina()

info_text = Text('''Press space to start loading textures''', origin=(0,0), color=color.white,z=-100)
loading_screen = LoadingWheel(enabled=False)
def load_textures():
    global load_bg
    textures_to_load = ['assets/textures/obunga', 'assets/textures/andrew', 'assets/textures/Sans', 'assets/textures/saddydaddy', 'assets/textures/angy munci', 'assets/textures/phonk.gif'] * 50
    bar = HealthBar(max_value=len(textures_to_load), value=0, position=(-.5,-.35,-2), scale_x=1, animation_duration=0, world_parent=loading_screen, bar_color=color.gray)
    for i, t in enumerate(textures_to_load):
        load_texture(t)
        bar.value = i+1
    # destroy(bar, delay=.01)
    loading_screen.enabled = False


loading_screen.enabled = True
info_text.enabled = False
t = time.time()

try:
    thread.start_new_thread(function=load_textures, args='')
except Exception as e:
    print('error starting thread', e)

print('---', time.time()-t)

editor_camera = EditorCamera(enabled=False)
sus=Entity()


health_bar_1 = HealthBar(bar_color=color.yellow, roundness=.5,value=100,z=100)
health_bar_2 = HealthBar(bar_color=color.red, roundness=.5,value=100,y=-66,x=-.8,z=100,scale=(.3,.015),show_text=False)
health_bar_1.animation_duration = 0
health_bar_2.animation_duration = 0

Nextbotted1=None
Nextbotted2=None
nextbot1=2
nextbot2=ra.randint(1,5)
phonk_texture=None
phonk_texture1=None

def game_begin():
    global load_bg,start,health_bar_2,health_bar_1,Nextbotted1,Nextbotted2,phonk_texture,phonk_texture1
    Harlod.speed=8
    ButtonClick.play()
    load_bg.enabled=False
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
    #nextbot3=ra.uniform(1,10) < third nextbot when theres gonna be loads more nextbots
    #Random nextbot spawner using the ra.randint from before
    if nextbot1==1:
        nextbot1_1=True
        Nextbotted1 = Nextbot(texture='assets/textures/obunga.png', chase_sound=obungachase, death_sound=death, death_texture='assets/textures/obunga.png',x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if nextbot1==2:
        nextbot1_2=True
        phonk_texture = Animation('assets/textures/phonk.gif')
        phonk_texture1 = Animation('assets/textures/phonk.gif')
        Nextbotted1 = Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=death, death_texture='assets/textures/phonk.gif',x=ra.uniform(-80,80),z=ra.uniform(-80,80))
        Entity(update=gif_applier)

    if nextbot1==3:
        nextbot1_3=True
        Nextbotted1=Nextbot(texture='assets/textures/saddydaddy.png', chase_sound=AutismCreatureChase, death_sound=death, death_texture='assets/textures/saddydaddy.png',x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if nextbot1==4:
        nextbot1_4=True
        Nextbotted1=Nextbot(texture='assets/textures/andrew.png', chase_sound=tateyChase, death_sound=death, death_texture='assets/textures/andrew.png',x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if nextbot1==5:
        nextbot1_5=True
        Nextbotted1=Nextbot(texture='assets/textures/angy munci.png', chase_sound=muncichase, death_sound=death, death_texture='assets/textures/angy munci.png',x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if nextbot2==1:
        if nextbot1_1:
            pass
        else:
            Nextbotted2 = Nextbot(texture='assets/textures/obunga.png', chase_sound=obungachase, death_sound=death, death_texture='assets/textures/obunga.png',x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    if nextbot2==2:
        if nextbot1_2:
            pass
        else:
            phonk_texture = Animation('assets/textures/phonk.gif')
            phonk_texture1 = Animation('assets/textures/phonk.gif')
            Nextbotted2 = Nextbot(texture='assets/textures/phonk.png', chase_sound=PhonkChase, death_sound=death, death_texture='assets/textures/phonk.gif',x=ra.uniform(-80,80),z=ra.uniform(-80,80))
            Entity(update=gif_applier)
    if nextbot2==3:
        if nextbot1_3:
            pass
        else:
            Nextbotted2=Nextbot(texture='assets/textures/saddydaddy.png', chase_sound=AutismCreatureChase, death_sound=death, death_texture='assets/textures/saddydaddy.png',x=ra.uniform(20,80),z=ra.uniform(20,80))
    if nextbot2==4:
        if nextbot1_4:
            pass
        else:
            Nextbotted2=Nextbot(texture='assets/textures/andrew.png', chase_sound=tateyChase, death_sound=death, death_texture='assets/textures/andrew.png',x=ra.uniform(20,80),z=ra.uniform(20,80))
    if nextbot2==5:
        if nextbot1_5:
            pass
        else:
            Nextbotted1=Nextbot(texture='assets/textures/angy munci.png', chase_sound=muncichase, death_sound=death, death_texture='assets/textures/angy munci.png',x=ra.uniform(-80,80),z=ra.uniform(-80,80))
    

def gif_applier():
    global nextbot1,nextbot2
    if nextbot1==2:
        phonk_texture.position = Nextbotted1.position
        phonk_texture.scale = Nextbotted1.scale
        phonk_texture.rotation=Nextbotted1.rotation
        phonk_texture1.position = Nextbotted1.position
        phonk_texture1.scale = Nextbotted1.scale
        phonk_texture1.rotation_y=Nextbotted1.rotation_y - 180
    elif nextbot2==2:
        phonk_texture.position = Nextbotted2.position
        phonk_texture.scale = Nextbotted2.scale
        phonk_texture.rotation=Nextbotted2.rotation
        phonk_texture1.position = Nextbotted2.position
        phonk_texture1.scale = Nextbotted2.scale
        phonk_texture1.rotation=Nextbotted2.rotation_x + 180
#Audios
muncichase=Audio('assets/audio/vacent1',loop=True,autoplay=False,volume=.8)
obungachase=Audio('assets/audio/prowler',autoplay=False,loop=True)
sanschase=Audio('assets/audio/megalovania',autoplay=False,loop=True)
yippechase=Audio('assets/audio/saddyclose',autoplay=False,loop=True)
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


ground = Entity(model='plane', scale=1000, texture='grass', texture_scale=Vec2(32), collider='box')


window.exit_button.visible=False
window.fps_counter.enabled=True

#Harlod/player stuff
Harlod=FirstPersonController(model='cube',collider='sphere', z=-10, color=color.orange,origin_y=0, speed=0)
mouse.locked=False
Harlod.walkSpeed=6
Harlod.runSpeed=17
healthtext=Text(text=f'{health_bar_2.value}/{health_bar_2.max_value}',x=-.5,y=-.4)
healthtext1=Text(text='Health:',x=-.8,y=-.4)
healthbox=Entity(alpha=.5,color=color.yellow)

def healthupdate():
    healthtext.text=f'{health_bar_2.value}/{health_bar_2.max_value}'
Entity(update=healthupdate)
    
#crorbar innit
Crowbar1=Actor("crowbar.gltf")
Crowbar1.reparentTo(camera.ui)
#Crowbar1.setScale(0.023)
Crowbar1.setScale(0.000000000000000000000000000000000000000000000023)
Crowbar1.setHpr(0,-15,0)
Crowbar1.loop("Bucko")


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
            Harlodypos=Nextbotted1.y + .3
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
    if playerdeath == True:
        if not seq1:
            Crowbar1.setTransparency(TransparencyAttrib.M_alpha)
            seq1 = True
            Harlod.position-=Harlod.forward
        if Harlod.y==Nextbotted1.y:
            playerdeath = False
            Harlod.position-=Harlod.position
    if held_keys['shift'] and held_keys['w'] and not nomove:
        if health_bar_1.value == 0:
            Harlod.speed = Harlod.walkSpeed
        else:
            Harlod.speed = Harlod.runSpeed
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