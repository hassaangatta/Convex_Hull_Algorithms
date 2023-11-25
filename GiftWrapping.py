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
plt.title('Jarvis March(Gift Wrapping)')
global done
done = plt.axes([0.75, 0, 0.2, 0.05])
global random
random = plt.axes([0.1, 0, 0.3, 0.05])
count = 0

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

def Gift_Wrapping (points):
    global count
    dup_points = points.copy()
    on_hull = min(points,key=lambda p:p[1])
    hull = []
    hull.append(on_hull)
    prev_angle = 0.0
    next_point = (0,0)
    while True:
        dup_points.remove(on_hull)
        temp_lines = []
        angle = 360.0
        for p in points:
            if p == on_hull:
                continue
            if (p in dup_points):
                temp_lines.append(Line2D(*zip(on_hull,p), color='blue'))
                ax.add_line(temp_lines[-1])
                fig.canvas.draw()
                count += 1
                plt.pause(0.5)
            temp_angle = polar_angle(on_hull,p)
            if (angle >= temp_angle and temp_angle >= prev_angle):
                angle = temp_angle
                next_point = p
        for l in temp_lines:
            Line2D.remove(l)
        plt.pause(0.5)
        count += 1
        on_hull = next_point
        prev_angle = angle
        if on_hull == hull[0]:
            line = (Line2D(*zip(hull[-1],hull[0]), color='green'))
            ax.add_line(line)
            fig.canvas.draw()
            plt.pause(0.5)
            count += 1
            break
        hull.append(next_point)
        line = (Line2D(*zip(hull[-2],hull[-1]), color='green'))
        ax.add_line(line)
        fig.canvas.draw()
        plt.pause(0.5)
        count += 1
    # print(hull)
 
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
        start = t.time()
        Gift_Wrapping(points)
        end = t.time()
        total = end - start - (count * 0.5)
        plt.annotate(f'Execution Time = {total:.3f}s', xy=(0, 0), xytext=(1.15, 0.4))
        plt.show()
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
