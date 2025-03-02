from random import uniform
from plotter import Plotter
import time
import sys
from measure import distance

paused = False

WINDOW_X = 5
WINDOW_Y = [[-1, 100], [-20,50], [-50,50]]
SAMPLE_TIME = 0.01
NOISE = 1.5

NUM_SUBPLOTS = 3
MOVE_WINDOW = True

SPEED=25

# Function to calculate / measure distance
def get_new_distance(current_time):
    #return min(current_time * SPEED, 90) + uniform(-NOISE, NOISE)
    return distance() # Actual measurement


if __name__ == '__main__':
    NUM_SUBPLOTS = int(sys.argv[1])

    # Create figure and subplot
    plotter = Plotter(get_new_distance, WINDOW_X, NUM_SUBPLOTS, SAMPLE_TIME, WINDOW_Y, MOVE_WINDOW)

    # Initialize data
    start_time = None
    pause_time = 0
    last_time = 0

    # global start_time
    start_time = time.time()

    plotter.run()

