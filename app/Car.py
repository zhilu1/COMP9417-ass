from tkinter import *
import app.GlobalVars as gv


class Car:
    def __init__(self, canvas, dir, light):
        self.dx = 0  # x-axis incres/decre
        self.dy = 0  # y-axis incres/decre
        self.canvas = canvas
        self.posx = 0  # starting x-axis position of car
        self.posy = 0  # starting y-axis position of car
        self.light = light
        self.stopped = False  # movable at beginning
        if(dir == 'D'):  # car moving down
            self.car = canvas.create_rectangle(gv.block_width+gv.road_width-gv.car_width, 0,
                                               gv.block_width+gv.road_width, gv.car_length,
                                               fill="white"
                                               )
            self.dy = 1
            self.posx = int(
                (gv.block_width+gv.road_width-gv.car_width) / gv.unit)
            self.posy = 0
        elif(dir == 'R'):  # car moving right
            self.car = canvas.create_rectangle(0, gv.block_width,
                                               gv.car_length, gv.block_width + gv.car_width,
                                               fill="blue"
                                               )
            self.dx = 1
            self.posx = 0
            self.posy = int(gv.block_width / gv.unit)
        elif(dir == 'L'):  # car moving right
            self.car = canvas.create_rectangle(gv.total_width - gv.car_length, gv.block_width+gv.road_width-gv.car_width,
                                               gv.total_width, gv.block_width + gv.road_width,
                                               fill="light blue"
                                               )
            self.dx = -1
            self.posx = int((gv.total_width - gv.car_length) / gv.unit)
            self.posy = int((gv.block_width+gv.road_width -
                             gv.car_width) / gv.unit)
        elif(dir == 'U'):  # car moving right
            self.car = canvas.create_rectangle(gv.block_width, gv.total_width - gv.car_length,
                                               gv.block_width+gv.car_width, gv.total_width,
                                               fill="orange"
                                               )
            self.dy = -1
            self.posx = int(gv.block_width / gv.unit)
            self.posy = int((gv.total_width - gv.car_length) / gv.unit)
        gv.roadmap[self.posx, self.posy] = False

    def move(self):
        # get next position moving to
        nextx = self.posx + self.dx
        nexty = self.posy + self.dy
        total_road_units = gv.total_width/gv.unit
        # destroy this car if moving out of boundary
        if(nextx > total_road_units or nexty > total_road_units or nextx < 0 or nexty < 0):
            self.destroy()
            return -1
        if(gv.roadmap[nextx, nexty] and self.lightMoveable(nextx, nexty)):
            # if moveable, then move
            self.canvas.move(self.car, self.dx * gv.car_length,
                             self.dy * gv.car_length)

            gv.roadmap[self.posx, self.posy] = True
            self.posx += self.dx
            self.posy += self.dy
            gv.roadmap[self.posx, self.posy] = False
            self.stopped = False  # movable
            return 1  # moved
        self.stopped = True  # unmovable
        return 0  # not moved

    def lightMoveable(self, nextx, nexty):
        return self.light.checkMoveable(nextx, nexty)

    def destroy(self):
        self.canvas.delete(self.car)
        gv.roadmap[self.posx, self.posy] = True
