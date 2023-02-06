from ursina import *
import random as ra
from ursina.prefabs.first_person_controller import FirstPersonController
from ursinanetworking import *
from time import sleep

App = Ursina()
Client = UrsinaNetworkingClient("localhost", 25565)
Easy = EasyUrsinaNetworkingClient(Client)
window.borderless = False

Players = {}
PlayersTargetPos = {}
SelfId = -1

@Client.event
def GetId(Id):
    global SelfId
    SelfId = Id
    print(f"My ID is : {SelfId}")

@Easy.event
def onReplicatedVariableUpdated(variable):
    PlayersTargetPos[variable.name] = variable.content["position"]

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_sensitivity = (155, 155)
Ply = Player()

def update():

    if Ply.position[1] < -5:
        Ply.position = (ra.randrange(0, 15), 10, ra.randrange(0, 15))

    for p in Players:
        try:
            Players[p].position += (Vec3(PlayersTargetPos[p]) - Players[p].position) / 25
        except Exception as e: print(e)
    
    Easy.process_net_events()

App.run()