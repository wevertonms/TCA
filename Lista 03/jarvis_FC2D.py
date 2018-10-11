def pseudoAngle(v1, v2):
    """Returns a pseudo-angle between two vectors v1 and v2
    """
    angle = 0
    n = 0
    for [x, y] in [v1, v2]:
        if (x > 0):
            if (y > 0):  # Primeiro quadrante
                if (x > y):
                    angleH = y / x  # angle formado com a horizontal
                else:
                    angleH = 2 - x / y  # angle formado com a horizontal
            else:  # Quarto quadrante
                if (x > -y):
                    angleH = 8 + y / x  # angle formado com a horizontal
                else:
                    angleH = 6 - x / y  # angle formado com a horizontal
        else:
            if (y > 0):  # Segundo quadrante
                if (-x > y):
                    angleH = 4 + y / x  # angle formado com a horizontal
                else:
                    angleH = 2 - x / y  # angle formado com a horizontal
            else:  # Terceiro quadrante
                if (x > y):
                    angleH = 6 - x / y  # angle formado com a horizontal
                else:
                    angleH = 4 + y / x  # angle formado com a horizontal
        angle = angle + ((-1)**n)*angleH
        n = n + 1
    return angle % 8


def nextPoint(p, i, direction):
    """Returns the id of the next convex hull in the p point set
    """
    lower = 8
    for j in range(0, len(p)):
        if j != i:
            angle = pseudoAngle([p[j][0]-p[i][0], p[j][1]-p[i][1]], direction)
            if (angle < lower):
                lower = angle
                index = j
    return index

def ordenate(point):
    """Returns the point's ordenate
    """
    return point[1]

def jarvis_FC2D(p):
    """Determine the convex hull by the Jarvis' algorithm and shows it in a plot
    """
    chp = []  # Convex hull's points set
    chp.append(min(p, key=ordenate))  # Finds the point with the lowest ordinate
    nextCHP = nextPoint(p, p.index(chp[0]), [1., 0.])  # Finds the next convex 
                                                       # hull's point
    chp.append(p[nextCHP])  # Adds the point to the convex hull points' set
    i = 1
    while (chp[i] != chp[0]):
        direction = [chp[i][0]-chp[i-1][0], chp[i][1]-chp[i-1][1]]
        nextCHP = nextPoint(p, nextCHP, direction)
        chp.append(p[nextCHP])
        i = i + 1
    return chp


from matplotlib.pyplot import plot, draw, show, grid
import random as rand
# Generates random points
p = [[rand.random(), rand.random()] for aux in range(1000)]
# Calls the function that find the convex hull for p
chp = jarvis_FC2D(p)
# Plots the points' set and its convex hull
plot([aux[0] for aux in p], [aux[1] for aux in p], 'bo',
     [aux[0] for aux in chp], [aux[1] for aux in chp], 'k')
# Shows the plots
show(block=False)
