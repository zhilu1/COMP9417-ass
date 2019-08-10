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
        self.ccp1 = closest_car_pos_road1  # closest car in road right to left
        self.ccp2 = closest_car_pos_road2  # closest car in road up to down
        self.ccp3 = closest_car_pos_road3  # closest car in road left to right
        self.ccp4 = closest_car_pos_road4  # closest car in road down to up
        # since all 4 lights in a intersection will switch at the same time, we only track the light in road left to right
        self.light_setting = light_setting  # light setting 0-green 1-red.
        self.light_delay = 0

    def __str__(self):
        return "[%d %d %d %d %d %d]" % (self.ccp1, self.ccp2, self.ccp3, self.ccp4, self.light_setting, self.light_delay)


light_right = None
light_down = None
light_left = None
light_up = None
# default Q learning parameter
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
    # algorithm = FixedSwitch() # select algorithm Fixed switch
    algorithm = qLearning  # select algorithm Q learning
    running(algorithm, cross, rounds=200)  # run algorithms

    """
    comment out following comment section to generate data for various parameters  
    """

    # for epsilon in np.arange(0.6, 1, 0.1):
    #     algorithm = Qlearning(
    #         discount_factor=0.9, learning_rate=0.1, epsilon=epsilon, action_space=[0, 1], initial_state=State(9, 9, 9, 9, 1), useFile=False)
    #     running(algorithm, cross, 150)
    #     algorithm.useFile = True
    #     running(algorithm, cross, 50)

    # for learning_rate in np.arange(0, 1, 0.1):
    #     algorithm = Qlearning(
    #         discount_factor=0.9, learning_rate=learning_rate, epsilon=0.1, action_space=[0, 1], initial_state=State(9, 9, 9, 9, 1), useFile=False)
    #     running(algorithm, cross, 200, 5)
    #     algorithm.useFile = True
    #     running(algorithm, cross, 50, 5)
    # gammas = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5,
    #           0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]
    # for discount_factor in gammas:
    #     algorithm = Qlearning(
    #         discount_factor=discount_factor, learning_rate=0.1, epsilon=0.1, action_space=[0, 1], initial_state=State(9, 9, 9, 9, 1), useFile=False)
    #     running(algorithm, cross, 150, 5)
    #     algorithm.useFile = True
    #     running(algorithm, cross, 50, 5)

    # for inten in [0, 5, 10, 20]:
    #     algorithm = Qlearning(
    #         discount_factor=0.9, learning_rate=0.1, epsilon=0.1, action_space=[0, 1], initial_state=State(9, 9, 9, 9, 1), useFile=False, extra_foldername=("instensitytest" + str(inten)))
    #     running(algorithm, cross, 200, inten)
    #     algorithm.useFile = True
    #     running(algorithm, cross, 50, inten)
    # def reward_func_anystopped(a, cond): return -1 if cond else 0
    # def reward_func_sumstopped(a, cond): return a-1 if cond else a
    # algorithm = Qlearning(
    #     discount_factor=0.9, learning_rate=0.1, epsilon=0.1, action_space=[0, 1],
    #     initial_state=State(9, 9, 9, 9, 1), useFile=False, extra_foldername=("reward_func_anystopped"))
    # running(algorithm, cross, reward_func=reward_func_anystopped)
    # algorithm.useFile = True
    # running(algorithm, cross, reward_func=reward_func_anystopped)

    # algorithm = Qlearning(
    #     discount_factor=0.9, learning_rate=0.1, epsilon=0.1, action_space=[0, 1],
    #     initial_state=State(9, 9, 9, 9, 1), useFile=False)
    # running(algorithm, cross, rounds=300)
    # algorithm.useFile = True
    # running(algorithm, cross, reward_func=reward_func_sumstopped)

    # for training in range(10):
    #     total_reward = 0


def running(algorithm, cross, rounds=150, intensitiy=5, reward_func=lambda a, cond: a-1 if cond else a):
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
        # reset env for each episode
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
        while time_total < 1:  # each episode contains 1000 time-steps
            # slow down the execution if you want to see the simulating
            # time.sleep(0.05)
            # get action a based on algorithm
            # take action a
            takeAction(algorithm.getAction())

            # generate cars
            if current_time % (rnd.randint(1, 5) + intensitiy) == 0:
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

            moveCars(car_list_down)
            moveCars(car_list_left)
            moveCars(car_list_up)
            moveCars(car_list_right)

            # calculating rewards and update states
            reward = 0
            cars_num = 0
            st.ccp1 = 9
            for car in car_list_right:
                reward = reward_func(reward, car.stopped)  # reward computation
                cars_num = cars_num + 1 if car.stopped else cars_num
                dist = light_right.posx - car.posx - 1
                if(st.ccp1 > dist and dist >= 0):
                    st.ccp1 = dist
            if(st.ccp1 > 9):
                st.ccp1 = 9

            st.ccp2 = 9
            for car in car_list_down:
                reward = reward_func(reward, car.stopped)
                cars_num = cars_num + 1 if car.stopped else cars_num
                dist = light_down.posy - car.posy - 1
                if(st.ccp2 > dist and dist >= 0):
                    st.ccp2 = dist
            if(st.ccp2 > 9):
                st.ccp2 = 9

            st.ccp3 = 9
            for car in car_list_left:
                reward = reward_func(reward, car.stopped)
                cars_num = cars_num + 1 if car.stopped else cars_num
                dist = car.posx - light_left.posx - 1
                if(st.ccp3 > dist and dist >= 0):
                    st.ccp3 = dist
            if(st.ccp3 > 9):
                st.ccp3 = 9

            st.ccp4 = 9
            for car in car_list_up:
                reward = reward_func(reward, car.stopped)
                cars_num = cars_num + 1 if car.stopped else cars_num
                dist = car.posy - light_up.posy - 1
                if(st.ccp4 > dist and dist >= 0):
                    st.ccp4 = dist
            if(st.ccp4 > 9):
                st.ccp4 = 9
            updateLightState(st)

            # pass in reward and new state to improve Q table
            algorithm.learn(reward, st)

            root.update()
            time_total += time_step
            rewards += cars_num
            current_time += 1
        stats['episode'].append(episode)
        stats['rewardsSum'].append(rewards)

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
    state.light_delay = light_right.delay
    # e.g 01 me first light green and second red. Future 2 means yellow


def moveCars(car_list):
    car_list = [car for car in car_list if (car.move() != -1)]


def takeAction(action):
    # switch all lights if action is 1
    if(action == 1):
        light_right.switchColor()
        light_down.switchColor()
        light_left.switchColor()
        light_up.switchColor()
    # decrease the delays in lights
    light_right.decrementDelay()
    light_down.decrementDelay()
    light_left.decrementDelay()
    light_up.decrementDelay()


if __name__ == "__main__":
    main()
