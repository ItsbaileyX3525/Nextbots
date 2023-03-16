

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

Players = {} #The players of the game
PlayersTargetPos={} #Player position updating 
PlayerTargetHpr={} #Player rotation updating

SelfId = -1 #decalres the id of players

@Client.event
def GetId(Id):
    global SelfId
    SelfId = Id
    print(f"My ID is : {SelfId}") #sets and prints the current player id

@Easy.event
def onReplicatedVariableCreated(variable):
    global Client
    variable_name = variable.name
    variable_type = variable.content["type"]

    if variable_type == "player": #If its a player set all this up
        PlayersTargetPos[variable_name] = Vec3(0, 0, 0)
        PlayerTargetHpr[variable_name] = Vec3(0,0,0)
        Players[variable_name] = PlayerRepresentation()
        if SelfId == int(variable.content["id"]):
            Players[variable_name].color = color.red
            Players[variable_name].visible = False

@Easy.event
def onReplicatedVariableUpdated(variable):
    PlayersTargetPos[variable.name] = variable.content["position"]
    PlayerTargetHpr[variable.name] = variable.content["rotation"]
@Easy.event
def onReplicatedVariableRemoved(variable): #Doesn't really work atm but removes the player when disconneted 
    variable_name = variable.name
    variable_type = variable.content["type"]
    if variable_type == "player":
        destroy(Players[variable_name])
        del Players[variable_name]

Ply = Player()

def Messages(key):
    Client.send_message("MyPosition", tuple(Ply.position + (0, 2, 0)))
    Client.send_message("MyRotation", tuple(Ply.rotation + (0,0,0)))

Entity(input=Messages)
def update():

    if Ply.position[1] < -5:
        Ply.position = (randrange(0, 15), 10, randrange(0, 15))
    for p in Players:
        try:
            Players[p].position += (Vec3(PlayersTargetPos[p]) - Players[p].position) / 25
            Players[p].rotation += (Vec3(PlayerTargetHpr[p]) - Players[p].rotation) / 25
        except Exception as e: print(e)
    
    Easy.process_net_events()

App.run()