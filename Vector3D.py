#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import unittest

class Vector3D(object):
    """Vector in R³ with homogeneous part h"""

    def __init__(self, x, y, z, h=1):
        """
        3D coordinates given with x, y, z, homgeneous part is optinals, defaults to 1
        """
        self.__data = [x, y, z, h]
        self.x = self.__data[0]
        self.y = self.__data[1]
        self.z = self.__data[2]
        self.h = self.__data[3]

    @classmethod
    def from_list(cls, data):
        """create class from 4 item tuple"""
        return cls(data[0], data[1], data[2], data[3])

    def __eq__(self, other):
        """test equality"""
        return all((self[index] == other[index] for index in range(4)))

    def nearly_equal(self, other):
        """
        test nearly equality
        special for unittesting, to test if two floating point number are nearly
        equal, up to some degree of error
        """
        return all((abs(self[index] - other[index]) < 0.0001 for index in range(4)))

    def __getitem__(self, key):
        return self.__data[key]

    def __richcmp__(self, other, method):
        if method == 0: # < __lt__
            pass
        elif method == 2: # == __eq__
            return self.x == other.x and self.y == other.y and self.z == other.z and self.h == other.h
        elif method == 4: # > __gt__
            pass
        elif method == 1: # <= lower_equal
            pass
        elif method == 3: # != __ne__
            return self.x != other.x or self.y != other.y or self.z != other.z or self.h != other.h
        elif method == 5: # >= greater equal
            pass

    def __len__(self):
        """list interface"""
        return 4

    def __getitem__(self, key):
        """list interface"""
        return self.__data[key]

    def __setitem__(self, key, value):
        """list interface"""
        self.__data[key] = value

    def __repr__(self):
        """object representation"""
        return "Vector3D(%(x)f, %(y)f, %(z)f, %(h)f)" % self.__dict__

    def __str__(self):
        """string output"""
        return "[%(x)f, %(y)f, %(z)f, %(h)f]" % self.__dict__

    def __add__(self, other):
        """
        vector addition with another Vector class
        does not add up homogeneous part
        """
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z, self.h)

    def __iadd__(self, other):
        """
        vector addition with another Vector class implace
        does not add up homogeneous part
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        """
        vector addition with another Vector class
        ignores homogeneous part
        """
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z, self.h)

    def __isub__(self, other):
        """
        vector addition with another Vector class implace
        ignores homogeneous part
        """
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, scalar):
        """
        multiplication with scalar
        ignores homogeneous part
        """
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar, self.h)

    def __imul__(self, scalar):
        """
        multiplication with scalar inplace
        ignores homogeneous part
        """
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self

    def __div__(self, scalar):
        """
        division with scalar
        ignores homogeneous part
        """
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar, self.h)

    def __idiv__(self, scalar):
        """
        vector addition with another Vector class
        ignores homogeneous part
        """
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self

    def length(self):
        """return length of vector"""
        return math.sqrt(self.x **2 + self.y ** 2 + self.z ** 2)

    def length_sqrd(self):
        """retrun length squared"""
        return self.x **2 + self.y ** 2 + self.z ** 2

    def dot(self, other):
        """
        homogeneous version, adds also h to dot product

        this version is used in matrix multiplication

        dot product of self and other vector
        dot product is the projection of one vector to another,
        for perpendicular vectors the dot prduct is zero
        for parallell vectors the dot product is the length of the other vector
        """
        dotproduct = self.x * other.x + self.y * other.y + self.z * other.z + self.h * other.h
        return dotproduct

    def dot3(self, other):
        """
        this is the non-homogeneous dot product of self and other,
        h is set to zero

        dot product of self and other vector
        dot product is the projection of one vector to another,
        for perpedicular vectors the dot prduct is zero
        for parallell vectors the dot product is the length of the other vector

        the dot product of two vectors represents also the sin of the angle
        between these two vectors.
        the dot product represents the projection of other onto self

        dot product = cos(theta)

        so theta could be calculates as
        theta = acos(dot product)
        """
        dotproduct = self.x * other.x + self.y * other.y + self.z * other.z
        return dotproduct

    def cross(self, other):
        """
        cross product of self and other vector
        the result is a new perpendicular vector to self and other

        the length of the new vector is defined as
        |cross product| = |self| * |other| * cos(theta)

        so the angle theta between self and other is calculated as follows

        theta = asin(|cross product| / (|self| * | other|))

        if self and other are unit vectors

        |self| = |other| = 1

        this simplifies to

        |cross product| = sin(theta)

        so you can use the cross product of two vectors two
        find the angle between these two vector, possible useful for shading/lightning
        """
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
            self.h)

    def normalized(self):
        """
        return self with length=1, unit vector
        divide every value (x,y,z) by length of vector
        TODO: what about homgeneous part?
        """
        return self / self.length()
    unit = normalized

    def project2d(self, shift_vec):
        """
        project self to 2d
        simply divide x and y with z value
        and transform with valeus from shift_vec
        """
        return (self.x / self.z + shift_vec[0], self.y / self.z + shift_vec[1])

    def project(win_width, win_height, fov, viewer_distance):
        """
        project some vector (vec1) to 2D Screen

        vec1 - vector to project
        win_width - width of window
        win_height - height of screen
        fov - field of view
        viewer-distance - distance ov viewer in front of screen

        returns <tuple> (x, y)
        """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return x, y

    def angle_to(self, other):
        """
        angle between self and other Vector object
        to calculate this, the dot product of self and other is used
        """
        v1 = self.normalized()
        v2 = other.normalized()
        dotproduct = v1.dot(v2)
        return math.acos(dotproduct)

    def angle_to_unit(self, other):
        """this version assumes that these two vectors are unit vectors"""
        return math.acos(self.dot(other))


class TestClass(unittest.TestCase):

    def test_init(self):
        m1 = Vector3D(1, 1, 1, 1)
        m2 = eval(m1.__repr__())
        assert m1 == m2
        m2 = m1 + m1
        m2 =  m2 - m1
        assert m2 == m1
        m1 *= 2
        print m1.normalized()

if __name__ == "__main__":
    unittest.main()
