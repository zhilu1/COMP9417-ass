from tkinter import *
from app.Constants import *


class Car:
    def __init__(self, canvas, dir):

        self.dx = 0  # x-axis incres/decre
        self.dy = 0  # y-axis incres/decre
        self.canvas = canvas
        if(dir == 'D'):  # car moving down
            self.car = canvas.create_rectangle(block_width+road_width-car_width, 0,
                                               block_width+road_width, car_length,
                                               fill="white"
                                               )
            self.dy = 1
        elif(dir == 'R'):  # car moving right
            self.car = canvas.create_rectangle(0, block_width,
                                               car_length, block_width+car_width,
                                               fill="blue"
                                               )
            self.dx = 1
        # elif(dir == 'L'):
        #     self.dx = -1
        # elif(dir == 'U'):
        #     self.dy = 1

    def move(self):
        self.canvas.move(self.car, self.dx * car_length, self.dy * car_length)
