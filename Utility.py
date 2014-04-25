import math

def calculate_normal(rect, point1, vector):
    #lets solve this using the parametric equation
    point2 = (point1[0] + vector[0], point1[1] + vector[1])
    h, k = point1
    p, q = point2
    x1 = p - h
    y1 = q - k
    normal = (1, 0)
    t = 9999999.9999 #a really large number
    if x1 != 0:
        t_temp = math.fabs((rect.right - h)/x1)
        t = t_temp
        t_temp = math.fabs((rect.left - h)/x1)
        if t_temp < t:
            t = t_temp
            normal = (-1, 0)
    if y1 != 0:
        t_temp = math.fabs((rect.bottom - k)/y1)
        if t_temp>=0 and t_temp < t:
            t = t_temp
            normal = (0, 1)
        t_temp = math.fabs((rect.top - k)/y1)
        if t_temp>=0 and t_temp < t:
            t = t_temp
            normal = (0, -1)
    return normal