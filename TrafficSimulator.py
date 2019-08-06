#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
from app.Qlearning import Qlearning
from app.FixedSwitch import FixedSwitch
import app.GlobalVars as gv
from app.Light import Light
from app.Car import Car
import random as rnd
import time
import numpy as np
from tkinter import *
root = Tk()


class State:
    def __init__(self, closest_car_pos_road1,
                 closest_car_pos_road2, closest_car_pos_road3, closest_car_pos_road4, light_setting):
        self.ccp1 = closest_car_pos_road1  # road 1 is right to left
        self.ccp2 = closest_car_pos_road2  # road 2 is up to down
        self.ccp3 = closest_car_pos_road3  # road 3 is left to right
        self.ccp4 = closest_car_pos_road4  # road 4 is down to up
        self.light_setting = light_setting
        self.light_delay = 0

    def __str__(self):
        # return "State with ccp1 %d ccp2 %d light %d delay %d" % (self.ccp1, self.ccp2, self.light_setting, self.light_delay)
        return "[%d %d %d %d %d %d]" % (self.ccp1, self.ccp2, self.ccp3, self.ccp4, self.light_setting, self.light_delay)


light_right = None
light_down = None
light_left = None
light_up = None
qLearning = Qlearning(
    discount_factor=0.9, learning_rate=0.1, epsilon=0.1, action_space=[0, 1], initial_state=State(9, 9, 9, 9, 1), useFile=False)


def main():
    gv.init()
    # root = Tk()
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
    global light_left
    global light_up
    light_right = Light(cross, 'R')
    light_down = Light(cross, 'D')
    light_left = Light(cross, 'L')
    light_up = Light(cross, 'U')
    time_step = 0.001
    end_time = 10
    # Keeps track of useful statistics
    # algorithm = FixedSwitch()
    algorithm = qLearning  # select algorithm

    for epsilon in np.arange(0, 1, 0.1):
        algorithm = Qlearning(
            discount_factor=0.9, learning_rate=0.1, epsilon=epsilon, action_space=[0, 1], initial_state=State(9, 9, 9, 9, 1), useFile=False)
        running(algorithm, cross, 100)
        algorithm.useFile = True
        running(algorithm, cross, 50)

    for learning_rate in np.arange(0, 1, 0.1):
        algorithm = Qlearning(
            discount_factor=0.9, learning_rate=learning_rate, epsilon=0.1, action_space=[0, 1], initial_state=State(9, 9, 9, 9, 1), useFile=False)
        running(algorithm, cross, 100)
        algorithm.useFile = True
        running(algorithm, cross, 50)
    gammas = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5,
              0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]
    for discount_factor in gammas:
        algorithm = Qlearning(
            discount_factor=discount_factor, learning_rate=0.1, epsilon=0.1, action_space=[0, 1], initial_state=State(9, 9, 9, 9, 1), useFile=False)
        running(algorithm, cross, 100)
        algorithm.useFile = True
        running(algorithm, cross, 50)

    # for training in range(10):
    #     total_reward = 0


