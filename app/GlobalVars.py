"""
File containing global variables used in several files

"""
import numpy as np

unit = 8
car_width = unit
car_length = unit
road_width = car_width*2  # the width of road
block_width = unit*49  # the width of each grey block, 48 units
total_width = block_width*2+road_width  # total length of the graph 100 units
roadmap = None


def init():

    global roadmap
    roadmap = np.ones((total_width, total_width), dtype=bool)
    # road map is a 2d array where each value indicates a position on map
    # true is crossable while false not
