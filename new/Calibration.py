
import platform

import numpy
from numpy import linalg
from scipy.linalg import svd,lstsq

class Translator:

    def __init__(self):
        self.display = []
        self.leap = []

    def add_point(self, display, leap):
        self.display.append(display)
        self.leap.append(leap)

    def calculate(self):
        A = numpy.zeros((3,3))
        A[0] = self.BR - self.BL
        A[1] = self.TL - self.BL
        A[2] = numpy.cross(A[0], A[1])
        A[2] /= numpy.linalg.norm(A[2])

        self.A = numpy.linalg.inv(A)

    def project(self, p):
        q = p
        p = self.BL
        n = self.A[2]

        q_proj = q - numpy.dot(q - p, n) * n
        return q_proj

    def get_z(self, p):
        p = numpy.array(p)
        proj = self.project(p)
        d = proj - p
        r = -1 if d[2] > 0 else 1 
        return numpy.linalg.norm(d) * r

    # Calculate borders from points
    def attempt_calibration(self, points, corner):
        center = numpy.average(points, axis=0)
        distances = [numpy.linalg.norm(numpy.array(p) - center) for p in points]
        if max(distances) < 4 and len(points) >= 100:
            self.calibratepoints(center, corner)
            return True
        print max(distances)
        return False

    def calibratepoints(self, point, corner):
        if corner == 0:
            self.TL = numpy.array(point)
        elif corner == 1:
            self.TR = numpy.array(point)
        elif corner == 2:
            self.BR = numpy.array(point)
        elif corner == 3:
            self.BL = numpy.array(point)

    def finalizecalibration(self):
        self.calculate()
        self.find_homography()

    def leaptransform(self, p):
        r = self.apply_homography(p[:2])
        return r[0], r[1], self.get_z(p)
        #return [self.get_x(p), self.get_y(p), self.get_z(p)]

    def find_homography(self):
        pb = numpy.array([[0,1], [1,1], [1,0], [0,0]]).astype(numpy.float)
        pa = numpy.array([self.TL[:2], self.TR[:2], self.BR[:2], self.BL[:2]]).astype(numpy.float)
        
        matrix = []
        for a0, b0 in zip(pa, pb):
            matrix.append([a0[0], a0[1], 1, 0, 0, 0, -b0[0]*a0[0], -b0[0]*a0[1]])
            matrix.append([0, 0, 0, a0[0], a0[1], 1, -b0[1]*a0[0], -b0[1]*a0[1]])

        A = numpy.matrix(matrix, dtype=numpy.float)
        B = numpy.array(pb).reshape(8)

        self.H = linalg.solve(A, B)
        # res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        # self.H = numpy.array(res).reshape(8)
        # print self.H

    def apply_homography(self, pt):
        T = self.H
        x = (T[0] * pt[0] + T[1] * pt[1] + T[2]) / (T[6] * pt[0] + T[7] * pt[1] + 1)
        y = (T[3] * pt[0] + T[4] * pt[1] + T[5]) / (T[6] * pt[0] + T[7] * pt[1] + 1)
        return x, y
