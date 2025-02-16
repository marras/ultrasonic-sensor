import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import uniform
from collections import deque
import numpy as np
import time
from measure import distance

# Add pause state
paused = False

SPEED = 20 ##### will be experimental
WINDOW_X = 5
SAMPLE_TIME = 0.1
NOISE = 1.5
MEAN_LAST_POINTS = 5


# Create figure and subplot
fig, ax = plt.subplots(2)
ax[0].set_xlim(0, WINDOW_X)
ax[0].set_ylim(-1, 100)
ax[0].set_xlabel('Czas [s]')
ax[0].set_ylabel('Odległość [cm]')
ax[0].set_title('Odległość od czujnika ultradźwiękowego')

ax[1].set_xlim(0, WINDOW_X)
ax[1].set_ylim(-20, 50)
ax[1].set_xlabel('Czas [s]')
ax[1].set_ylabel('Prędkość [cm/s]')
ax[1].set_title('Prędkość chwilowa')


# Add status text
status_text = ax[0].text(0.02, 0.99, 'Running', transform=ax[0].transAxes)

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
    line.set_data([], [])
    point.set_data([], [])
    v_line.set_data([], [])
    v_point.set_data([], [])
    return line, point, v_line,v_point, status_text


def get_new_distance(current_time):
    # Random
    #return min(current_time * SPEED, 90) + uniform(-NOISE, NOISE)

    return distance()

    # TODO: Get actual distance from sensor

def update(frame):
    global last_time, pause_time
    
    if not paused:
        current_time = time.time() - start_time - pause_time
        last_time = current_time
        
        x.append(current_time)

        new_y = get_new_distance(current_time)
                
        y.append(new_y)

        # Set position
        line.set_data(list(x), list(y))
        point.set_data([current_time], [new_y])

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
            ax[0].set_xlim(current_time - WINDOW_X, current_time)
            ax[1].set_xlim(current_time - WINDOW_X, current_time)

        status_text.set_text('Running')
    else:
        status_text.set_text('Paused')
        
    return line, point, v_line, v_point, status_text

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

line, = ax[0].plot([], [], 'b-', label='Położenie')
point, = ax[0].plot([], [], 'ro', label='Nowy punkt')

v_line, = ax[1].plot([], [], 'b-', label='Prędkość')
v_point, = ax[1].plot([], [], 'ro', label='Nowy punkt 2')


ani = FuncAnimation(fig, update, init_func=init, 
                   interval=SAMPLE_TIME*1000, blit=True)

# ax.legend()
plt.show()
