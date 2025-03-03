import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np
import time
from accel import get_angles

MEAN_LAST_POINTS = [None, 5, 10]

COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

class Plotter():
    def __init__(self, measure_func, 
                 WINDOW_X, NUM_SUBPLOTS, SAMPLE_TIME,
                 WINDOW_Y = [[-1, 100], [-20,50], [-50,50]],
                 MOVE_WINDOW=True):
        self.MOVE_WINDOW = MOVE_WINDOW
        self.measure_func = measure_func
        self.WINDOW_X = WINDOW_X
        self.WINDOW_Y = WINDOW_Y
        self.NUM_SUBPLOTS = NUM_SUBPLOTS
        self.fig, _ = plt.subplots(NUM_SUBPLOTS, layout="tight", figsize=(16, 8))
        self.ax = self.fig.axes
        self.ani = None

        self.SAMPLE_TIME = SAMPLE_TIME

        # We will increase this for every new run in start_new_run()
        self.current_dataset = -1

        self.x = []
        self.y = []

        self.drawings = []


    def start_new_run(self):
        self.current_dataset += 1
        self.x.append(deque(maxlen=int(self.WINDOW_X/self.SAMPLE_TIME)))
        self.y.append([deque(maxlen=int(self.WINDOW_X/self.SAMPLE_TIME)),
                       deque(maxlen=int(self.WINDOW_X/self.SAMPLE_TIME)),
                       deque(maxlen=int(self.WINDOW_X/self.SAMPLE_TIME))])

        # Extend = append but to a flat list
        if (self.NUM_SUBPLOTS >= 1):
            line, dist_point = self.init_plot_distance(self.ax[0])
            self.drawings.extend([line, dist_point])

        if (self.NUM_SUBPLOTS >= 2):
            v_line, v_point = self.init_plot_velocity(self.ax[1])
            self.drawings.extend([v_line, v_point])

        if (self.NUM_SUBPLOTS >= 3):
            a_line, a_point = self.init_plot_acceleration(self.ax[2])
            self.drawings.extend([a_line, a_point])

        self.ax[0].legend()

    def get_color(self):
        return COLORS[self.current_dataset % len(COLORS)]

    def init_plot_distance(self, ax):
        ax.set_xlim(0, self.WINDOW_X)
        ax.set_ylim([-1, 100])
        ax.set_xlabel('Czas [s]')
        ax.set_ylabel('Odległość [cm]')
        ax.set_title('Odległość od czujnika ultradźwiękowego')

        line, = ax.plot([], [], self.get_color() + '-', label='%d. (α = %.0f)' % (self.current_dataset, get_angles()[0]))
        point, = ax.plot([], [], 'ro')

        return (line, point)

    def init_plot_velocity(self, ax):
        ax.set_xlim(0, self.WINDOW_X)
        ax.set_ylim(-20, 50)
        ax.set_xlabel('Czas [s]')
        ax.set_ylabel('Prędkość [cm/s]')
        ax.set_title('Prędkość chwilowa')
        
        line, = ax.plot([], [], self.get_color() + '-', label='Prędkość %d' % self.current_dataset)
        point, = ax.plot([], [], 'ro', label='Nowy punkt 2')

        return (line, point)

    def init_plot_acceleration(self, ax):
        ax.set_xlim(0, self.WINDOW_X)
        ax.set_ylim(-50, 50)
        ax.set_xlabel('Czas [s]')
        ax.set_ylabel('Przyspieszenie [cm/s]')
        ax.set_title('Przyspieszenie chwilowe')
        
        line, = ax.plot([], [], self.get_color() + '-', label='Przyspieszenie %d' % self.current_dataset)
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
    
    def current_x(self):
        return self.x[self.current_dataset]

    def current_y(self):
        return self.y[self.current_dataset]


    def animate(self, _frame):
        current_time = time.time() - self.start_time
        self.current_x().append(current_time)

        # Set position
        for i in range(self.NUM_SUBPLOTS):
            if i == 0:
                new_y = self.measure_func(current_time)
            else:
                new_y = self.derivative(self.current_x(), self.current_y()[i-1], MEAN_LAST_POINTS[i])

            self.current_y()[i].append(new_y) # If possible, calculate a new point based on the derivative of the previous plot

            current_drawing_index = self.current_dataset * self.NUM_SUBPLOTS * 2 + 2*i

            self.drawings[current_drawing_index].set_data(list(self.current_x()), list(self.current_y()[i])) # Line
            self.drawings[current_drawing_index+1].set_data([current_time], [new_y]) # Point

        # Move time window if necessary
        if current_time > self.WINDOW_X:
            if self.MOVE_WINDOW:
                for i in range(self.NUM_SUBPLOTS):
                    self.ax[i].set_xlim(current_time - self.WINDOW_X, current_time)
            else:
                self.pause()
        
        alpha, beta = get_angles() 
        print("α = %.0f°" % alpha)

        return self.drawings

    def pause(self):
        self.ani.event_source.stop()

        if len(self.current_y()[1]) > 0: 
            print("v_avg: %.2f cm/s" % np.mean(self.current_y()[1]))
            print("v_max: %.2f cm/s" % np.max(self.current_y()[1]))
        else:
            print("Not enough data to calculate average velocity.")

    def run(self):
        self.start_new_run()
        self.start_time = time.time()

        if self.ani:
            print("New run started.")
            self.ani.event_source.start()
        else:
            print("Starting first run.", self.SAMPLE_TIME)
            self.ani = FuncAnimation(self.fig, self.animate, interval=self.SAMPLE_TIME*1000, blit=self.MOVE_WINDOW, repeat=False)
            plt.show()

