#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tkinter import *
import time
import random as rnd
from app.Car import Car
from app.Light import Light
import app.GlobalVars as gv


def main():
    gv.init()
    root = Tk()
    root.title('Traffic Light Simulator')
    # creating the roads
    cross = Canvas(root, width=gv.total_width,
                   height=gv.total_width, bg='grey')
    roadx = cross.create_rectangle(gv.block_width, 0,
                                   gv.road_width+gv.block_width, 2*gv.block_width+gv.road_width,
                                   fill="black"
                                   )
    roady = cross.create_rectangle(0, gv.block_width,
                                   2*gv.block_width+gv.road_width, gv.block_width+gv.road_width,
                                   fill="black"
                                   )
    cross.pack()
    light_right = Light(cross, 'R')
    light_down = Light(cross, 'D')
    light_down.toGreen()
    car_list = []
    steps = 1
    time_step = 0.05
    while 1:
        steps += 1
        if(steps % 100 == 0):
            light_right.switchColor()
            light_down.switchColor()
            steps = 1
        if(rnd.randint(0, 10) < 3):
            car_list.append(Car(cross, 'R', light_right))
            # print(car_list)
        if(rnd.randint(0, 10) < 3):
            car_list.append(Car(cross, 'D', light_down))
        for car in car_list:
            car.move()
        # permissojn
        root.update()
        time.sleep(time_step)

    # root.mainloop()


if __name__ == "__main__":
    main()
