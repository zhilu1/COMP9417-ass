from tkinter import *
from app.Constants import *


class Light:

    def __init__(self, canvas, dir):
        self.canvas = canvas
        if(dir == 'D'):  # the light on move down road
            self.light = canvas.create_rectangle(block_width+road_width-car_width, block_width-car_width,
                                                 block_width+road_width, block_width,
                                                 fill="red"
                                                 )
        elif(dir == 'R'):  # the light on move right road
            self.light = canvas.create_rectangle(block_width-car_length, block_width,
                                                 block_width, block_width+car_width,
                                                 fill="red"
                                                 )

    def toGreen(self):
        self.canvas.itemconfig(self.light, fill="green")
        self.canvas.itemconfig(self.light, fill="red")
