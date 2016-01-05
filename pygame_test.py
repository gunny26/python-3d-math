#!/usr/bin/python3

import pygame
import sys
import math
import time
# own modules
import Models3D
from Mesh3D import Mesh3D as Mesh3D
from Vector3D import Vector3D as Vector3D
from Matrix3D import Matrix3D as Matrix3D

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
        self.model = Mesh3D(Models3D.get_cube_polygons())
        self.model = Mesh3D(self.model.transform(Matrix3D.get_scale_matrix(10, 10, 1)))
        self.center = (surface.get_width() / 2, surface.get_height() / 2)

    def update(self):
        """
        called on every frame
        apply transformation matrix and project every polygon to 2d
        for color avg_z function is used
        polygons are sorted on avg_z value

        finally painting on surface is called
        """
        self.vector = Matrix3D.get_rot_z_matrix(math.pi/180).v_dot(self.vector)
        self.model = Mesh3D(self.model.transform(Matrix3D.get_rot_z_matrix(math.pi/90)))
        #self.vector = Matrix3D.get_rot_y_matrix(math.pi/180).v_dot(self.vector)
        print self.vector
        projected = self.__project(self.vector, self.center)
        pygame.draw.polygon(self.surface, pygame.Color(255,255,255,0), (self.center, projected), 1)
        pygame.draw.polygon(self.surface, pygame.Color(255,255,255,0), self.model.projected(self.center), 1)

    @staticmethod
    def __project(vector, shift_tuple, fov=0.8, viewer_distance=1):
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
        objects = (
            Thing(surface, (0, 0)),
        )
        clock = pygame.time.Clock()       
        pause = False
        color = pygame.Color(255, 255, 255, 255)
        print "Matrix precalculations done in %s seconds" % (time.time()-total_starttime)
        anim_starttime = time.time()
        frames = 0
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
                if keyinput[pygame.K_UP]:
                    viewer_distance += 1
                if keyinput[pygame.K_DOWN]:
                    viewer_distance -= 1
                if keyinput[pygame.K_PLUS]:
                    fov += .1
                if keyinput[pygame.K_MINUS]:
                    fov -= .1
                if keyinput[pygame.K_p]:
                    pause = not pause
                if keyinput[pygame.K_r]:
                    viewer_distance = 256
                    fov = 2
            if pause is not True:
                # clear screen
                surface.fill((0, 0, 0, 255))
                for thing in objects:
                    thing.update()
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

