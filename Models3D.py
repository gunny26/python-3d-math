#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
# own modules
from Mesh3D import Mesh3D as Mesh3D
from Matrix3D import Matrix3D as Matrix3D
from Vector3D import Vector3D as Vector3D

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
    transform = Matrix3D.get_shift_matrix(0, 0, 1).dot(Matrix3D.get_rot_x_matrix(-math.pi/4))
    face = face.dot(transform)
    face = face.dot(Matrix3D.get_shift_matrix(0, 0, 1))
    polygons.append(Polygon(face))
    # back
    face = get_triangle_points()
    face = face.dot(Matrix3D.get_rot_x_matrix(math.pi/4))
    face = face.dot(Matrix3D.get_shift_matrix(0, 0, -1))
    polygons.append(Polygon(face))
    # left
    face = get_triangle_points()
    face = face.dot(Matrix3D.get_rot_x_matrix(-math.pi/4))
    face = face.dot(Matrix3D.get_rot_y_matrix(-math.pi/2))
    face = face.dot(Matrix3D.get_shift_matrix(1, 0, 0))
    polygons.append(Polygon(face))
    # right
    face = get_triangle_points()
    face = face.dot(Matrix3D.get_rot_x_matrix(-math.pi/4))
    face = face.dot(Matrix3D.get_rot_y_matrix(math.pi/2))
    face = face.dot(Matrix3D.get_shift_matrix(-1, 0, 0))
    polygons.append(face)
    return polygons

def get_cube_polygons():
    # a cube consist of six faces
    # left
    polygons = []
    rec = Mesh3D(get_rectangle_points())
    t = Matrix3D.get_shift_matrix(-1, 0, 0).dot(Matrix3D.get_rot_y_matrix(math.pi/2))
    polygons += rec.transform(t)
    # right
    t = Matrix3D.get_shift_matrix(1, 0, 0).dot(Matrix3D.get_rot_y_matrix(math.pi/2))
    polygons += rec.transform(t)
    # bottom
    t = Matrix3D.get_shift_matrix(0, -1, 0).dot(Matrix3D.get_rot_x_matrix(math.pi/2))
    polygons += rec.transform(t)
    # top
    t = Matrix3D.get_shift_matrix(0, 1, 0).dot(Matrix3D.get_rot_x_matrix(math.pi/2))
    polygons += rec.transform(t)
    # front
    t = Matrix3D.get_shift_matrix(0, 0, -1)
    polygons += rec.transform(t)
    # back
    t = Matrix3D.get_shift_matrix(0, 0, 1)
    polygons += rec.transform(t)
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
