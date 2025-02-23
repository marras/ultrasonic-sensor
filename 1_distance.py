from random import uniform
from plotter import Plotter
import time
# from measure import distance

paused = False

WINDOW_X = 5
SAMPLE_TIME = 0.1
NOISE = 1.5

NUM_SUBPLOTS = 3

RANDOM=True
SPEED=25

# Function to calculate / measure distance
def get_new_distance(current_time):
    return min(current_time * SPEED, 90) + uniform(-NOISE, NOISE)
    #return distance() # Actual measurement

# Create figure and subplot
plotter = Plotter(get_new_distance, WINDOW_X, NUM_SUBPLOTS, SAMPLE_TIME)

# Initialize data
start_time = None
pause_time = 0
last_time = 0

# global start_time
start_time = time.time()

# Spacja - pauza
def on_key_press(event):
    global paused, pause_time
    if event.key == ' ':  # spacebar
        paused = not paused
        if paused:
            print ("Paused")
            # pause_time = time.time() - start_time - last_time
        else:
            print ("Running")
            # start_time = time.time() - last_time

# Connect keyboard event
plotter.fig.canvas.mpl_connect('key_press_event', on_key_press)

plotter.run()

