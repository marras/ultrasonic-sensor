import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

x_array = np.arange(-5,5,0.1)

fig = plt.figure(figsize=(7,6.3))
ax = fig.add_subplot(1, 1, 1)

ax.set_ylim(-5,5)

ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_label_coords(1,1.05)
ax.set_xlabel("y")

ax.yaxis.set_label_coords(1,1)
ax.set_ylabel("x", rotation=0)

while (True):
    formula = input("y = ") 

    try:
        y_array = [eval(formula) for x in x_array]
    except (NameError, SyntaxError):
        print("Invalid formula")
        continue

    plt.plot(x_array, y_array)
    plt.show()
    break