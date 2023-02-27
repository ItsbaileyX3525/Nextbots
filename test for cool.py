
from ursina import *
app = Ursina()
timer=0
a=Text(text="I said this file doesnt exist!")
def update():
    global timer
    timer+=time.dt
if timer>=6:
    b=Text(text="Come on man get out of here")
app.run()