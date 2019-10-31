import graphics.engine
import perlin
import math

############ Display variables

scale = 6
distance = 100

############ Land size

width = 150 # map width
length = 100 # map length

############ Noise variables

n1div = 30 # landmass distribution
n2div = 4 # boulder distribution
n3div = 1 # rock distribution

n1scale = 20 # landmass height
n2scale = 2 # boulder scale
n3scale = 0.5 # rock scale

noise1 = perlin.noise(width / n1div, length / n1div) # landmass / mountains
noise2 = perlin.noise(width / n2div, length / n2div) # boulders
noise3 = perlin.noise(width / n3div, length / n3div) # rocks

############ z modifiers

zroot = 2
zpower = 2.5

############ colors

colors = {
    0: 'blue',
    1: 'yellow',
    20: 'green',
    25: 'gray',
    1000: 'white'
    }

############ 3D shapes

points = []
triangles = []

############

def color(a, b, c): # check land type
    z = (points[a][2] + points[b][2] + points[c][2]) / 3 # calculate average height of triangle
    for color in colors:
        if z <= color:
            return colors[color]
            break

for x in range(-int(width/2), int(width/2)):
    for y in range(-int(length/2), int(length/2)):
        x1 = x + width/2 
        y1 = y + length/2
        z = noise1.perlin(x1 / n1div, y1 / n1div) * n1scale # add landmass
        z += noise2.perlin(x1 / n2div, y1 / n2div) * n2scale # add boulders
        z += noise3.perlin(x1 / n3div, y1 / n3div) * n3scale # add rocks
        if z >= 0:
            z = -math.sqrt(z)
        else:
            z = ((-z) ** (1 / zroot)) ** zpower
        points.append([x, y, z]) 

for x in range(width):
    for y in range(length):
        if 0 < x and 0 < y:
            a, b, c = int(x * length + y), int(x * length + y - 1), int((x - 1) * length + y) # find 3 points in triangle
            triangles.append([a, b, c, color(a, b, c)])
                
        if x < width - 1 and y < length - 1:
            a, b, c, = int(x * length + y), int(x * length + y + 1), int((x + 1) * length + y) # find 3 points in triangle
            triangles.append([a, b, c, color(a, b, c)])

############

world = graphics.engine.Engine3D(points, triangles, scale=scale, distance=distance, width=1400, height=750, title='Terrain')

world.rotate('x', -30)
world.render()

'''
def animate():
    world.clear()
    world.rotate('x', 30)
    world.rotate('z', 0.1)
    world.rotate('x', -30)
    world.render()
    world.screen.window.after(1, animate)
animate()
'''
