import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import uniform
from collections import deque
import numpy as np
import time
from measure import distance

# Add pause state
paused = False

WINDOW_X = 5
SAMPLE_TIME = 0.1
NOISE = 1.5
MEAN_LAST_POINTS = 5


def plot_distance(ax):
	ax.set_xlim(0, WINDOW_X)
	ax.set_ylim(-1, 100)
	ax.set_xlabel('Czas [s]')
	ax.set_ylabel('Odległość [cm]')
	ax.set_title('Odległość od czujnika ultradźwiękowego')

	line, = ax.plot([], [], 'b-', label='Położenie')
	point, = ax.plot([], [], 'ro', label='Nowy punkt')

    return line

def plot_velocity(ax):
	ax.set_xlim(0, WINDOW_X)
	ax.set_ylim(-20, 50)
	ax.set_xlabel('Czas [s]')
	ax.set_ylabel('Prędkość [cm/s]')
	ax.set_title('Prędkość chwilowa')
	
	line, = ax.plot([], [], 'b-', label='Prędkość')
	point, = ax.plot([], [], 'ro', label='Nowy punkt 2')

    return (line, point)

# Create figure and subplot
NUM_SUBPLOTS = 2
fig, ax = plt.subplots(NUM_SUBPLOTS)

dist_line, dist_point = plot_distance(ax[0])
v_line, v_point = plot_velocity(ax[1])
 
# Add status text
status_text = ax[0].text(0.0, 0.05, 'Running', transform=ax[0].transAxes)

# Initialize data
x = deque(maxlen=int(WINDOW_X/SAMPLE_TIME))
y = deque(maxlen=int(WINDOW_X/SAMPLE_TIME))
v = deque(maxlen=int(WINDOW_X/SAMPLE_TIME))
start_time = None
pause_time = 0
last_time = 0

def init():
    global start_time
    start_time = time.time()
    dist_line.set_data([], [])
    dist_point.set_data([], [])
    v_line.set_data([], [])
    v_point.set_data([], [])
    return dist_line, dist_point, v_line,v_point, status_text


def get_new_distance(current_time):
    # Random
    #return min(current_time * SPEED, 90) + uniform(-NOISE, NOISE)

    return distance()

def update(frame):
    global last_time, pause_time
    
    if not paused:
        current_time = time.time() - start_time - pause_time
        last_time = current_time
        
        x.append(current_time)

        new_y = get_new_distance(current_time)
                
        y.append(new_y)

        # Set position
        dist_line.set_data(list(x), list(y))
        dist_point.set_data([current_time], [new_y])

        # Calculate velocity
        if len(x) > MEAN_LAST_POINTS:
            # Fit to last MEAN_LAST_POINTS points
            last_x = np.array(list(x)[-MEAN_LAST_POINTS:])
            last_y = np.array(list(y)[-MEAN_LAST_POINTS:])

            A = np.vstack([last_x, np.ones(len(last_x))]).T

            current_v, _b = np.linalg.lstsq(A, last_y)[0]
        else:
            current_v = 0

        v.append(current_v)

        v_line.set_data(list(x), list(v))
        v_point.set_data([current_time], [current_v])

        # Move time window if necessary
        if current_time > WINDOW_X:
            for i in range(NUM_SUBPLOTS):
                ax[i].set_xlim(current_time - WINDOW_X, current_time)
           
        status_text.set_text('Running')
    else:
        status_text.set_text('Paused')
        
    return dist_line, dist_point, v_line, v_point, status_text

# Spacja - pauza
def on_key_press(event):
    global paused, pause_time
    if event.key == ' ':  # spacebar
        paused = not paused
        if paused:
            pause_time = time.time() - start_time - last_time
        else:
            start_time = time.time() - last_time

# Connect keyboard event
fig.canvas.mpl_connect('key_press_event', on_key_press)

ani = FuncAnimation(fig, update, init_func=init, 
                   interval=SAMPLE_TIME*1000, blit=True)

# ax.legend()
plt.show()
