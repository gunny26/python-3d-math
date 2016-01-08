#!/usr/bin/python
import pygame
import sys
import math
import time
# own modules
import Models3D
from Mesh3D import Mesh3D as Mesh3D
from Vector3D import Vector3D as Vector3D
from Matrix3D import Matrix3D as Matrix3D

# in german Blickwinkel,
# according to wikipedia, for console games played on TV 60degrees
# for notebook/pc display usually something between 90 and 100 degrees
# https://en.wikipedia.org/wiki/Field_of_view_in_video_games
FOV_ANGLE = 100 * math.pi / 180
FOV = 1.0 / math.tan(FOV_ANGLE/2.0)
# how far from the screen is the viewer away
VIEWER_DISTANCE = 1.1

# shift Z in the background
X_SHIFT = 0
Y_SHIFT = 0
Z_SHIFT = 10
SCALE = 1.0
ASPECT_RATIO = 16/9
far = 100.0
near = 1.0

class Thing(object):
    """abstract class to represent mesh of polygons"""

    def __init__(self, surface, origin):
        """
        pygame surface to draw on
        center positon of mesh in 2d space
        """
        self.surface = surface
        (self.origin_x, self.origin_y) = origin
        self.vector = Vector3D(100, 0, 0, 1)
        self.model = Models3D.get_cube_mesh()
        self.center = (surface.get_width() / 2, surface.get_height() / 2)
        self.angle = 0
        self.angle_step = math.pi/180
        self.x_axis = Vector3D(100.0, 0.0, 0.0, 1)
        self.y_axis = Vector3D(0.0, 100.0, 0.0, 1)
        self.z_axis = Vector3D(0.0, 0.0, 100.0, 1)

    def update(self):
        """
        called on every frame
        apply transformation matrix and project every polygon to 2d
        for color avg_z function is used
        polygons are sorted on avg_z value

        finally painting on surface is called
        """
        # Clock vector
        vector = Matrix3D.get_rot_z_matrix(self.angle).v_dot(self.vector)
        # projected = self.__project(self.vector, self.center)
        projected = self.__projectm(vector, self.center)
        pygame.draw.polygon(self.surface, pygame.Color(255,255,255,0), (self.center, projected), 1)
        # Cube
        mesh = self.model.transform(Matrix3D.get_rot_z_matrix(self.angle))
        #mesh = mesh.transform(Matrix3D.get_rot_x_matrix(self.angle))
        mesh = mesh.transform(Matrix3D.get_scale_matrix(SCALE, SCALE, SCALE))
        mesh = mesh.transform(Matrix3D.get_shift_matrix(X_SHIFT, Y_SHIFT, Z_SHIFT))
        for face in mesh:
            vertices = [self.__projectm(vertice, self.center) for vertice in face]
            pygame.draw.polygon(self.surface, pygame.Color(255,255,255,0), vertices, 1)
        self.angle += self.angle_step
        # axis vectors
        pygame.draw.polygon(self.surface, pygame.Color(255,0,0,0), (self.center, self.__projectm(self.x_axis, self.center)), 1)
        pygame.draw.polygon(self.surface, pygame.Color(0,255,0,0), (self.center, self.__projectm(self.y_axis, self.center)), 1)
        pygame.draw.polygon(self.surface, pygame.Color(0,0,255,0), (self.center, self.__projectm(self.z_axis, self.center)), 1)

    @staticmethod
    def __projectm(vector, center):
        """
        called on every frame
        apply transformation matrix and project every polygon to 2d
        for color avg_z function is used
        polygons are sorted on avg_z value

        finally painting on surface is called
        """
        clipping_m = Matrix3D([
            [FOV * ASPECT_RATIO, 0.0, 0.0                            , 0.0],
            [0.0               , FOV, 0.0                            , 0.0],
            [0.0               , 0.0, (far + near) / (far-near)      , (2.0 * near * far) / (near-far)],
            [0.0               , 0.0, 1.0                            , 0.0]
        ])
        new_vector = clipping_m.v_dot(vector)
        new_x = center[0] + new_vector.x * 16.0 / ( 2.0 * new_vector.z) + 8.0
        new_y = center[1] + new_vector.y * 9.0 / ( 2.0 * new_vector.z) + 4.5
        return new_x, new_y
 
    @staticmethod
    def __project(vector, shift_tuple, fov=FOV, viewer_distance=VIEWER_DISTANCE):
        factor = fov / (viewer_distance + vector[2])
        x = vector[0] * factor + shift_tuple[0]
        y = -vector[1] * factor + shift_tuple[1]
        return (x, y)