def running(algorithm, cross, rounds):
    print(str(algorithm))
    car_list_right = []
    car_list_down = []
    car_list_left = []
    car_list_up = []
    stats = {
        'episode': [],
        'rewardsSum': []
    }
    time_step = 0.001
    for episode in range(rounds):

        current_time = 0
        time_total = 0
        st = State(9, 9, 9, 9, 1)  # initialize a state
        light_down.toGreen()
        light_up.toGreen()
        light_right.toRed()
        light_left.toRed()
        rewards = 0
        print("episode" + str(episode))
        # clean up all cars
        for car in car_list_right:
            car.destroy()
        for car in car_list_down:
            car.destroy()
        for car in car_list_left:
            car.destroy()
        for car in car_list_up:
            car.destroy()
        car_list_right = []
        car_list_down = []
        car_list_left = []
        car_list_up = []
        while time_total < 1:  # training for some period of time

            # switch based on policy action
            # get action a based on policy
            # take action a
            takeAction(algorithm.getAction())

            if current_time % (rnd.randint(1, 5) + 5) == 0:
                # only one or zero car can appear at one timestep
                rand_num = rnd.random()
                if(rand_num > 0.75):
                    car_list_right.append(Car(cross, 'R', light_right))
                elif(rand_num > 0.5):
                    car_list_left.append(Car(cross, 'L', light_left))
                elif(rand_num > 0.25):
                    car_list_up.append(Car(cross, 'U', light_up))
                else:
                    car_list_down.append(Car(cross, 'D', light_down))
            # # generating cars randomly
            # if(rnd.randint(0, 10) < 2):
            #     car_list_right.insert(0, Car(cross, 'R', light_right))

            # if(rnd.randint(0, 10) < 2):
            #     car_list_down.insert(0, Car(cross, 'D', light_down))
            # move car and remove from list if move to end
            # car_list_right = [
            #     car for car in car_list_right if (car.move() != -1)]
            # car_list_down = [
            #     car for car in car_list_down if (car.move() != -1)]
            # car_list3 = [car for car in car_list_left if (car.move() != -1)]
            # car_list4 = [car for car in car_list_up if (car.move() != -1)]

            moveCars(car_list_down)
            moveCars(car_list_left)
            moveCars(car_list_up)
            moveCars(car_list_right)

            reward = 0
            st.ccp1 = 9
            for car in car_list_right:
                reward = reward - 1 if car.stopped else reward  # reward computation
                # if car.stopped:
                #     reward = -1
                dist = light_right.posx - car.posx - 1
                if(st.ccp1 > dist and dist >= 0):
                    st.ccp1 = dist
            if(st.ccp1 > 9):
                st.ccp1 = 9

            st.ccp2 = 9
            for car in car_list_down:
                reward = reward - 1 if car.stopped else reward  # reward computation
                # if car.stopped:
                #     reward = -1
                dist = light_down.posy - car.posy - 1
                if(st.ccp2 > dist and dist >= 0):
                    st.ccp2 = dist
            if(st.ccp2 > 9):
                st.ccp2 = 9

            st.ccp3 = 9
            for car in car_list_left:
                reward = reward - 1 if car.stopped else reward  # reward computation
                # if car.stopped:
                #     reward = -1
                dist = car.posx - light_left.posx - 1
                if(st.ccp3 > dist and dist >= 0):
                    st.ccp3 = dist
            if(st.ccp3 > 9):
                st.ccp3 = 9

            st.ccp4 = 9
            for car in car_list_up:
                reward = reward - 1 if car.stopped else reward  # reward computation
                # if car.stopped:
                #     reward = -1
                dist = car.posy - light_up.posy - 1
                if(st.ccp4 > dist and dist >= 0):
                    st.ccp4 = dist
            if(st.ccp4 > 9):
                st.ccp4 = 9
            updateLightState(st)

            # print(st)

            # pass in reward and new state to improve policy and calculate Q

            algorithm.learn(reward, st)

            root.update()
            time_total += time_step
            rewards += reward
            current_time += 1
        stats['episode'].append(episode)
        stats['rewardsSum'].append(rewards)
        # print(time_total)  # DEBUG USE

        # finish training / execution
    #         total_reward += rewards
    #     total_stats['totalReward'].append(total_reward)
    #     total_stats['training'].append(training)
    # plt.plot(total_stats['training'], total_stats['totalReward'])
    # plt.xlabel('Training')
    # plt.ylabel('Reward Total')
    algorithm.saveResult(stats['episode'], stats['rewardsSum'])
    # clean up all cars
    for car in car_list_right:
        car.destroy()
    for car in car_list_down:
        car.destroy()
    for car in car_list_left:
        car.destroy()
    for car in car_list_up:
        car.destroy()


def updateLightState(state):
    state.light_setting = 0
    if(light_right.color != "green"):
        state.light_setting = 1
    # if(light_down.color == "red"):
    #     state.light_setting2 = 1
    state.light_delay = light_right.delay
    # state.light_delay2 = light_down.delay
    # e.g 01 me first light green and second red. Future 2 means yellow

# 0b01 means right light
# 0b10 means down light


def moveCars(car_list):
    car_list = [car for car in car_list if (car.move() != -1)]


def takeAction(action):
    # if (action & 0b01 != 0):
        # switch right light
    if(action == 1):
        light_right.switchColor()
        light_down.switchColor()
        light_left.switchColor()
        light_up.switchColor()
    # if (action & 0b10 != 0):
    # switch down light
    light_right.decrementDelay()
    light_down.decrementDelay()
    light_left.decrementDelay()
    light_up.decrementDelay()


if __name__ == "__main__":
    main()
