#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tkinter import *
import time
import random as rnd
from app.Car import Car
from app.Light import Light
import app.GlobalVars as gv
from app.FixedSwitch import FixedSwitch
from app.Qlearning import Qlearning
import matplotlib.pyplot as plt


class State:
    def __init__(self, steps, closest_car_pos_road1,
                 closest_car_pos_road2, light_setting1, light_setting2):
        self.steps = steps
        self.ccp1 = closest_car_pos_road1  # road 1 is right to left
        self.ccp2 = closest_car_pos_road2  # road 2 is up to down
        self.light_setting1 = light_setting1
        self.light_setting2 = light_setting2
        self.light_delay1 = 0
        self.light_delay2 = 0


light_right = None
light_down = None
qLearning = Qlearning(
    0.9, 0.1, 0.1, [0b00, 0b10, 0b01, 0b11], State(1, 9, 9, 0, 1), True)


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
    global light_right
    global light_down
    light_right = Light(cross, 'R')
    light_down = Light(cross, 'D')
    light_down.toGreen()
    car_list1 = []  # to right cars list
    car_list2 = []  # to down cars list
    steps = 1
    time_step = 0.01
    st = State(1, 9, 9, 0, 1)  # initialize a state
    time_total = 0
    end_time = 10
    # Keeps track of useful statistics
    stats = {
        'time_step': [time_total],
        'rewards': [0]
    }

    algorithm = FixedSwitch()
    # algorithm = qLearning  # select algorithm
    while time_total < 10:  # training for some period of time
        st.steps += 1

        # switch based on policy action
        # get action a based on policy
        # take action a
        takeAction(algorithm.getAction())

        # generating cars randomly
        if(rnd.randint(0, 10) < 3):
            car_list1.append(Car(cross, 'R', light_right))

        if(rnd.randint(0, 10) < 3):
            car_list2.append(Car(cross, 'D', light_down))
        # move car and remove from list if move to end
        car_list1 = [car for car in car_list1 if (car.move() != -1)]
        car_list2 = [car for car in car_list2 if (car.move() != -1)]

        reward = 0
        # update state and calculating reward
        st.ccp1 = 9
        for car in car_list1:
            reward = reward - 1 if car.stopped else reward  # reward computation
            dist = light_right.posx - car.posx - 1
            if(dist < 0):
                if st.ccp1 >= 9:
                    st.ccp1 = 9
                break
            else:
                st.ccp1 = dist
        st.ccp2 = 9
        for car in car_list2:
            reward = reward - 1 if car.stopped else reward  # reward computation
            dist = light_down.posy - car.posy - 1
            if(dist < 0):
                if st.ccp2 >= 9:
                    st.ccp2 = 9
                break
            else:
                st.ccp2 = dist

        updateLightState(st)

        # pass in reward and new state to improve policy and calculate Q

        algorithm.learn(reward, st)

        root.update()
        time.sleep(time_step)
        time_total += time_step
        stats['time_step'].append(time_total)
        stats['rewards'].append(reward)
        # print(time_total)  # DEBUG USE

    # finish training / execution
    plt.plot(stats['time_step'], stats['rewards'])
    plt.xlabel('Time')
    plt.ylabel('Reward')
    plt.show()
    algorithm.saveResult()


def updateLightState(state):
    state.light_setting1 = 0
    state.light_setting2 = 0
    if(light_right.color == "red"):
        state.light_setting1 = 1
    if(light_down.color == "red"):
        state.light_setting2 = 1
    state.light_delay1 = light_right.delay
    state.light_delay2 = light_down.delay
    # e.g 01 me first light green and second red. Future 2 means yellow

# 0b01 means right light
# 0b10 means down light


def takeAction(action):
    if (action & 0b01 != 0):
        # switch right light
        light_right.switchColor()
    if (action & 0b10 != 0):
        # switch down light
        light_down.switchColor()
    light_right.decrementDelay()
    light_down.decrementDelay()


if __name__ == "__main__":
    main()
