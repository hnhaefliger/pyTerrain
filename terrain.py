import graphics.engine
import perlin

############ Display variables

scale = 7
distance = 40

############ Land size

width = 100
length = 50

############ Noise variables

noise1 = perlin.noise(width, length) # landmass / mountains
noise2 = perlin.noise(width, length) # boulders
noise3 = perlin.noise(width, length) # rocks

n1div = 20 # landmass distribution
n2div = 3 # boulder distribution
n3div = 2 # rock distribution

n1scale = 20 # landmass height
n2scale = 3 # boulder scale
n3scale = 1 # rock scale

############ 3D shapes

points = []
triangles = []

############

def color(a, b, c): # check land type
    z = (points[a][2] + points[b][2] + points[c][2]) / 3 # calculate average height of triangle
    if z <= 0:
        return 'blue'
    elif z < 1:
        return 'yellow'
    else:
        return 'green'

for x in range(-int(width/2), int(width/2)):
    for y in range(-int(length/2), int(length/2)):
        z = noise1.perlin((x + width/2) / n1div, (y + width/2) / n1div) * n1scale # add landmass
        z += noise2.perlin((x + width/2) / n2div, (y + width/2) / n2div) * n2scale # add boulders
        z += noise3.perlin((x + width/2) / n3div, (y + width/2) / n3div) * n3scale # add rocks
        points.append([x, y, -z if z <= 0 else 0]) 

for x in range(width):
    for y in range(length):
        if 0 < x and 0 < y:
            a, b, c = int(x * length + y), int(x * length + y - 1), int((x - 1) * length + y) # find 3 points in triangle
            triangles.append([a, b, c, color(a, b, c)])
                
        if x < width - 1 and y < length - 1:
            a, b, c, = int(x * length + y), int(x * length + y + 1), int((x + 1) * length + y) # find 3 points in triangle
            triangles.append([a, b, c, color(a, b, c)])

############

test = graphics.engine.Engine3D(points, triangles, scale=scale, distance=distance)
test.rotate('x', -30)
test.render()
