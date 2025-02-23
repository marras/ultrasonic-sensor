from random import uniform
from plotter import Plotter
import time
import sys
# from measure import distance

WINDOW_X = 5
SAMPLE_TIME = 0.1
NOISE = 1.5

NUM_SUBPLOTS = 1
MOVE_WINDOW = False # Do not move window for multiple plots, looks like crap

RANDOM=True
SPEED=25

# Function to calculate / measure distance
def get_new_distance(current_time):
    return min(current_time * SPEED, 90) + uniform(-NOISE, NOISE)
    #return distance() # Actual measurement

paused = False
# Spacja - pauza
def on_key_press(event):
    global paused
    if event.key == ' ':  # spacebar
        paused = not paused
        if paused:
            print ("Paused")
            plotter.pause()
        else:
            print ("Running")
            plotter.run()


if __name__ == '__main__':
    NUM_SUBPLOTS = int(sys.argv[1])

    # Create figure and subplot
    plotter = Plotter(get_new_distance, WINDOW_X, NUM_SUBPLOTS, SAMPLE_TIME, MOVE_WINDOW)

    # Initialize data
    start_time = None
    pause_time = 0
    last_time = 0

    # global start_time
    start_time = time.time()

    #Connect keyboard event
    plotter.fig.canvas.mpl_connect('key_press_event', on_key_press)

    plotter.run()