def test():
    """test"""
    try:
        total_starttime = time.time()
        fps = 25
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        myfont = pygame.font.SysFont("mono", 14)
        objects = (
            Thing(surface, (0, 0)),
        )
        clock = pygame.time.Clock()
        pause = False
        color = pygame.Color(255, 255, 255, 255)
        print "Matrix precalculations done in %s seconds" % (time.time()-total_starttime)
        anim_starttime = time.time()
        frames = 0
        global VIEWER_DISTANCE
        global FOV
        global X_SHIFT
        global Y_SHIFT
        global Z_SHIFT
        global SCALE
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
                elif keyinput[pygame.K_UP]:
                    VIEWER_DISTANCE += 0.1
                elif keyinput[pygame.K_DOWN]:
                    if VIEWER_DISTANCE > 0.1 :
                        VIEWER_DISTANCE -= 0.1
                elif keyinput[pygame.K_PLUS]:
                    FOV += 0.1
                elif keyinput[pygame.K_MINUS]:
                    FOV -= 0.1
                # X/x for X_SHIFT
                elif keyinput[pygame.K_x]:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        X_SHIFT += 0.1
                    else:
                        X_SHIFT -= 0.1
                # Y/y for Y_SHIFT
                elif keyinput[pygame.K_y]:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        Y_SHIFT += 0.1
                    else:
                        Y_SHIFT -= 0.1
                # Z/z for Z_SHIFT
                elif keyinput[pygame.K_z]:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        Z_SHIFT += 0.1
                    else:
                        Z_SHIFT -= 0.1
                # S/s for SCALE
                elif keyinput[pygame.K_s]:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        SCALE += 0.1
                    else:
                        SCALE -= 0.1
                elif keyinput[pygame.K_p]:
                    pause = not pause
                elif keyinput[pygame.K_r]:
                    VIEWER_DISTANCE = 1.0
                    FOV = 0.8
            if pause is not True:
                # clear screen
                surface.fill((0, 0, 0, 255))
                for thing in objects:
                    thing.update()
                text = myfont.render("FOV            : %0.2f" % FOV, 1, (255,255,0))
                surface.blit(text, (10, 10))
                text = myfont.render("VIEWER_DISTANCE: %0.2f" % VIEWER_DISTANCE, 1, (255,255,0))
                surface.blit(text, (10, 24))
                text = myfont.render("X_SHIFT        : %0.2f" % X_SHIFT, 1, (255,255,0))
                surface.blit(text, (10, 38))
                text = myfont.render("Y_SHIFT        : %0.2f" % Y_SHIFT, 1, (255,255,0))
                surface.blit(text, (10, 52))
                text = myfont.render("Z_SHIFT        : %0.2f" % Z_SHIFT, 1, (255,255,0))
                surface.blit(text, (10, 66))
                text = myfont.render("SCALE          : %0.2f" % SCALE, 1, (255,255,0))
                surface.blit(text, (10, 80))
                pygame.display.flip()
            frames += 1
        duration = time.time() - anim_starttime
        print "Done 100 Frames in %f seonds, average %f fps" % (duration, 100/duration)
        print "Whole program duration %f seconds" % (time.time()-total_starttime)
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == "__main__":
    test()
    sys.exit(0)
    import cProfile
    import pstats
    profile = "profiles/%s.profile" % sys.argv[0].split(".")[0]
    cProfile.runctx( "test()", globals(), locals(), filename=profile)
    s = pstats.Stats(profile)
    s.sort_stats('time')
    s.print_stats()

