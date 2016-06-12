import itertools
from math import (sqrt, acos, pi)
import message


class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError(message.COORDINATES_MUST_NON_EMPTY)

        except TypeError:
            raise TypeError(message.COORDINATES_MUST_ITERABLE)

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def magnitude(self):
        try:
            if not self.coordinates:
                raise ValueError
            return sqrt(sum(x*x for x in self.coordinates))
        except ValueError:
            raise ValueError(message.COORDINATES_MUST_NON_EMPTY)

    def __add__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return Vector(list(x+y for x, y in itertools.izip(self.coordinates, other.coordinates)))
        except ValueError:
            raise ValueError(message.VECTORS_NOT_OF_SAME_DIMENSIONS)

    def __sub__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return Vector(list(x - y for x, y in itertools.izip(self.coordinates, other.coordinates)))
        except ValueError:
            raise ValueError(message.VECTORS_NOT_OF_SAME_DIMENSIONS)

    def __mul__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return Vector(list(x * y for x, y in itertools.izip(self.coordinates, other.coordinates)))
        except ValueError:
            raise ValueError(message.VECTORS_NOT_OF_SAME_DIMENSIONS)

    def scalar(self, scalar):
        self.coordinates = tuple(list(scalar * x for x in self.coordinates))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return Vector(list(x/magnitude for x in self.coordinates))
        except ZeroDivisionError:
            raise Exception(message.ZERO_VECTOR_CAN_NOT_BE_NORMALIZED)

    def dot_product(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return sum(x * y for x, y in itertools.izip(self.coordinates, other.coordinates))
        except ValueError:
            raise ValueError(message.VECTORS_NOT_OF_SAME_DIMENSIONS)

    def get_angle_in_radian(self, other):
        try:
            v = self.normalized()
            w = other.normalized()
            return acos(v.dot_product(w))
        except Exception as e:
            if str(e) == message.ZERO_VECTOR_CAN_NOT_BE_NORMALIZED:
                raise Exception(message.ZERO_VECTOR_CAN_NOT_BE_NORMALIZED)
            else:
                raise e

    def get_angle_in_degree(self, other):
        degree_per_radian = 180./pi
        return self.get_angle_in_radian(other) * degree_per_radian