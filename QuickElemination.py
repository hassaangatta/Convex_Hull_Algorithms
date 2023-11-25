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
plt.title('Quick Elimination')
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

def is_inside(point, bounding_box):
        x_bb = [bounding_box[0][0],bounding_box[1][0],bounding_box[2][0],bounding_box[3][0]]
        y_bb = [bounding_box[0][1],bounding_box[1][1],bounding_box[2][1],bounding_box[3][1]]
        cross = 0
        for i in range(4):
            x1, y1, x2, y2 = x_bb[i - 1], y_bb[i - 1], x_bb[i], y_bb[i]
            if (x1 <= point[0] < x2 or x2 <= point[0] < x1) and point[1] <= (
                (y2 - y1) / (x2 - x1)
            ) * (point[0] - x1) + y1:
                cross += 1
        return cross % 2 != 0

def calculate_remaing_points(points):
    global count
    candidate_points = points    
    leftmost = min(candidate_points, key=lambda p: p[0])
    candidate_points.remove(leftmost)
    rightmost = max(candidate_points, key=lambda p: p[0])
    candidate_points.remove(rightmost)
    topmost = max(candidate_points, key=lambda p: p[1])
    candidate_points.remove(topmost)
    bottommost = min(candidate_points, key=lambda p: p[1])
    candidate_points.remove(bottommost)

    line = Line2D(*zip(rightmost,topmost), color='yellow')
    ax.add_line(line)
    fig.canvas.draw()
    line = Line2D(*zip(rightmost,bottommost), color='yellow')
    ax.add_line(line)
    fig.canvas.draw()
    line = Line2D(*zip(leftmost,topmost), color='yellow')
    ax.add_line(line)
    fig.canvas.draw()
    line = Line2D(*zip(leftmost,bottommost), color='yellow')
    ax.add_line(line)
    fig.canvas.draw()
    count += 1
    plt.pause(0.5)

    bounding_box = [topmost, leftmost, bottommost, rightmost]

    remaining_points = []

    for point in candidate_points:
        if not is_inside(point,bounding_box):
            remaining_points.append(point)

    for point in bounding_box:
        remaining_points.append(point)

    return remaining_points

def Grahm_Scan(points):
    global count
    hull = []
    p0 = min(points, key=lambda p: p[1])
    hull.append(p0)
    points.remove(p0)
    points.sort(key=lambda p: (polar_angle(p0, p), dist(p0, p)))
    lines = []
    for i in range(len(points)):
        while len(hull) >= 2 and ccw(hull[-2][0],hull[-2][1],hull[-1][0],hull[-1][1],points[i][0],points[i][1]) != 1:
            line = Line2D(*zip(hull[-1],points[i]), color='green')
            ax.add_line(line)
            fig.canvas.draw()
            plt.pause(0.5)
            count += 1
            Line2D.remove(line)
            hull.pop()
            Line2D.remove(lines[-1])
            lines.pop()
            count += 1
            plt.pause(0.5)
        hull.append(points[i])
        if (len(hull) >= 2):
            lines.append(Line2D(*zip(hull[-2],hull[-1]), color='green'))
            ax.add_line(lines[-1])
            fig.canvas.draw()
            count += 1
            plt.pause(0.5)
    lines.append(Line2D(*zip(hull[-1],hull[0]), color='green'))
    ax.add_line(lines[-1])
    fig.canvas.draw()
    count += 1
    plt.pause(0.5)
    return hull

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
        res = calculate_remaing_points(points)
        # print("Remaining Points:", res)
        res = Grahm_Scan(res)
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
