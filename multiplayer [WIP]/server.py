from ursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)
Easy = EasyUrsinaNetworkingServer(Server)

@Server.event
def onClientConnected(Client):
    Easy.create_replicated_variable(f"player_{Client.id}",{ "type" : "player", "id" : Client.id, "position" : (0, 0, 0), "rotation" : {0,0,0} })
    print(f"{Client} connected !")
    Client.send_message("GetId", Client.id)

@Server.event
def onClientDisconnected(Client):
    Easy.remove_replicated_variable_by_name(f"player_{Client.id}")


@Server.event
def MyPosition(Client, NewPos):
    Easy.update_replicated_variable_by_name(f"player_{Client.id}", "position", NewPos)

@Server.event
def MyRotation(Client, NewHpr):
    Easy.update_replicated_variable_by_name(f'player_{Client.id}', "rotation", NewHpr)

while True:
    Easy.process_net_events()