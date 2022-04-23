import math
import random

from celluloid import Camera
from matplotlib import pyplot as plt

from Point import Point
from Vector import Vector

# Dynamic convex hull algorithm

fig = plt.figure()
camera = Camera(fig)


def det(a, b, c, d):
    return a * d - b * c


# Sector test for convex polygon
def get_point_position_to_convex_polygon(p0: Point, points: list) -> str:
    if get_point_position_to_line(p0, points[0], points[1]) == "right" or \
            get_point_position_to_line(p0, points[0], points[len(points) - 1]) == "left":
        return "out"

    start = 0
    end = len(points) - 1

    while end - start > 1:
        sep = math.floor((start + end) / 2)
        if get_point_position_to_line(p0, points[0], points[sep]) == "left":
            start = sep
        else:
            end = sep

    if get_point_position_to_line(p0, points[start], points[start + 1]) == 'left':
        return 'in'
    else:
        return 'out'


def get_point_position_to_line(p0: Point, p1: Point, p2: Point):
    d = det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)
    if d > 0:
        return "left"
    elif d < 0:
        return "right"
    else:
        return "on the line"


def point_distance(p1: Point, p2: Point):
    return math.sqrt(abs((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y)))


def find_middle_point(p1: Point, p2: Point, p3: Point):
    if Vector(p3, p1) * Vector(p3, p2) <= 0:
        return p3
    elif Vector(p2, p1) * Vector(p2, p3) <= 0:
        return p2
    else:
        return p1


def dynamic_convex_hull(points: list, old_convex_hull: list):

    if len(points) <= 2:
        return points

    if len(points) == 3:
        if get_point_position_to_line(points[0], points[1], points[2]) == "on the line":
            mid_point = find_middle_point(points[0], points[1], points[2])
            if mid_point == points[0]:
                return [points[1], points[2]]
            elif mid_point == points[1]:
                return [points[0], points[2]]
            else:
                return [points[0], points[1]]
        else:
            if get_point_position_to_line(points[2], points[0], points[1]) == "left":
                return [points[0], points[1], points[2]]
            if get_point_position_to_line(points[2], points[0], points[1]) == "right":
                return [points[0], points[2], points[1]]

    if len(points) > 3:
        new_point = points[-1]
        start = -1
        end = -1
        if get_point_position_to_line(new_point, old_convex_hull[-1], old_convex_hull[0]) == "right" \
                and get_point_position_to_line(new_point, old_convex_hull[0], old_convex_hull[1]) == "right":
            for i in range(len(old_convex_hull) - 1):
                if get_point_position_to_line(new_point, old_convex_hull[i], old_convex_hull[i + 1]) == "right":
                    start = i + 1
            end = len(old_convex_hull) - 1
            for i in range(len(old_convex_hull) - 1, start, -1):
                if get_point_position_to_line(new_point, old_convex_hull[i - 1], old_convex_hull[i]) == "right":
                    end = i - 1
            new_hull = old_convex_hull[start:end + 1] + [new_point]
        else:
            old_convex_hull.append(old_convex_hull[0])
            for i in range(len(old_convex_hull) - 1):
                if get_point_position_to_line(new_point, old_convex_hull[i], old_convex_hull[i + 1]) == "right":
                    start = i
                    break
            if start == -1:
                old_convex_hull.pop()
                return old_convex_hull
            for i in range(start, len(old_convex_hull) - 1):
                if get_point_position_to_line(new_point, old_convex_hull[i], old_convex_hull[i + 1]) == "right":
                    end = i + 1
                else:
                    break
            old_convex_hull.pop()
            new_hull = old_convex_hull[0:start + 1] + [new_point] + old_convex_hull[end:len(old_convex_hull)]

        return new_hull


def draw_convex_hull(convex_hull_points: list, color: str):
    for i in range(len(convex_hull_points)):
        plt.plot([convex_hull_points[i].x, convex_hull_points[(i + 1) % len(convex_hull_points)].x],
                 [convex_hull_points[i].y, convex_hull_points[(i + 1) % len(convex_hull_points)].y], color=color)


def draw_point(point: Point):
    plt.scatter(point.x, point.y, color="red")


def draw_points(points: list):
    for i in range(len(points)):
        draw_point(points[i])


def generate_point(points: list):
    points.append(Point(random.randint(0, 30), random.randint(0, 30)))


def init_generation():
    points = []
    convex_hull = []

    for i in range(20):
        generate_point(points)

        is_existed = False
        for j in range(len(points) - 1):
            if points[j] == points[-1]:
                is_existed = True
        if is_existed:
            continue

        draw_points(points)
        # time.sleep(3)
        convex_hull = dynamic_convex_hull(points, convex_hull)
        if len(convex_hull) == 1:
            draw_point(convex_hull[0])
        else:
            draw_convex_hull(convex_hull, "black")
        camera.snap()


def init():
    init_generation()
    plt.grid(True)
    animation = camera.animate(blit=False, interval=300)
    animation.save("animation.gif")
    plt.show()


init()
