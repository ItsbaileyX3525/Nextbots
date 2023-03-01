from ursina import *
from direct.showbase.Loader import Loader
from panda3d.core import Filename
window.borderless=False
app=Ursina()
winfile = "D:\\python\\3D\\Nextbots\\assets\\textures"
pandafile = Filename.fromOsSpecific(winfile)
f=Entity(model='cube',texture=load_texture("andrew.png", winfile))

app.run()