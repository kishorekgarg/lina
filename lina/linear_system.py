import lina.message as message
from lina.line import Line, MyFloat
from lina.plane import Plane
from copy import deepcopy


class LinearSystem(object):
    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(message.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]

    def multiply_coefficient_and_row(self, coefficient, row):
        normal_vector = self[row].normal_vector
        constant_term = self[row].constant_term

        new_normal_vector = normal_vector.scalar(coefficient)
        new_constant_term = constant_term * coefficient

        self[row] = Plane(new_normal_vector, new_constant_term)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        normal_vector1 = self[row_to_add].normal_vector
        normal_vector2 = self[row_to_be_added_to].normal_vector
        constant_term1 = self[row_to_add].constant_term
        constant_term2 = self[row_to_be_added_to].constant_term

        new_normal_vector = normal_vector1.scalar(coefficient) + normal_vector2
        new_constant_term = constant_term1 * coefficient + constant_term2

        self[row_to_be_added_to] = Plane(new_normal_vector, new_constant_term)

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = Line.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == message.NO_NONZERO_ELEMENTS_FOUND:
                    continue
                else:
                    raise e

        return indices

    def compute_triangular_form(self):
        system = deepcopy(self)
        num_equations = len(system)
        num_variables = system.dimension
        j = 0
        for i in range(num_equations):
            while j < num_variables:
                coefficient = MyFloat(system[i].normal_vector[j])
                if coefficient.is_near_zero():
                    swap_succeeded = system.swap_non_zero_coefficient_row_below(i, j)
                    if not swap_succeeded:
                        j += 1
                        continue
                system.clear_coefficient(i, j)
                j += 1
                break
        return system

    def swap_non_zero_coefficient_row_below(self, row, col):
        num_equations = len(self)

        for i in range(row+1, num_equations):
            coefficient = MyFloat(self[i].normal_vector[col])
            if not coefficient.is_near_zero():
                self.swap_rows(row, i)
                return True
        return False

    def clear_coefficient(self, row, col):
        num_equations = len(self)
        x = MyFloat(self[row].normal_vector[col])

        for i in range(row + 1, num_equations):
            nv = self[i].normal_vector
            y = nv[col]
            z = -y/x
            self.add_multiple_times_row_to_row(z,row, i)

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(message.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret
