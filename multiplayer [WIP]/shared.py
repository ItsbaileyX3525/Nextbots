from ursina import *
from ursinanetworking import *

class Ground(Entity, Replicator):
    def __init__(self, position=(0,0,0)):
        Entity.__init__(self,scale=1000,parent=scene,position=position,model='cube',origin_y = .5,texture = 'grass',collider='box',)
        Replicator.__init__(self)

