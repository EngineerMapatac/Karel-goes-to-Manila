import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Manila Grid Dimensions
GRID_SIZE = 10

def draw_cube(x, y, z, size=0.4, color=(0.2, 0.6, 1.0)):
    """Draws a solid colored cube centered at (x, y, z)."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    
    s = size
    glBegin(GL_QUADS)
    # Front
    glVertex3f(-s, -s,  s); glVertex3f( s, -s,  s); glVertex3f( s,  s,  s); glVertex3f(-s,  s,  s)
    # Back
    glVertex3f(-s, -s, -s); glVertex3f(-s,  s, -s); glVertex3f( s,  s, -s); glVertex3f( s, -s, -s)
    # Top
    glVertex3f(-s,  s, -s); glVertex3f(-s,  s,  s); glVertex3f( s,  s,  s); glVertex3f( s,  s, -s)
    # Bottom
    glVertex3f(-s, -s, -s); glVertex3f( s, -s, -s); glVertex3f( s, -s,  s); glVertex3f(-s, -s,  s)
    # Right
    glVertex3f( s, -s, -s); glVertex3f( s,  s, -s); glVertex3f( s,  s,  s); glVertex3f( s, -s,  s)
    # Left
    glVertex3f(-s, -s, -s); glVertex3f(-s, -s,  s); glVertex3f(-s,  s,  s); glVertex3f(-s,  s, -s)
    glEnd()
    glPopMatrix()

def draw_grid():
    """Renders the Manila street intersection grid lines."""
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_LINES)
    for i in range(GRID_SIZE + 1):
        # Horizontal street lines
        glVertex3f(0, 0, i)
        glVertex3f(GRID_SIZE, 0, i)
        # Vertical avenue lines
        glVertex3f(i, 0, 0)
        glVertex3f(i, 0, GRID_SIZE)
    glEnd()

def main():
    pygame.init()
    display = (1000, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Karel Goes to Manila - 3D Prototype")

    # Perspective & Camera Setup
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    # Karel State
    karel_x, karel_z = 0, 0
    beepers = [(2, 3), (5, 5), (7, 1)]

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP and karel_z < GRID_SIZE:
                    karel_z += 1
                elif event.key == K_DOWN and karel_z > 0:
                    karel_z -= 1
                elif event.key == K_LEFT and karel_x > 0:
                    karel_x -= 1
                elif event.key == K_RIGHT and karel_x < GRID_SIZE:
                    karel_x += 1
                elif event.key == K_SPACE:
                    # Pick up beeper
                    if (karel_x, karel_z) in beepers:
                        beepers.remove((karel_x, karel_z))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Angled isometric view positioned relative to grid center
        gluLookAt(
            GRID_SIZE / 2, 12, GRID_SIZE + 8,  # Camera eye position
            GRID_SIZE / 2, 0, GRID_SIZE / 2,   # Look-at center point
            0, 1, 0                            # Up vector
        )

        draw_grid()

        # Draw beepers/tokens (Yellow markers)
        for bx, bz in beepers:
            draw_cube(bx, 0.2, bz, size=0.2, color=(1.0, 0.8, 0.1))

        # Draw Karel (Cyan block)
        draw_cube(karel_x, 0.4, karel_z, size=0.4, color=(0.1, 0.7, 0.9))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()