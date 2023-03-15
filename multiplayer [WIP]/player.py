from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from direct.actor.Actor import Actor

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_sensitivity = (155, 155)

class PlayerRepresentation(Entity):
    def __init__(self, position = (5,5,5)):
        super().__init__(parent = scene,position = position,origin_y=2,rotation=(-90,0,0),model = None,color = color.white,highlight_color = color.white)
        self.actor=Actor('player.glb')
        self.actor.loop("idle")
        self.actor.setScale(.018,.018,.018)
        self.actor.setHpr(0,-90,0)
        self.actor.reparentTo(self)
        self.actor.setPos(0,-2,1)