from re import A
from ursina import *
from random import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursinanetworking import *
from direct.actor.Actor import *

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_sensitivity = (155, 155)
        self.actor=Actor("player.glb")
        self.actor.loop("idle")
        self.actor.reparentTo(self)
        self.actor.setScale(0.018)
        self.actor.setHpr(180,0,0)
        x,y,z=self.actor.getPos()
        self.actor.setPos(x,1,1)
class PlayerRepresentation(Entity):
    def __init__(self, position = (5,5,5)):
        super().__init__(parent = scene,position = position,origin_y = .5,model='player.glb',scale=0.018)

        

App = Ursina()
Client = UrsinaNetworkingClient("localhost", 25565)
Easy = EasyUrsinaNetworkingClient(Client)
window.borderless = False

sky = Sky()

Blocks = {}
Players = {}
PlayersTargetPos = {}

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
    if variable_type == "block":
        block_type = variable.content["block_type"]
        if block_type == "grass": new_block = Entity(model='plane',texture='grass',collider='box')
        else:
            print("Block not found.")
            return

        new_block.name = variable_name
        new_block.position = variable.content["position"]
        new_block.client = Client
        Blocks[variable_name] = new_block
    elif variable_type == "player":
        PlayersTargetPos[variable_name] = Vec3(0, 0, 0)
        Players[variable_name] = PlayerRepresentation()
        Players[variable_name].loop("idle")
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
ground=Entity(model='plane',texture='grass',collider='box',scale=1000)

INDEX = 1
SELECTED_BLOCK = ""



def input(key):

    global INDEX, SELECTED_BLOCK

    if key == "right mouse down":
        A = raycast(Ply.position + (0, 2, 0), camera.forward, distance = 6, traverse_target = scene)

    if key == "left mouse down":
        A = raycast(Ply.position + (0, 2, 0), camera.forward, distance = 6, traverse_target = scene)


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