#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tkinter import *
import time
import random as rnd

road_width = 50  # the width of road
block_width = road_width*5  # the width of each grey block
total_width = block_width*2+road_width  # total length of the graph
car_width = 10
car_length = 10

root = Tk()
root.title('Traffic Light Simulator')


# creating the roads
cross = Canvas(root, width=total_width, height=total_width, bg='grey')
cross.create_rectangle(block_width, 0,
                       road_width+block_width, 2*block_width+road_width,
                       fill="black"
                       )
cross.create_rectangle(0, block_width,
                       2*block_width+road_width, block_width+road_width,
                       fill="black"
                       )


cross.pack()

example_car = cross.create_rectangle(0, block_width,
                                     car_length, block_width+car_width,
                                     fill="yellow"
                                     )

# if(time % (rnd.nextInt(10)+5) == 0):


for x in range(car_length, total_width, car_length):
    cross.move(example_car, car_length, 0)

    root.update()
    time.sleep(.01)

root.mainloop()
