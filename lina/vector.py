import itertools
import math


class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __len__(self):
        try:
            if not self.coordinates:
                raise ValueError
            return math.sqrt(sum(x*x for x in self.coordinates))
        except ValueError:
            raise ValueError('Coordinates are empty')

    def __add__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return Vector(list(x+y for x, y in itertools.izip(self.coordinates, other.coordinates)))
        except ValueError:
            raise ValueError('Both vectors have different dimensions')

    def __sub__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return Vector(list(x - y for x, y in itertools.izip(self.coordinates, other.coordinates)))
        except ValueError:
            raise ValueError('Both vectors have different dimensions')

    def __mul__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError
            return Vector(list(x * y for x, y in itertools.izip(self.coordinates, other.coordinates)))
        except ValueError:
            raise ValueError('Both vectors have different dimensions')

    def scalar(self, scalar):
        self.coordinates = tuple(list(scalar * x for x in self.coordinates))