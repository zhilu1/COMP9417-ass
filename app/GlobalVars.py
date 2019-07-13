import numpy as np

unit = 8
car_width = unit
car_length = unit
road_width = car_width*4  # the width of road
block_width = road_width*12  # the width of each grey block, 48 units
total_width = block_width*2+road_width  # total length of the graph 100 units
roadmap = None


def init():

    global roadmap
    roadmap = np.ones((total_width, total_width), dtype=bool)
    # true is crossable while false not
