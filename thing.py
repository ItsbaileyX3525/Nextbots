from ursina import *

app = Ursina(vsync=25)

player = Entity(model='cube', color=color.orange, scale=(2,2,2),x=40,y=3)
follower = Entity(model='sphere', color=color.blue, scale=(2,2,2),y=3)
obsticale=Entity(model='cube',collider='box',color=color.red,y=3,x=20)
ground=Entity(model='plane',texture='grass',scale=1000,texture_scale=(50,50), collider='box')
EditorCamera()

# Keep track of the previous obstacle hit by the follower
previous_obstacle = None

def update():
    global previous_obstacle

    # Get the direction from the follower to the player
    direction = player.position - follower.position

    # Use raycasting to detect any blocks in the follower's path
    ray = raycast(follower.position, direction.normalized(), distance=2, ignore=[player])

    if ray.hit and ray.entity != previous_obstacle:
        # If the ray hits a new obstacle, move the follower around it
        obstacle_normal = ray.normal
        follower.position += obstacle_normal * (ray.distance - 1)
        previous_obstacle = ray.entity
    else:
        # If there's no obstacle or the same obstacle in the way, move the follower towards the player
        previous_obstacle = None
        follower.position += direction.normalized() * time.dt * 5



app.run()


"""from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class PathfindingLaddy(Entity):
    def __init__(self, target, **kwargs):
        super().__init__(self,model='cube',scale_y=1,y=0, collider='box', color=color.green, **kwargs)
        self.target=target
        self.colliding=False
        self.timer=0
        self.timerActive=False

    def update(self):
        if not self.colliding:
            self.position += self.forward * time.dt * 4
            self.look_at_2d(self.target, 'y')
        for Blocks in scene.entities:
            if Blocks.collider=='box':
                if self.intersects(self, Blocks):
                    self.colliding=True
                    self.rotation_x+=90
        
    def colliderUpdate(self):
        if self.timerActive:
            self.timer += time.dt
            self.position += self.forward *time.dt * 4
            if self.timer >= 2:
                self.timerActive=False
                self.colliding=False
                self.timer=0

    def input(self, key):
        pass

app=Ursina()

ground=Entity(model='plane',texture='grass',scale=1000,texture_scale=(50,50), collider='box')
Player=FirstPersonController()
Test=PathfindingLaddy(target=Player)
block=Entity(model='cube', scale_x=5, collider='box',color=color.red)

app.run()"""