#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
# own modules
from Vector3D import Vector3D as Vector3D
from Polygon import Polygon as Polygon


class Matrix3D(object):

    def __init__(self, array_data):
        assert len(array_data) == 4
        assert all((len(row) == 4 for row in array_data))
        self.__data =  array_data

    def __str__(self):
        return "\n".join((str(row) for row in self.__data))

    def __repr__(self): 
        return("Matrix3D([%s])" % ", ".join((str(row) for row in self.__data)))

    def __eq__(self, other):
        return all((self.__data[index] == other[index] for index in range(4)))

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.__data[key[0]][key[1]]
        else:
            return self.__data[key]

    @classmethod
    def identity(cls):
        """
        return identity matrix 4x4
        """
        return cls([
            [1,  0, 0, 0],
            [0,  1, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]
        ])

    @classmethod
    def zeros(cls):
        """
        return identity matrix 4x4
        """
        return cls([
            [0,  0, 0, 0],
            [0,  0, 0, 0],
            [0,  0, 0, 0],
            [0,  0, 0, 0]
        ])

    def col(self, colnum):
        """
        little helper to get column vector of matrix
        for column specified by index
        """
        return list((row[colnum] for row in self.__data))

    def row(self, rownum):
        """
        little helper to get column vector of matrix
        for column specified by index
        """
        return self.__data[rownum]

    def transpose(self):
        """
        return transposed version of self

        | a1  b1  c1  d1 |T    | a1  a2  a3  a4 |
        | a2  b2  c2  d2 |  =  | b1  b2  b3  b4 |
        | a3  b3  c3  d3 |     | c1  c2  c3  c4 |
        | a4  b4  c4  d4 |     | d1  d2  d3  d4 |
        """
        new_data = []
        for colnum in range(4):
           new_data.append(self.col(colnum))
        return Matrix3D(new_data)

    def dot(self, other):
        """ 
        return dot product of these to 4x4 matrices
        Matrix A : self
        Matrix B : other

        TODO: find a way to describe this in short terms

        | a11 | a12 | a13 | a14 |   | b11 | b12 | b13 | b14 |   | row[1].col[1] row[1].col[2] ... ... |
        | a21 | a22 | a23 | a24 | . | b21 | b22 | b23 | b24 | = | row[2].col[1] row[2].col[2] ... ... |
        | a31 | a32 | a33 | a34 |   | b31 | b32 | b33 | b34 |   | ...           ...                   |
        | a41 | a42 | a43 | a44 |   | b41 | b42 | b43 | b44 |   |                                     |
        """
        assert isinstance(other, Matrix3D)
        ret_matrix = self.zeros()
        for rownum in range(4):
            row_vec = Vector3D.from_list(self.row(rownum))
            for colnum in range(4):
                col_vec = Vector3D.from_list(other.col(colnum))
                ret_matrix[rownum][colnum] = row_vec.dot(col_vec)
        return ret_matrix

    def v_dot(self, vector):
        """
        calculate dot product of Matrix3D with inverted(Vector3D)

        | a1 | b1 | c1 | d1 |   | x |   | a1*x + b1*y + c1*z + d1*h |
        | a2 | b2 | c2 | d2 | . | y | = | a2*x + b2*y + c2*z + d2*h |
        | a3 | b3 | c3 | d3 |   | z |   | a3*x + b3*y + c3*z + d3*h |
        | a4 | b4 | c4 | d4 |   | h |   | a4*x + b4*y + c4*z + d4*h |
        """
        assert isinstance(vector, Vector3D)
        ret_data = [0, 0, 0, 0]
        for index in range(4):
            row_vec = Vector3D.from_list(self.__data[index])
            ret_data[index] = row_vec.dot(vector)
        return Vector3D.from_list(ret_data)

    @classmethod
    def get_rot_x_matrix(cls, theta):
        """
        return rotation matrix around X-axis
        return rotated version of self around X-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
        |1     0           0| |x|   |        x        |   |x'|
        |0   cos θ    -sin θ| |y| = |y cos θ - z sin θ| = |y'|
        |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|
        """
        cos = math.cos(theta)
        sin = math.sin(theta)
        return cls([
            [1,    0,   0, 0],
            [0,  cos, -sin, 0],
            [0,  sin, cos, 0],
            [0,    0,   0, 1]
        ])

    @classmethod
    def get_rot_y_matrix(cls, theta):
        """
        return rotated version of self around Y-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
        | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
        |     0    1       0| |y| = |         y        | = |y'|
        |-sin θ    0   cos θ| |z|   |-x sin θ + z cos θ|   |z'|
        """
        cos = math.cos(theta)
        sin =  math.sin(theta)
        # substitute sin with cos, but its not clear if this is faster
        # sin² + cos² = 1
        # sin = sqrt(1.0 - cos)
        return cls([
            [ cos, 0, sin, 0],
            [   0, 1,   0, 0],
            [-sin, 0, cos, 0],
            [   0, 0,   0, 1]
        ])

    @classmethod
    def get_rot_z_matrix(cls, theta):
        """
        return rotated version of self around Z-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/1 4607640/rotating-a-vector-in-3d-space
        |cos θ   -sin θ   0| |x|   |x cos θ - y sin θ|   |x'|
        |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
        |  0       0      1| |z|   |        z        |   |z'|
        """
        cos = math.cos(theta)
        sin = math.sin(theta)
        return cls([
            [cos, -sin, 0, 0],
            [sin,  cos, 0, 0],
            [  0,    0, 1, 0],
            [  0,    0, 0, 1]
        ])

    @classmethod
    def get_rot_align(cls, vector1, vector2):
        """
        return rotation matrix to rotate vector1 such that

        T(vector1) = vector2

        remember order of vectors:
        vector1 is the vector to be transformed, not vector 2

        so vector1 is aligned with vector2
        to do this efficiently, vector1 and vector2 have to be unit vectors
        look at this website to get detailed explanation of what is done here
        http://www.iquilezles.org/www/articles/noacos/noacos.htm
        """
        # make sure, that both vectors are unit vectors
        # TODO: Performance Issue
        assert isinstance(vector1, Vector3D)
        assert isinstance(vector1, Vector3D)
        assert vector1.length_sqrd() == 1
        assert vector2.length_sqrd() == 1
        cross = vector2.cross(vector1)
        dot = vector2.dot(vector1)
        k = 1.0 / (1.0 + dot)
        return cls([
            [cross[0] * cross[0] * k + dot     , cross[1] * cross[0] * k - cross[2], cross[2] * cross[0] * k + cross[1], 0],
            [cross[1] * cross[1] * k + cross[2], cross[1] * cross[1] * k + dot     , cross[2] * cross[1] * k - cross[0], 0],
            [cross[2] * cross[2] * k - cross[1], cross[1] * cross[2] * k + cross[0], cross[2] * cross[2] * k + dot,      0],
            [                                 0,                                  0,                                     1]
        ])

    @classmethod
    def get_shift_matrix(cls, x, y, z):
        """
        return transformation matrix to shift vector

        | 1  0  0  sx| |x| |x+sx|
        | 0  1  0  sy| |y| |y+sy|
        | 0  0  1  sz|.|z|=|z+sz|
        | 0  0  0   1| |1| |   1|
        """
        return cls([
            [1, 0, 0, x], 
            [0, 1, 0, y], 
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])

    @classmethod
    def get_scale_matrix(cls, x, y, z):
        """
        return transformation matrix to scale vector
        | x  0  0  0|
        | 0  y  0  0|
        | 0  0  z  0|
        | 0  0  0  1|
        """
        return cls([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ])

