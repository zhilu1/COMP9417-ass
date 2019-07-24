from tkinter import *
import app.GlobalVars as gv


class Light:

    def __init__(self, canvas, dir):
        self.canvas = canvas
        self.posx = 0  # position of light
        self.posy = 0
        self.color = "red"
        self.delay = 0
        if(dir == 'D'):  # the light on move down road
            self.light = canvas.create_rectangle(gv.block_width+gv.road_width-gv.car_width, gv.block_width-gv.car_width,
                                                 gv.block_width+gv.road_width, gv.block_width,
                                                 fill="red"
                                                 )
            self.posx = int(
                (gv.block_width+gv.road_width-gv.car_width)/gv.unit)
            self.posy = int((gv.block_width-gv.car_width)/gv.unit)
        elif(dir == 'R'):  # the light on move right road
            self.light = canvas.create_rectangle(gv.block_width-gv.car_length, gv. block_width,
                                                 gv.block_width, gv.block_width + gv.car_width,
                                                 fill="red"
                                                 )
            self.posx = int((gv.block_width-gv.car_length)/gv.unit)
            self.posy = int((gv.block_width)/gv.unit)

    def toGreen(self):
        self.canvas.itemconfig(self.light, fill="green")
        self.color = "green"
        self.delay = 4

    def toRed(self):
        self.canvas.itemconfig(self.light, fill="red")
        self.color = "red"
        self.delay = 4

    def switchColor(self):
        if(self.delay != 0):
            return
        if(self.color == "red"):
            self.toGreen()
        elif(self.color == "green"):
            self.toRed()

    def checkMoveable(self, nextx, nexty):
        if(self.posx == nextx and self.posy == nexty and self.color == "red"):
            return False
        else:
            return True

    def decrementDelay(self):
        self.delay = self.delay-1 if self.delay > 0 else 0
