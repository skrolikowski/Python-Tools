from math import degrees
from pyglet.gl import *
from pybox.containers.stack import Stack
from pybox.math.transform import Transform

transformations = Stack([Transform()])
color = (255, 255, 255, 255)
lineWidth = 1

# ----------------------------
# Graphics state
# ----------------------------

def setColor(*args):
    global color

    if len(args) == 1:
        # color = hexToRgb(args[0])
        pass
    elif len(args) == 3:
        color = (args[0], args[1], args[2], 255)
    elif len(args) == 4:
        color = (args[0], args[1], args[2], args[3])
    else:
        raise AttributeError('Invalid color values passed in definition.')

def getColor():
    global color
    return color

def setLineWidth(width):
    global lineWidth
    lineWidth = width

def getLineWidth():
    global lineWidth
    return lineWidth

# ----------------------------
# Drawing
# ----------------------------

def rectangle(mode, x, y, width, height):
    global color, lineWidth

    # Set line width
    glLineWidth(lineWidth)

    # Enable alpha blending
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Enable line smoothing
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

    if mode == 'fill':
        drawMode = GL_QUADS
    elif mode == 'line':
        drawMode = GL_LINE_LOOP
    else:
        raise AttributeError('Invalid draw mode: use either `fill` or `line`')

    pyglet.graphics.draw(4, drawMode,
        ('v2i', (x, y, x + width, y, x + width, y + height, x, y + height)),
        ('c4B', color * 4)
    )

def ellipse(mode, x, y, rx, ry):
    pass

def circle(mode, x, y, r):
    pass

# ----------------------------
# Coordinate system
# ----------------------------

def push():
    glPushMatrix()
    glLoadIdentity()

def pop():
    glPopMatrix()

def translate(tx, ty, tz = 1.0):
    glTranslatef(tx, ty, tz)

def rotate(angle, ax = 0.0, ay = 0.0, az = 1.0):
    glRotatef(angle, ax / 1, ay / 1, az / 1)

def scale(sx, sy, sz = 1.0):
    glScalef(sx, sy, sz)

def applyTransform(trans):
    current = transformations.pop()
    current.apply(trans)

    transformations.push(current)

def newTransform(x, y, angle, sx, sy, ox, oy, kx, ky):
    transformations.push(Transform(x, y, angle, sx, sy, ox, oy, kx, ky))

def replaceTransform(trans):
    if type(trans) != Transform:
        raise AttributeError('Argument must be of type Transform.')

    transformations.pop()
    transformations.push(trans)

def currentTransform():
    trans = transformations.peek()

    if not trans:
        trans = Transform()

    return trans
