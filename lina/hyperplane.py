from vector import Vector
from line import Line, MyFloat
import message


class HyperPlane(object):

    def __init__(self, dimension=None, normal_vector=None, constant_term=None):
        if not dimension and not normal_vector:
            raise Exception(message.EITHER_DIMENSION_OR_NORMAL_VECTOR_MUST_BE_PROVIDED)
        if not normal_vector:
            self.dimension = dimension
            all_zeros = [0.0]*self.dimension
            normal_vector = Vector(all_zeros)
        else:
            self.dimension = normal_vector.dimension

        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = 0.0
        self.constant_term = float(constant_term)

        self.set_basepoint()

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n.coordinates[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == message.NO_NONZERO_ELEMENTS_FOUND:
                self.basepoint = None
            else:
                raise e

    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == message.NO_NONZERO_ELEMENTS_FOUND:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    def is_parallel(self, plane):
        nv1 = self.normal_vector
        nv2 = plane.normal_vector

        return nv1.is_parallel(nv2)

    def __eq__(self, plane):
        if self.normal_vector.is_zero_vector():
            if not plane.normal_vector.is_zero_vector():
                return False
            else:
                diff = self.constant_term - plane.constant_term
                return MyFloat(diff).is_near_zero()
        elif plane.normal_vector.is_zero_vector():
            return False

        if not self.is_parallel(plane):
            return False
        x = self.basepoint
        y = plane.basepoint
        basepoint_difference = x - y

        return basepoint_difference.is_orthogonal(self.normal_vector)

    def intersection_point(self, plane):
        try:
            a, b = self.normal_vector.coordinates
            c, d = plane.normal_vector.coordinates
            x = d * self.constant_term - b * plane.constant_term
            y = - c * self.constant_term + a * plane.constant_term
            denominator = 1.0 / (a * d - b * c)
            return Vector([x, y]).scalar(denominator)
        except ZeroDivisionError:
            return self if self == plane else None