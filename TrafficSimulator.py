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
    def __init__(self, closest_car_pos_road1,
                 closest_car_pos_road2, light_setting):
        self.ccp1 = closest_car_pos_road1  # road 1 is right to left
        self.ccp2 = closest_car_pos_road2  # road 2 is up to down
        self.light_setting = light_setting
        self.light_delay = 0

    def __str__(self):
        return "State with ccp1 %d ccp2 %d light %d delay %d" % (self.ccp1, self.ccp2, self.light_setting, self.light_delay)


light_right = None
light_down = None
qLearning = Qlearning(
    discount_factor=0.9, learning_rate=0.1, epsilon=0.1, action_space=[0, 1], initial_state=State(9, 9, 0), useFile=False)


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
    time_step = 0.001
    end_time = 10
    # Keeps track of useful statistics
    stats = {
        'episode': [0],
        'rewardsSum': [0]
    }
    car_list1 = []
    car_list2 = []
    # algorithm = FixedSwitch()
    algorithm = qLearning  # select algorithm
    for episode in range(50):

        current_time = 0
        time_total = 0
        st = State(9, 9, 0)  # initialize a state
        light_down.toGreen()
        light_right.toRed()
        rewards = 0
        print("episode" + str(episode))
        for car in car_list1:
            car.destroy()
        for car in car_list2:
            car.destroy()
        car_list1 = []
        car_list2 = []
        while time_total < 1:  # training for some period of time

            # switch based on policy action
            # get action a based on policy
            # take action a
            takeAction(algorithm.getAction())

            if current_time % (rnd.randint(1, 10) + 5) == 0:
                # rand_num = rnd.random()
                # if(rand_num > 0.9):
                # car_list1.insert(0, Car(cross, 'R', light_right))
                # else:
                car_list2.insert(0, Car(cross, 'D', light_down))
            # # generating cars randomly
            # if(rnd.randint(0, 10) < 2):
            #     car_list1.insert(0, Car(cross, 'R', light_right))

            # if(rnd.randint(0, 10) < 2):
            #     car_list2.insert(0, Car(cross, 'D', light_down))
            # move car and remove from list if move to end
            car_list1 = [car for car in car_list1 if (car.move() != -1)]
            car_list2 = [car for car in car_list2 if (car.move() != -1)]

            reward = 0
            # update state and calculating reward
            st.ccp1 = 9
            for car in car_list1:
                reward = reward - 1 if car.stopped else reward  # reward computation
                dist = light_right.posx - car.posx - 1
                print(dist)
                # NOTE logic here is based on car list is in sorted order from start pos to end pos
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
                # print(dist)
                # if(dist < 0):
                # if st.ccp2 >= 9:
                # st.ccp2 = 9
                # break
                # else:
                if(st.ccp2 > dist and dist >= 0):
                    st.ccp2 = dist
            if(st.ccp2 > 9):
                st.ccp2 = 9

            updateLightState(st)

            # pass in reward and new state to improve policy and calculate Q

            algorithm.learn(reward, st)

            root.update()
            time.sleep(time_step)
            time_total += time_step
            rewards += reward
            current_time += 1
        stats['episode'].append(episode)
        stats['rewardsSum'].append(rewards)
        # print(time_total)  # DEBUG USE

    # finish training / execution
    algorithm.saveResult()
    plt.plot(stats['episode'], stats['rewardsSum'])
    plt.xlabel('Episode')
    plt.ylabel('Reward Sum')
    plt.show()
    plt.savefig('plot' + type(algorithm).__name__)


def updateLightState(state):
    state.light_setting = 0
    if(light_right.color == "red"):
        state.light_setting = 1
    # if(light_down.color == "red"):
    #     state.light_setting2 = 1
    state.light_delay = light_right.delay
    # state.light_delay2 = light_down.delay
    # e.g 01 me first light green and second red. Future 2 means yellow

# 0b01 means right light
# 0b10 means down light


def takeAction(action):
    # if (action & 0b01 != 0):
        # switch right light
    if(action == 1):
        light_right.switchColor()
        light_down.switchColor()
    # if (action & 0b10 != 0):
    # switch down light
    light_right.decrementDelay()
    light_down.decrementDelay()


if __name__ == "__main__":
    main()
