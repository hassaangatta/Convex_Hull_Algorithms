import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
import numpy as np
import math
import time as t

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
points = []
plt.title('Monotone Chain')
global done
done = plt.axes([0.75, 0, 0.2, 0.05])
global random
random = plt.axes([0.1, 0, 0.3, 0.05])
count = 0

def dist(p1, p2):
    x1, y1, x2, y2 = *p1, *p2
    return math.sqrt((y2-y1)**2 + (x2-x1)**2)

def polar_angle(p1, p2):
    dy = p2[1]-p1[1]
    dx = p2[0]-p1[0]
    if (dx == 0 and dy >= 0):
        return 90.0
    elif (dx == 0 and dy < 0):
        return 270.0
    angle = math.degrees(math.atan2(dy, dx))
    if (angle<0):
        angle += 360
    return angle

def ccw (x1,y1,x2,y2,x3,y3):
  area = (x1*y2) - (x1*y3) - (y1*x2) + (y1*x3) + (x2*y3) - (y2*x3)
  if area < 0:
    return -1
  elif area > 0:
    return 1
  else:
    return 0

def Monotone_Chain(points):
    global count
    points = sorted(set(points))
    
    if len(points) <= 1:
        return points
 
    lower = []
    lines = []
    for p in points:
        if (len(lower) >= 2):
            lines.append(Line2D(*zip(lower[-2],lower[-1]),color='blue'))
            ax.add_line(lines[-1])
            fig.canvas.draw()
            plt.pause(0.5)
            count += 1
        while len(lower) >= 2 and ccw(lower[-2][0], lower[-2][1], lower[-1][0], lower[-1][1], p[0], p[1]) <= 0:
            if (len(lines)>=1):
                Line2D.remove(lines[-1])
                lines.pop()
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        if (len(upper) >= 2):
            lines.append(Line2D(*zip(upper[-2],upper[-1]),color='green'))
            ax.add_line(lines[-1])
            fig.canvas.draw()
            plt.pause(0.5)
            count += 1
        while len(upper) >= 2 and ccw(upper[-2][0], upper[-2][1], upper[-1][0], upper[-1][1], p[0], p[1]) <= 0:
            if (len(lines) >=1 ):
                Line2D.remove(lines[-1])
                lines.pop()
            upper.pop()
        upper.append(p)
    
    line = Line2D(*zip(upper[-2],upper[-1]),color='green')
    ax.add_line(line)
    fig.canvas.draw()
    line = Line2D(*zip(lower[-2],lower[-1]),color='blue')
    ax.add_line(line)
    fig.canvas.draw()
    plt.pause(0.5)
    count += 1
    return lower[:-1] + upper[:-1]

def draw_point(x, y):
    ax.scatter(x, y, color='red')
    fig.canvas.draw()

def on_click(event):
    # print(event.name)
    if (event.inaxes == random and event.name == 'button_press_event'):
        for i in range(10):
            points.append((np.random.uniform(0,10),np.random.uniform(0,10)))
            draw_point(points[i][0],points[i][1])
    elif (event.inaxes == done and event.name == 'button_press_event'):
        fig.canvas.mpl_disconnect(cid)  
        done_button.disconnect(cid_done)
        random_button.disconnect(cid_random)
        # print(points)
        start = t.time()
        res = Monotone_Chain(points)
        end = t.time()
        total = end - start - (count * 0.5)
        plt.annotate(f'Execution Time = {total:.3f}s', xy=(0, 0), xytext=(1.15, 0.4))
        plt.show()
        # print(res)
    elif (event.name == 'button_press_event'):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            points.append((x, y))
            # print(f"Clicked at: ({x}, {y})")
            draw_point(x, y)

done_button = Button(done, 'Calculate Hull')
cid_done = done_button.on_clicked(on_click)
random_button = Button(random, 'Generate Random points')
cid_random = random_button.on_clicked(on_click)
cid = fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()

# print("Points:", points)
