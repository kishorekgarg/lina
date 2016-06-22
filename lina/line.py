from vector import Vector
import message


class Line(object):

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
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

    def is_parallel(self, line):
        nv1 = self.normal_vector
        nv2 = line.normal_vector

        return nv1.is_parallel(nv2)

    def __eq__(self, line):
        if self.normal_vector.is_zero_vector():
            if not line.normal_vector.is_zero_vector():
                return False
            else:
                diff = self.constant_term - line.constant_term
                return MyFloat(diff).is_near_zero()
        elif line.normal_vector.is_zero_vector():
            return False

        if not self.is_parallel(line):
            return False
        x = self.basepoint
        y = line.basepoint
        basepoint_difference = x - y

        return basepoint_difference.is_orthogonal(self.normal_vector)

    def intersection_point(self, line):
        try:
            A, B = self.normal_vector.coordinates
            C, D = line.normal_vector.coordinates
            x = D * self.constant_term - B * line.constant_term
            y = - C * self.constant_term + A * line.constant_term
            denominator = 1.0 / (A*D - B*C)
            return Vector([x, y]).scalar(denominator)
        except ZeroDivisionError:
            return self if self == line else None

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyFloat(item).is_near_zero():
                return k
        raise Exception(message.NO_NONZERO_ELEMENTS_FOUND)


class MyFloat(float):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps