#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tkinter import *
import time
import random as rnd
from app.Car import Car
from app.Light import Light
from app.Constants import *


def main():
    root = Tk()
    root.title('Traffic Light Simulator')
    # creating the roads
    cross = Canvas(root, width=total_width, height=total_width, bg='grey')
    roadx = cross.create_rectangle(block_width, 0,
                                   road_width+block_width, 2*block_width+road_width,
                                   fill="black"
                                   )
    roady = cross.create_rectangle(0, block_width,
                                   2*block_width+road_width, block_width+road_width,
                                   fill="black"
                                   )
    cross.pack()
    light_right = Light(cross, 'R')
    light_down = Light(cross, 'D')

    example_car = Car(cross, 'R')
    example_car2 = Car(cross, 'D')

    #

    for x in range(car_length, total_width, car_length):
        example_car.move()
        example_car2.move()
        root.update()
        time.sleep(0.05)

    root.mainloop()


if __name__ == "__main__":
    main()
