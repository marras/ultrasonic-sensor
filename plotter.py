import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np
import time

MEAN_LAST_POINTS = [None, 5, 10]

class Plotter():
    def __init__(self, measure_func, WINDOW_X, NUM_SUBPLOTS, SAMPLE_TIME, MOVE_WINDOW=True):
        self.MOVE_WINDOW = MOVE_WINDOW
        self.measure_func = measure_func
        self.WINDOW_X = WINDOW_X
        self.NUM_SUBPLOTS = NUM_SUBPLOTS
        self.fig, self.ax = plt.subplots(NUM_SUBPLOTS, layout="tight")
        self.SAMPLE_TIME = SAMPLE_TIME

        self.x = deque(maxlen=int(WINDOW_X/SAMPLE_TIME))
        self.y = [deque(maxlen=int(WINDOW_X/SAMPLE_TIME)),deque(maxlen=int(WINDOW_X/SAMPLE_TIME)),deque(maxlen=int(WINDOW_X/SAMPLE_TIME))]

        # Special case for single plot - ax is not an array
        if (NUM_SUBPLOTS == 1):
            line, dist_point = self.init_plot_distance(self.ax)
            
        if (NUM_SUBPLOTS > 1):
            line, dist_point = self.init_plot_distance(self.ax[0])

        drawings = [[line, dist_point]]

        if (NUM_SUBPLOTS >= 2):
            v_line, v_point = self.init_plot_velocity(self.ax[1])
            drawings.append([v_line, v_point])

        if (NUM_SUBPLOTS >= 3):
            a_line, a_point = self.init_plot_acceleration(self.ax[2])
            drawings.append([a_line, a_point])

        # Flatten the list of drawings
        self.drawings = [item for sublist in drawings for item in sublist]


    def init_plot_distance(self, ax):
        ax.set_xlim(0, self.WINDOW_X)
        ax.set_ylim(-1, 100)
        ax.set_xlabel('Czas [s]')
        ax.set_ylabel('Odległość [cm]')
        ax.set_title('Odległość od czujnika ultradźwiękowego')

        line, = ax.plot([], [], 'b-', label='Położenie')
        point, = ax.plot([], [], 'ro', label='Nowy punkt')

        return (line, point)

    def init_plot_velocity(self, ax):
        ax.set_xlim(0, self.WINDOW_X)
        ax.set_ylim(-20, 50)
        ax.set_xlabel('Czas [s]')
        ax.set_ylabel('Prędkość [cm/s]')
        ax.set_title('Prędkość chwilowa')
        
        line, = ax.plot([], [], 'b-', label='Prędkość')
        point, = ax.plot([], [], 'ro', label='Nowy punkt 2')

        return (line, point)

    def init_plot_acceleration(self, ax):
        ax.set_xlim(0, self.WINDOW_X)
        ax.set_ylim(-50, 50)
        ax.set_xlabel('Czas [s]')
        ax.set_ylabel('Przyspieszenie [cm/s]')
        ax.set_title('Przyspieszenie chwilowe')
        
        line, = ax.plot([], [], 'b-', label='Przyspieszenie')
        point, = ax.plot([], [], 'ro', label='Nowy punkt 3')

        return (line, point)

    # Calculate 1st derivative of y with respect to x (= tangent line "a" coefficient)
    def derivative(self, x, y, num_last_points):
        if len(x) > num_last_points:
            # Fit line to last `num_last_points`` points
            last_x = np.array(list(x)[-num_last_points:])
            last_y = np.array(list(y)[-num_last_points:])

            A = np.vstack([last_x, np.ones(len(last_x))]).T

            a, _b = np.linalg.lstsq(A, last_y)[0]
        else:
            a = 0

        return a

    def animate(self, _frame):
        current_time = time.time() - self.start_time
        self.x.append(current_time)

        # Set position
        for i in range(self.NUM_SUBPLOTS):
            if i == 0:
                new_y = self.measure_func(current_time)
            else:
                new_y = self.derivative(self.x, self.y[i-1], MEAN_LAST_POINTS[i])

            self.y[i].append(new_y) # If possible, calculate a new point based on the derivative of the previous plot

            self.drawings[2*i].set_data(list(self.x), list(self.y[i])) # Line
            self.drawings[2*i+1].set_data([current_time], [new_y]) # Point

        # Move time window if necessary
        if current_time > self.WINDOW_X:
            if self.MOVE_WINDOW:
                for i in range(self.NUM_SUBPLOTS):
                    self.ax[i].set_xlim(current_time - self.WINDOW_X, current_time)
            else:
                self.ani.event_source.stop()
            
        return self.drawings

    def run(self):
        self.start_time = time.time()
        self.ani = FuncAnimation(self.fig, self.animate, interval=self.SAMPLE_TIME*1000, blit=True, repeat=False)
        # ax.legend()
        plt.show()

