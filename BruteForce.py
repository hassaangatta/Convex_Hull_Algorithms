import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
import numpy as np
import time as t

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
points = []
plt.title('Brute Force')
global done
done = plt.axes([0.75, 0, 0.2, 0.05])
global random
random = plt.axes([0.1, 0, 0.3, 0.05])
count = 0

def ccw (x1,y1,x2,y2,x3,y3):
  area = (x1*y2) - (x1*y3) - (y1*x2) + (y1*x3) + (x2*y3) - (y2*x3)
  if area > 0:
    return 1
  else:
    return 0

def convex_hull():
    global count
    x_values = []
    y_values = []
    line = None
    temp_line = None
    for i in range(0, len(points)):
        for j in range(0, len(points)):
            if j != i:
                above = 0
                below = 0
                line = Line2D(*zip(points[i],points[j]), color='blue')
                ax.add_line(line)
                fig.canvas.draw()
                count += 1
                plt.pause(0.5)
                for k in range(0, len(points)):
                    if k != i and k != j:      
                        temp_line = Line2D(*zip(points[j],points[k]), color='yellow')
                        ax.add_line(temp_line)
                        fig.canvas.draw()                 
                        if (ccw(points[k][0],points[k][1],points[i][0],points[i][1],points[j][0],points[j][1])):
                            above = above + 1
                        else:
                            below = below + 1
                        plt.pause(0.5)
                        count += 1
                        Line2D.remove(temp_line)
                    if k == len(points) - 1 and ((below == 0) or (above == 0)):
                        x_values = [points[i][0], points[j][0]]
                        y_values = [points[i][1], points[j][1]]
                        perm_line = Line2D(*zip(points[i],points[j]), color='green')
                        ax.add_line(perm_line)
                        fig.canvas.draw()
                Line2D.remove(line)
                plt.pause(0.5)
                count += 1

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
        convex_hull()
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