def get_rectangle_points():
    """basic rectangle vertices"""
    points = (
        Vector3D(-1,  1, 0, 1),
        Vector3D( 1,  1, 0, 1),
        Vector3D( 1, -1, 0, 1),
        Vector3D(-1, -1, 0, 1),
        Vector3D(-1,  1, 0, 1),
    )
    return points

def get_triangle_points():
    """basic triangle vertices"""
    points = (
        Vector3D(-1,  0, 0, 1),
        Vector3D( 0,  1, 0, 1),
        Vector3D( 1,  0, 0, 1),
        Vector3D(-1,  0, 0, 1),
    )
    return points

def get_pyramid_polygons():
    polygons = []
    # front
    face = get_triangle_points()
    transform = get_shift_matrix(0, 0, 1).dot(get_rot_x_matrix(-math.pi/4))
    face = face.dot(transform)
    face = face.dot(get_shift_matrix(0, 0, 1))
    polygons.append(Polygon(face))
    # back
    face = get_triangle_points()
    face = face.dot(get_rot_x_matrix(math.pi/4))
    face = face.dot(get_shift_matrix(0, 0, -1))
    polygons.append(Polygon(face))
    # left
    face = get_triangle_points()
    face = face.dot(get_rot_x_matrix(-math.pi/4))
    face = face.dot(get_rot_y_matrix(-math.pi/2))
    face = face.dot(get_shift_matrix(1, 0, 0))
    polygons.append(Polygon(face))
    # right
    face = get_triangle_points()
    face = face.dot(get_rot_x_matrix(-math.pi/4))
    face = face.dot(get_rot_y_matrix(math.pi/2))
    face = face.dot(get_shift_matrix(-1, 0, 0))
    polygons.append(face)
    return polygons

