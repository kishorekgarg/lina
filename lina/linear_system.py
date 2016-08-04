import lina.message as message
from lina.line import Line, MyFloat
from lina.plane import Plane
from copy import deepcopy
from lina.vector import Vector
from lina.hyperplane import HyperPlane


def _get_new_plane(coefficient, plane):
    new_normal_vector = plane.normal_vector.scalar(coefficient)
    return HyperPlane(normal_vector=new_normal_vector,
                      constant_term=coefficient * plane.constant_term)


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
        if isinstance(self.planes[0], HyperPlane):
            self[row] = _get_new_plane(coefficient, self[row])
        else:
            normal_vector = self[row].normal_vector
            constant_term = self[row].constant_term

            new_normal_vector = normal_vector.scalar(coefficient)
            new_constant_term = constant_term * coefficient

            self[row] = Plane(new_normal_vector, new_constant_term)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        if isinstance(self.planes[0], HyperPlane):
            recipient_plane = self[row_to_be_added_to]
            new_plane = _get_new_plane(coefficient, self[row_to_add])
            new_normal_vector = recipient_plane.normal_vector + new_plane.normal_vector
            constant_term = new_plane.constant_term + recipient_plane.constant_term
            self[row_to_be_added_to] = HyperPlane(normal_vector=new_normal_vector,
                                                  constant_term=constant_term)
        else:
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

    def compute_rref(self):
        tf = self.compute_triangular_form()
        num_equations = len(tf)
        pivots = tf.indices_of_first_nonzero_terms_in_each_row()

        for i in range(num_equations)[::-1]:
            j = pivots[i]
            if j < 0:
                continue
            tf.scale_row_coefficient_to_one(i, j)
            tf.clear_coefficient_above(i, j)
        return tf

    def scale_row_coefficient_to_one(self, row, col):
        normal_vector = self[row].normal_vector
        c = 1.0/normal_vector[col]
        self.multiply_coefficient_and_row(c, row)

    def clear_coefficient_above(self, row, col):
        for i in range(row)[::-1]:
            nv = self[i].normal_vector
            c = -(nv[col])
            self.add_multiple_times_row_to_row(c, row, i)

    def compute_solution(self):
        try:
            return self.gaussian_elimination_and_extraction()
        except Exception as e:
            if str(e) == message.NO_SOLUTIONS_MSG or str(e) == message.INF_SOLUTIONS_MSG:
                return str(e)
            else:
                raise e

    def gaussian_elimination_and_extraction(self):
        rref = self.compute_rref()

        rref.check_exceptions()
        num_variables = rref.dimension
        solution_coordinates = [rref.planes[i].constant_term for i in range(num_variables)]
        return Vector(solution_coordinates)

    def check_exceptions(self):
        for plane in self.planes:
            try:
                Line.first_nonzero_index(plane.normal_vector)
            except Exception as e:
                if str(e) == message.NO_NONZERO_ELEMENTS_FOUND:
                    constant_term = MyFloat(plane.constant_term)
                    if not constant_term.is_near_zero():
                        raise Exception(message.NO_SOLUTIONS_MSG)
                else:
                    raise e
        pivots = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in pivots])
        num_variables = self.dimension

        if num_pivots < num_variables:
            raise Exception(message.INF_SOLUTIONS_MSG)

    def compute_parametrized_solution(self):
        try:
            return self.gaussian_elimination_and_parametrized_solution()
        except Exception as e:
            if str(e) == message.NO_SOLUTIONS_MSG:
                return str(e)
            else:
                raise e

    def gaussian_elimination_and_parametrized_solution(self):
        rref = self.compute_rref()

        rref.check_exceptions_for_parametrization()
        direction_vectors = self.get_direction_vectors_for_parametrization()
        basepoint = self.get_basepoint_for_parametrization()
        return Parametrization(basepoint, direction_vectors)

    def check_exceptions_for_parametrization(self):
        for plane in self.planes:
            try:
                Line.first_nonzero_index(plane.normal_vector)
            except Exception as e:
                if str(e) == message.NO_NONZERO_ELEMENTS_FOUND:
                    constant_term = MyFloat(plane.constant_term)
                    if not constant_term.is_near_zero():
                        raise Exception(message.NO_SOLUTIONS_MSG)
                else:
                    raise e

    def get_direction_vectors_for_parametrization(self):
        num_variables = self.dimension
        pivots = self.indices_of_first_nonzero_terms_in_each_row()
        free_variable_indices = set(range(num_variables)) - set(pivots)

        direction_vectors = []

        for free_var in free_variable_indices:
            vector_coords = [0] * num_variables
            vector_coords[free_var] = 1
            for index, plane in enumerate(self.planes):
                pivot_var = pivots[index]
                if pivot_var < 0:
                    break
                vector_coords[pivot_var] = -plane.normal_vector[free_var]

            direction_vectors.append(Vector(vector_coords))

        return direction_vectors

    def get_basepoint_for_parametrization(self):
        num_variables = self.dimension
        pivots = self.indices_of_first_nonzero_terms_in_each_row()

        basepoint_coords = [0] * num_variables

        for index, plane in enumerate(self.planes):
            pivot_var = pivots[index]
            if pivot_var < 0:
                break
            basepoint_coords[pivot_var] = plane.constant_term

        return Vector(basepoint_coords)

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


class Parametrization(object):
    def __init__(self, basepoint, direction_vectors):
        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for vector in direction_vectors:
                assert vector.dimension == self.dimension
        except AssertionError:
            raise Exception(message.BASE_POINT_AND_DIRECTION_VECTOR_DIMENSION_NOT_SAME)

    def __str__(self):
        output = ''
        for coord in range(self.dimension):
            output += 'x_{} = {} '.format(coord + 1,
                                          round(self.basepoint[coord], 3))
            for free_var, vector in enumerate(self.direction_vectors):
                output += '+ {} t_{}'.format(round(vector[coord], 3),
                                             free_var + 1)
            output += '\n'
        return output

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            for v1, v2 in zip(self.direction_vectors, other.direction_vectors):
                if v1 != v2:
                    return False
            if not (self.basepoint == other.basepoint):
                return False
            return True
        else:
            return False
