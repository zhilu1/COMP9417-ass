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
    time_step = 0.01
    while 1:
        steps += 1
        if(steps % 100 == 0):
            light_right.switchColor()
            light_down.switchColor()
            steps = 1
        if(rnd.randint(0, 10) < 3):
            car_list.append(Car(cross, 'R', light_right))

        if(rnd.randint(0, 10) < 3):
            car_list.append(Car(cross, 'D', light_down))
        # move car and remove from list if move to end
        car_list = [car for car in car_list if (car.move() != -1)]
        # for car in car_list:
        #     res = car.move()
        #     if(res == -1):
        #         car_list

        root.update()
        time.sleep(time_step)


if __name__ == "__main__":
    main()