def get_cube_polygons():
    # a cube consist of six faces
    # left
    polygons = []
    rec = Polygon(get_rectangle_points())
    t = get_shift_matrix(-1, 0, 0).dot(get_rot_y_matrix(math.pi/2))
    polygons.append(rec.transform(t))
    # right
    t = get_shift_matrix(1, 0, 0).dot(get_rot_y_matrix(math.pi/2))
    polygons.append(rec.transform(t))
    # bottom
    t = get_shift_matrix(0, -1, 0).dot(get_rot_x_matrix(math.pi/2))
    polygons.append(rec.transform(t))
    # top
    t = get_shift_matrix(0, 1, 0).dot(get_rot_x_matrix(math.pi/2))
    polygons.append(rec.transform(t))
    # front
    t = get_shift_matrix(0, 0, -1)
    polygons.append(rec.transform(t))
    # back
    t = get_shift_matrix(0, 0, 1)
    polygons.append(rec.transform(t))
    return polygons

def get_scale_rot_matrix(scale_tuple, aspect_tuple, shift_tuple):
    """
    create a affine transformation matrix

    scale is of type tuple (200, 200, 1)
    shift is of type tuple (0, 0, -10)
    degreees of type tuple for everx axis steps in degrees
    aspect of type tuple to correct aspect ratios
    steps is of type int

    rotates around x/y/z in 1 degree steps and precalculates
    360 different matrices
    """
    aspect_ratio = aspect_tuple[0] / aspect_tuple[1]
    scale_matrix = get_scale_matrix(*scale_tuple)
    shift_matrix = get_shift_matrix(*shift_tuple)
    alt_basis = (
        (1, 0, 0, 0),
        (0, aspect_ratio, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1)
    )
    # TODO : majke inversion function
    alt_basis_inv = np.linalg.inv(alt_basis)
    # combine scale and change of basis to one transformation
    # static matrix
    # TODO : make dot function for matrices
    static_transformation = shift_matrix.dot(alt_basis_inv.dot(scale_matrix))
    return static_transformation

def get_rot_matrix(static_transformation, degrees, steps):
    """
    static_transformation of type Matrix3d, will be applied to every step
    degrees of type tuple, for every axis one entry in degrees
    steps of type int, how many steps to precalculate
    """
    deg2rad = math.pi / 180
    transformations = []
    for step in range(steps):
        factor = step * deg2rad
        angle_x = degrees[0] * factor
        angle_y = degrees[1] * factor
        angle_z = degrees[2] * factor
        # this part of tranformation is calculate for every step
        transformation = get_rot_z_matrix(angle_z).dot(
                get_rot_x_matrix(angle_x).dot(
                    get_rot_y_matrix(angle_y)))
        # combine with static part of transformation,
        # which does scaling, shifting and aspect ration correction
        # to get affine transformation matrix
        transformation = static_transformation.dot(transformation)
        transformations.append(transformation)
    return transformations
