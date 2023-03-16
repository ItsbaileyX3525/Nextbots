from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from direct.actor.Actor import Actor

app=Ursina()
class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_sensitivity = (155, 155)

class PlayerRepresentation(Entity):
    def __init__(self, position = (0,0,0)):
        super().__init__(parent = scene,position = position,origin_y=2,rotation=(0,0,0),model = 'player.glb',color = color.white,highlight_color = color.white)
        self.actor=Actor('player.glb')
        self.actor.loop("idle")
        self.actor.setScale(.18,.18,.18)
        self.actor.reparentTo(self)
        self.actor.setPos(0,0,-20)
        self.actor.setHpr(0,0,0)
    

p=PlayerRepresentation()

def input(key):
    if key=='k':
        print(p.actor.getPos())
    if key=='l':
        print(p.position)
    if held_keys['w']:
        p.rotation+=(1,0,0)
    if held_keys['s']:
        p.rotation-=(1,0,0)
    if held_keys['a']:
        p.rotation+=(0,0,1)
    if held_keys['d']:
        p.rotation+=(0,0,-1)
    if held_keys['f']:
        p.rotation+=(0,1,0)
    if held_keys['g']:
        p.rotation+=(0,-1,0)
    print(p.world_rotation)

ground=Entity(model='plane',texture='grass',scale=1000)
EditorCamera()
app.run()