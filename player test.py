from ursina import *
from direct.actor.Actor import Actor
from direct.interval.ActorInterval import LerpAnimInterval
from panda3d.direct import LerpBlendType
app=Ursina()
apps=Ursina()
EditorCamera()
class Character(Entity): # Player model, attaches to the Harlod (FPC)
    def __init__(self):
        super().__init__()
        self.actor=Actor("player.glb")
        self.actor.reparentTo(scene)
        self.actor.setScale(0.018)
        self.actor.setHpr(180,0,0)
        x,y,z=self.actor.getPos()
        self.actor.setPos(x,.9,1)
        self.actor.loop("idle")
        self.actor.ls()
        self.current_anim=None
    def AnimLoop(self,toanim,rate=1,part=None):
        fromanim=self.actor.get_current_anim()
        self.actor.enableBlend()
        self.actor.loop(str(toanim), partName=part)
        self.actor.setPlayRate(rate,toanim,partName=part)
        if self.current_anim!=None:
            Interv=LerpAnimInterval(self.actor, 0.25, self.current_anim, toanim, partName=part)
        else:
            Interv=LerpAnimInterval(self.actor, 0.25, fromanim, toanim, partName=part)
        print(self.actor.getCurrentAnim())
        Interv.start()
        self.current_anim=toanim
    
    def input(self, key):
        if key=='w':
            self.AnimLoop(toanim="walk")
        elif key=='w' and held_keys['shift']:
            self.AnimLoop(toanim="run")
        elif held_keys['w'] and key=='shift':
            self.AnimLoop(toanim="run")
        elif key=='a':
            self.AnimLoop(toanim="strafe left")
        elif key=='d':
            self.AnimLoop(toanim="strafe right")
        elif key=='s':
            self.AnimLoop(toanim="walk backwards")
        elif key=='s' and held_keys['shift']:
            self.AnimLoop(toanim="run backwards")
        elif key=='shift' and held_keys['s']:
            self.AnimLoop(toanim="run backwards")
        elif key == 'd up' and not held_keys['a'] and not held_keys['s'] and not held_keys['w']:
            self.AnimLoop(toanim="idle")
        elif key == 'a up'and not held_keys['d'] and not held_keys['s'] and not held_keys['w']:
            self.AnimLoop(toanim="idle")
        elif key == 's up'and not held_keys['a'] and not held_keys['d'] and not held_keys['w']:
            self.AnimLoop(toanim="idle")
        elif key == 'w up'and not held_keys['a'] and not held_keys['s'] and not held_keys['d']:
            self.AnimLoop(toanim="idle")
        elif key=='m':
            self.AnimLoop(toanim='death')
        elif key=='n':
            self.AnimLoop(toanim="continue")

    def update(self):
        currfix=self.actor.get_current_anim()
        if currfix!=None:
            pass
        else:
            self.AnimLoop(toanim="idle")
poo=Character()
app.run()