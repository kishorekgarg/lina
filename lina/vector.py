import itertools
from math import (sqrt, acos, pi, fabs)
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
        return Vector(list(scalar * x for x in self.coordinates))

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

    def angle_in_radian(self, other):
        try:
            v = self.normalized()
            w = other.normalized()
            return acos(v.dot_product(w))
        except Exception as e:
            if str(e) == message.ZERO_VECTOR_CAN_NOT_BE_NORMALIZED:
                raise Exception(message.ZERO_VECTOR_CAN_NOT_BE_NORMALIZED)
            else:
                raise e

    def angle_in_degree(self, other):
        degree_per_radian = 180./pi
        return self.angle_in_radian(other) * degree_per_radian

    def is_parallel(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return self.is_zero_vector() or other.is_zero_vector() or self.angle_in_radian(other) == 0 or \
                   self.angle_in_radian(other) == pi
        except ValueError:
            raise ValueError(message.VECTORS_NOT_OF_SAME_DIMENSIONS)

    # Threshold is being used here to remove false negative
    # which will be encountered because of approx zero values of vectors
    def is_zero_vector(self, threshold=1e-10):
        return self.magnitude() < threshold

    def is_orthogonal(self, other, threshold=1e-10):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return fabs(self.dot_product(other)) < threshold
        except ValueError:
            raise ValueError(message.VECTORS_NOT_OF_SAME_DIMENSIONS)

    def projection(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return self.dot_product(other.normalized())
        except ValueError:
            raise ValueError(message.VECTORS_NOT_OF_SAME_DIMENSIONS)

    def projection_parallel_component(self, other):
        try:
            other_normalized = other.normalized()
            return other_normalized.scalar(self.projection(other))
        except Exception as e:
            if str(e) == message.ZERO_VECTOR_CAN_NOT_BE_NORMALIZED:
                raise Exception(message.NO_UNIQUE_PARALLEL_COMPONENT_OF_PROJECTION)
            else:
                raise e

    def projection_orthogonal_component(self, other):
        try:
            return self - self.projection_parallel_component(other)
        except Exception as e:
            if str(e) == message.NO_UNIQUE_PARALLEL_COMPONENT_OF_PROJECTION:
                raise Exception(message.NO_UNIQUE_ORTHOGONAL_COMPONENT_OF_PROJECTION)
            else:
                raise e


