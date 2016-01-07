#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import unittest
from Vector3D import Vector3D as Vector3D
from Matrix3D import Matrix3D as Matrix3D

class TestClass(unittest.TestCase):

    def test_init(self):
        m1 = Vector3D(1, 1, 1, 1)
        m2 = eval(m1.__repr__())
        assert m1 == m2
        m2 = m1 + m1
        m2 =  m2 - m1
        assert m2 == m1
        m1 *= 2

    def test_det(self):
        m = Matrix3D.identity()
        print "det(I)=", m.det()
        # for next example look at
        # http://matheguru.com/lineare-algebra/207-determinante.html
        mr = Matrix3D([
            [  5,  0,  3, -1 ],
            [  3,  0,  0,  4 ],
            [ -1,  2,  4, -2 ],
            [  1,  0,  0,  5 ],
        ])
        print "T(mr)=\n", mr.transpose()
        print "det(mr)=", mr.det()
        assert mr.det() == 66
        print "det(T(mr))=", mr.transpose().det()
        assert mr.det() == mr.transpose().det()

    def test_scale(self):
        m = Matrix3D.identity()
        m2 = m.scale(2.0)
        print "2 * I:\n", m2
        m3 = m2.scale(1.0/2.0)
        print "1/2 * ( 2 * I):\n", m3
        assert m3 == m

    def test_inverse(self):
        # for next example look at
        # http://matheguru.com/lineare-algebra/207-determinante.html
        mr = Matrix3D([
            [  5.0,  0.0,  3.0, -1.0 ],
            [  3.0,  0.0,  0.0,  4.0 ],
            [ -1.0,  2.0,  4.0, -2.0 ],
            [  1.0,  0.0,  0.0,  5.0 ],
        ])
        print "inverse(mr) =\n", mr.inverse()
        test_m = Matrix3D([
           [0.0, 0.4545454545454546, 0.0, -0.36363636363636365],
           [-0.6666666666666667, 1.7121212121212122, 0.5, -1.303030303030303],
           [0.33333333333333337, -0.7878787878787878, 0.0, 0.696969696969697],
           [0.0, -0.09090909090909091, 0.0, 0.2727272727272727]
        ])
        assert mr.inverse() == test_m

    def test_transformations(self):
        # test zeros
        m = Matrix3D.zeros()
        assert isinstance(m, Matrix3D)
        # test if __repr__ is able to convert to object
        m1 = eval(m.__repr__())
        assert m == m1
        # test identity
        m = Matrix3D.identity()
        assert isinstance(m, Matrix3D)
        # test __getitem__ interface
        assert m[0, 0] == 1
        assert m[1, 1] == 1
        assert m[2, 2] == 1
        assert m[3, 3] == 1
        # get column vector
        assert m.col(0) == [1, 0, 0, 0]
        m1 = Matrix3D.identity()
        assert m1.dot(Matrix3D.identity()) == Matrix3D.identity()
        assert m1.dot(Matrix3D.zeros()) == Matrix3D.zeros()

    def test_matrix_dot(self):
        """test dot product identity matrix and transpose"""
        mi = Matrix3D.identity()
        # I dot transposed(I) = I
        assert mi == mi.dot(mi.transpose())
        mr = Matrix3D([
            [  1,  2,  3,  4 ],
            [  5,  6,  7,  8 ],
            [  9, 10, 11, 12 ],
            [ 13, 14, 15, 16 ],
        ])
        assert mr.dot(mi) == mr
        test_transposed = Matrix3D([
            [1, 5, 9, 13],
            [2, 6, 10, 14],
            [3, 7, 11, 15],
            [4, 8, 12, 16]
        ])
        assert mr.transpose() == test_transposed
        test_m = Matrix3D([
            [30, 70, 110, 150],
            [70, 174, 278, 382],
            [110, 278, 446, 614],
            [150, 382, 614, 846],
        ])
        assert mr.dot(mr.transpose()) == test_m
        A = Matrix3D([
            [ 3, 0, 0, 0 ],
            [ 0, -1, 0, 0 ],
            [ 0, 0, 2, 0 ],
            [ 0, 0, 0, 1 ]
        ])
        B = Matrix3D([
            [ math.sqrt(3)/2, 0, -1/2, 0 ],
            [ 0, 1, 0, 0 ],
            [ 1/2, 0, math.sqrt(3)/2, 0 ],
            [ 0, 0, 0, 1]
        ])
        C = Matrix3D([
            [1, 0, 0, 3],
            [0, 1, 0, -1],
            [0, 0, 1, 2],
            [0, 0, 0, 1]
        ])
        # testing assosiativeness (A*B)*C == A*(B*C)
        assert A.dot(B).dot(C) == A.dot(B.dot(C))
        # TODO: find reliable result
        #print A.dot(B).dot(C)

    def test_rot_matrices(self):
        m = Matrix3D.get_rot_x_matrix(100)
        assert m.dot(Matrix3D.identity()) == m
        m = Matrix3D.get_rot_y_matrix(100)
        assert m.dot(Matrix3D.identity()) == m
        m = Matrix3D.get_rot_z_matrix(100)
        assert m.dot(Matrix3D.identity()) == m
        # rotate vector only in x-axis around x - nothing should happen
        v1 = Vector3D(1, 0, 0, 1)
        assert Matrix3D.get_rot_x_matrix(100).v_dot(v1) == v1
        v1 = Vector3D(0, 1, 0, 1)
        assert Matrix3D.get_rot_y_matrix(100).v_dot(v1) == v1
        v1 = Vector3D(0, 0, 1, 1)
        assert Matrix3D.get_rot_z_matrix(100).v_dot(v1) == v1
        # rotate vectors really
        v1 = Vector3D(1.0, 0.0, 0.0, 1.0)
        # 90 degrees or pi/2
        real_v = Matrix3D.get_rot_z_matrix(math.pi/2).v_dot(v1)
        test_v = Vector3D.from_list([0.000000, 1.000000, 0.000000, 1.000000])
        assert real_v.nearly_equal(test_v)
        # 180 degrees
        real_v = Matrix3D.get_rot_z_matrix(math.pi).v_dot(v1)
        test_v = Vector3D.from_list([-1.000000, 0.000000, 0.000000, 1.000000])
        assert real_v.nearly_equal(test_v)
        # 270 degrees
        real_v = Matrix3D.get_rot_z_matrix(math.pi + math.pi/2).v_dot(v1)
        test_v = Vector3D.from_list([0.000000, -1.000000, 0.000000, 1.000000])
        assert real_v.nearly_equal(test_v)
        # 360 degrees
        real_v = Matrix3D.get_rot_z_matrix(2 * math.pi).v_dot(v1)
        test_v = Vector3D.from_list([1.000000, 0.000000, 0.000000, 1.000000])
        assert real_v.nearly_equal(test_v)
        # rotate around Y-Axis about 180 degrees
        real_v = Matrix3D.get_rot_y_matrix(math.pi).v_dot(v1)
        test_v = Vector3D.from_list([-1.000000, 0.000000, 0.000000, 1.000000])
        assert real_v.nearly_equal(test_v)
        # rotate y:90 and x:90 -> (0, 1, 0, 1)
        real_v = Matrix3D.get_rot_y_matrix(math.pi/2).v_dot(v1)
        test_v = Vector3D.from_list([0.000000, 0.000000, -1.000000, 1.000000])
        assert real_v.nearly_equal(test_v)
        real_v = Matrix3D.get_rot_x_matrix(math.pi/2).v_dot(real_v)
        test_v = Vector3D.from_list([0.000000, 1.000000, 0.000000, 1.000000])
        assert real_v.nearly_equal(test_v)
        # and this is the combined version
        rot_y = Matrix3D.get_rot_y_matrix(math.pi/2)
        print "rotation around y:\n", rot_y
        rot_x = Matrix3D.get_rot_x_matrix(math.pi/2)
        print "rotation around x:\n", rot_x
        rot_z = Matrix3D.get_rot_z_matrix(math.pi/2)
        print "rotation around z:\n", rot_z
        rot_m = rot_x.dot(rot_y.dot(rot_z))
        print "combined rotation matrix:\n", rot_m
        real_v = rot_m.v_dot(v1)
        print "resulting vector:", real_v
        test_v = Vector3D.from_list([0.000000, 1.000000, 0.000000, 1.000000])
        assert real_v.nearly_equal(test_v)

    def test_m_transforms(self):
        v = Vector3D(1, 1, 0, 1)
        m = Matrix3D.get_shift_matrix(5, 5, 0)
        print "shift matrix:\n", m
        print "shifted vector:", m.v_dot(v)
        m = Matrix3D.get_scale_matrix(2, 2, 0)
        print "scale matrix:\n", m
        print "scaled vector:", m.v_dot(v)

if __name__ == "__main__":
    unittest.main()
