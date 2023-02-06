from ursinanetworking import *
from shared import *

Server = UrsinaNetworkingServer("localhost", 25565)
Blabla = ReplicatedSvEventsHandler(Server)
new_block = Blabla.create_replicated_object(Ground)

while True:
    Server.process_net_events()
    Blabla.replicated_update()