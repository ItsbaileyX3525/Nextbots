

from ursina import *
from random import *
from ursina.prefabs.first_person_controller import FirstPersonController

from ursinanetworking import *


from player import *
from player import *


App = Ursina()
Client = UrsinaNetworkingClient("localhost", 25565)
Easy = EasyUrsinaNetworkingClient(Client)
window.borderless = False

sky = Sky()
ground=Entity(model='plane',texture='grass',scale=1000,texture_scale=(31,31),collider='box')

Players = {}
PlayersTargetPos={}

SelfId = -1

@Client.event
def GetId(Id):
    global SelfId
    SelfId = Id
    print(f"My ID is : {SelfId}")

@Easy.event
def onReplicatedVariableCreated(variable):
    global Client
    variable_name = variable.name
    variable_type = variable.content["type"]

    if variable_type == "player":
        PlayersTargetPos[variable_name] = Vec3(0, 0, 0)
        Players[variable_name] = PlayerRepresentation()
        if SelfId == int(variable.content["id"]):
            Players[variable_name].color = color.red
            Players[variable_name].visible = False

@Easy.event
def onReplicatedVariableUpdated(variable):
    PlayersTargetPos[variable.name] = variable.content["position"]

@Easy.event
def onReplicatedVariableRemoved(variable):
    variable_name = variable.name
    variable_type = variable.content["type"]
    if variable_type == "player":
        destroy(Players[variable_name])
        del Players[variable_name]

Ply = Player()



def input(key):

    Client.send_message("MyPosition", tuple(Ply.position + (0, 1, 0)))

def update():

    if Ply.position[1] < -5:
        Ply.position = (randrange(0, 15), 10, randrange(0, 15))

    for p in Players:
        try:
            Players[p].position += (Vec3(PlayersTargetPos[p]) - Players[p].position) / 25
        except Exception as e: print(e)
    
    Easy.process_net_events()

App.run()