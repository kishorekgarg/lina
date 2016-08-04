import unittest
from lina.linear_system import LinearSystem, Parametrization
from lina.plane import Plane
from lina.vector import Vector
from decimal import Decimal
from lina.hyperplane import HyperPlane


class LinearSystemTestCase(unittest.TestCase):

    def setUp(self):
        self.p0 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='1')
        self.p1 = Plane(normal_vector=Vector([0.0, 1.0, 0.0]), constant_term='2')
        self.p2 = Plane(normal_vector=Vector([1.0, 1.0, -1.0]), constant_term='3')
        self.p3 = Plane(normal_vector=Vector([1.0, 0.0, -2.0]), constant_term='2')

    def test_linear_system(self):
        s = LinearSystem([self.p0, self.p1, self.p2, self.p3])

        self.assertEqual(s.indices_of_first_nonzero_terms_in_each_row(), [0, 1, 0, 0], 'Index should match')
        self.assertEqual('{},{},{},{}'.format(s[0],s[1],s[2],s[3]),
                         'x_1 + x_2 + x_3 = 1,x_2 = 2,x_1 + x_2 - x_3 = 3,x_1 - 2x_3 = 2', 'Equations should be same')
        self.assertEqual(len(s), 4, 'Number of planes are not the same')
        # print s
        # s[0] = p1
        # print s

    def test_swap_rows(self):
        s = LinearSystem([self.p0, self.p1, self.p2, self.p3])
        s.swap_rows(0, 1)
        result = (s[0] == self.p1 and s[1] == self.p0 and s[2] == self.p2 and s[3] == self.p3)
        self.assertTrue(result, 'test_swap_rows : test case 1 failed')

        s.swap_rows(1, 3)
        result = (s[0] == self.p1 and s[1] == self.p3 and s[2] == self.p2 and s[3] == self.p0)
        self.assertTrue(result, 'test_swap_rows : test case 2 failed')

        s.swap_rows(3, 1)
        result = (s[0] == self.p1 and s[1] == self.p0 and s[2] == self.p2 and s[3] == self.p3)
        self.assertTrue(result, 'test_swap_rows : test case 3 failed')

        s.multiply_coefficient_and_row(1, 0)
        result = (s[0] == self.p1 and s[1] == self.p0 and s[2] == self.p2 and s[3] == self.p3)
        self.assertTrue(result, 'test_swap_rows : test case 4 failed')

        s.multiply_coefficient_and_row(-1, 2)
        result = (s[0] == self.p1 and s[1] == self.p0
                and s[2] == Plane(normal_vector=Vector([-1.0, -1.0, 1.0]), constant_term='-3') and s[3] == self.p3)
        self.assertTrue(result, 'test_swap_rows : test case 5 failed')

        s.multiply_coefficient_and_row(10, 1)
        result = (s[0] == self.p1 and s[1] == Plane(normal_vector=Vector([10.0, 10.0, 10.0]), constant_term='10')
                and s[2] == Plane(normal_vector=Vector([-1.0, -1.0, 1.0]), constant_term='-3') and s[3] == self.p3)
        self.assertTrue(result, 'test_swap_rows : test case 6 failed')

        s.add_multiple_times_row_to_row(0, 0, 1)
        result = (s[0] == self.p1 and s[1] == Plane(normal_vector=Vector([10.0, 10.0, 10.0]), constant_term='10')
                and s[2] == Plane(normal_vector=Vector([-1.0, -1.0, 1.0]), constant_term='-3') and s[3] == self.p3)
        self.assertTrue(result, 'test_swap_rows : test case 7 failed')

        s.add_multiple_times_row_to_row(1, 0, 1)
        result = (s[0] == self.p1 and s[1] == Plane(normal_vector=Vector([10.0, 11.0, 10.0]), constant_term='12')
                and s[2] == Plane(normal_vector=Vector([-1.0, -1.0, 1.0]), constant_term='-3') and s[3] == self.p3)
        self.assertTrue(result, 'test_swap_rows : test case 8 failed')

        s.add_multiple_times_row_to_row(-1, 1, 0)
        result = (s[0] == Plane(normal_vector=Vector([-10.0, -10.0, -10.0]), constant_term='-10')
                and s[1] == Plane(normal_vector=Vector([10.0, 11.0, 10.0]), constant_term='12')
                and s[2] == Plane(normal_vector=Vector([-1.0, -1.0, 1.0]), constant_term='-3') and s[3] == self.p3)
        self.assertTrue(result, 'test_swap_rows : test case 9 failed')

    def test_compute_triangular_form(self):
        p1 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='1')
        p2 = Plane(normal_vector=Vector([0.0, 1.0, 1.0]), constant_term='2')
        s = LinearSystem([p1, p2])
        t = s.compute_triangular_form()
        result = (t[0] == p1 and t[1] == p2)
        self.assertTrue(result, 'test_compute_triangular_form : test case 1 failed')

        p1 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='1')
        p2 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='2')
        s = LinearSystem([p1, p2])
        t = s.compute_triangular_form()
        result = (t[0] == p1 and t[1] == Plane(constant_term='1'))
        self.assertTrue(result, 'test_compute_triangular_form : test case 2 failed')

        p1 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='1')
        p2 = Plane(normal_vector=Vector([0.0, 1.0, 0.0]), constant_term='2')
        p3 = Plane(normal_vector=Vector([1.0, 1.0, -1.0]), constant_term='3')
        p4 = Plane(normal_vector=Vector([1.0, 0.0, -2.0]), constant_term='2')
        s = LinearSystem([p1, p2, p3, p4])
        t = s.compute_triangular_form()
        result = (t[0] == p1 and t[1] == p2 and t[2] == Plane(normal_vector=Vector([0.0, 0.0, -2.0]), constant_term='2')
                  and t[3] == Plane())
        self.assertTrue(result, 'test_compute_triangular_form : test case 3 failed')

        p1 = Plane(normal_vector=Vector([0.0, 1.0, 1.0]), constant_term='1')
        p2 = Plane(normal_vector=Vector([1.0, -1.0, 1.0]), constant_term='2')
        p3 = Plane(normal_vector=Vector([1.0, 2.0, -5.0]), constant_term='3')
        s = LinearSystem([p1, p2, p3])
        t = s.compute_triangular_form()
        result = (t[0] == Plane(normal_vector=Vector([1.0, -1.0, 1.0]), constant_term='2')
                  and t[1] == Plane(normal_vector=Vector([0.0, 1.0, 1.0]), constant_term='1')
                  and t[2] == Plane(normal_vector=Vector([0.0, 0.0, -9.0]), constant_term='-2'))
        self.assertTrue(result, 'test_compute_triangular_form : test case 4 failed')

    def test_compute_rref(self):
        p1 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='1')
        p2 = Plane(normal_vector=Vector([0.0, 1.0, 1.0]), constant_term='2')
        s = LinearSystem([p1, p2])
        r = s.compute_rref()
        result = (r[0] == Plane(normal_vector=Vector([1.0, 0.0, 0.0]), constant_term='-1') and r[1] == p2)
        self.assertTrue(result, 'test_compute_rref : test case 1 failed')

        p1 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='1')
        p2 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='2')
        s = LinearSystem([p1, p2])
        r = s.compute_rref()
        result = (r[0] == p1 and r[1] == Plane(constant_term='1'))
        self.assertTrue(result, 'test_compute_rref : test case 2 failed')

        p1 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='1')
        p2 = Plane(normal_vector=Vector([0.0, 1.0, 0.0]), constant_term='2')
        p3 = Plane(normal_vector=Vector([1.0, 1.0, -1.0]), constant_term='3')
        p4 = Plane(normal_vector=Vector([1.0, 0.0, -2.0]), constant_term='2')
        s = LinearSystem([p1, p2, p3, p4])
        r = s.compute_rref()
        result = (r[0] == Plane(normal_vector=Vector([1.0, 0.0, 0.0]), constant_term='0') and r[1] == p2
                  and r[2] == Plane(normal_vector=Vector([0.0, 0.0, -2.0]), constant_term='2') and r[3] == Plane())
        self.assertTrue(result, 'test_compute_rref : test case 3 failed')

        p1 = Plane(normal_vector=Vector([0.0, 1.0, 1.0]), constant_term='1')
        p2 = Plane(normal_vector=Vector([1.0, -1.0, 1.0]), constant_term='2')
        p3 = Plane(normal_vector=Vector([1.0, 2.0, -5.0]), constant_term='3')
        s = LinearSystem([p1, p2, p3])
        r = s.compute_rref()
        result = (r[0] == Plane(normal_vector=Vector([1.0, 0.0, 0.0]), constant_term=Decimal('23') / Decimal('9'))
                  and r[1] == Plane(normal_vector=Vector([0.0, 1.0, 0.0]), constant_term=Decimal('7') / Decimal('9'))
                  and r[2] == Plane(normal_vector=Vector([0.0, 0.0, 1.0]), constant_term=Decimal('2') / Decimal('9')))
        self.assertTrue(result, 'test_compute_rref : test case 4 failed')

    def test_compute_solution(self):
        # first system
        p1 = Plane(Vector([5.862, 1.178, -10.366]), -8.15)
        p2 = Plane(Vector([-2.931, -0.589, 5.183]), -4.075)
        system1 = LinearSystem([p1, p2])
        self.assertEqual(system1.compute_solution(), 'No solutions', 'There is no solution to this system.')

        # # second system
        p1 = Plane(Vector([8.631, 5.112, -1.816]), -5.113)
        p2 = Plane(Vector([4.315, 11.132, -5.27]), -6.775)
        p3 = Plane(Vector([-2.158, 3.01, -1.727]), -0.831)
        system2 = LinearSystem([p1, p2, p3])
        self.assertEqual(system2.compute_solution(), 'Infinitely many solutions',
                         'There are infinite solutions to this system.')

        # third system
        p1 = Plane(Vector([5.262, 2.739, -9.878]), -3.441)
        p2 = Plane(Vector([5.111, 6.358, 7.638]), -2.152)
        p3 = Plane(Vector([2.016, -9.924, -1.367]), -9.278)
        p4 = Plane(Vector([2.167, -13.543, -18.883]), -10.567)
        system3 = LinearSystem([p1, p2, p3, p4])
        self.assertEqual(system3.compute_solution(),
                         Vector([-1.1772018757899585, 0.707150558138741, -0.08266358490228289]),
                         'Wrong solution computed!')

    def test_compute_parametrized_solution(self):
        p1 = Plane(normal_vector=Vector([0.786, 0.786, 0.588]), constant_term=-0.714)
        p2 = Plane(normal_vector=Vector([-0.131, -0.131, 0.244]), constant_term=0.319)

        system = LinearSystem([p1, p2])
        result = Parametrization(Vector([0.319, 0, 0]), [Vector([0.131, 1, 0]), Vector([-0.244, 0, 1])])
        self.assertEqual(system.compute_parametrized_solution(), result, 'Wrong solution computed!')

        p1 = Plane(Vector([8.631, 5.112, -1.816]), -5.113)
        p2 = Plane(Vector([4.315, 11.132, -5.27]), -6.775)
        p3 = Plane(Vector([-2.158, 3.01, -1.727]), -0.831)

        system = LinearSystem([p1, p2, p3])
        result = Parametrization(Vector([-0.831, 0, 0]), [Vector([-3.01, 1, 0]), Vector([1.727, 0, 1])])
        self.assertEqual(system.compute_parametrized_solution(), result, 'Wrong solution computed!')

        p1 = Plane(Vector([0.935, 1.76, -9.365]), -9.955)
        p2 = Plane(Vector([0.187, 0.352, -1.873]), -1.991)
        p3 = Plane(Vector([0.374, 0.704, -3.746]), -3.982)
        p4 = Plane(Vector([-0.561, -1.056, 5.619]), 5.973)

        system = LinearSystem([p1, p2, p3, p4])
        result = Parametrization(Vector([5.973, 0, 0]), [Vector([1.056, 1, 0]), Vector([-5.619, 0, 1])])
        self.assertEqual(system.compute_parametrized_solution(), result, 'Wrong solution computed!')
        
    def test_hyper_plane(self):
        p1 = HyperPlane(normal_vector=Vector([0.786, 0.786]), constant_term=0.786)
        p2 = HyperPlane(normal_vector=Vector([-0.131, -0.131]), constant_term=-0.131)

        system = LinearSystem([p1, p2])
        self.assertEqual(system.compute_solution(), 'Infinitely many solutions', 'Wrong solution computed!')

        p1 = HyperPlane(normal_vector=Vector([2.102, 7.489, -0.786]),
                        constant_term=-5.113)
        p2 = HyperPlane(normal_vector=Vector([-1.131, 8.318, -1.209]),
                        constant_term=-6.775)
        p3 = HyperPlane(normal_vector=Vector([9.015, 5.873, -1.105]),
                        constant_term=-0.831)

        system = LinearSystem([p1, p2, p3])
        self.assertEqual(system.compute_solution(),
                         Vector([0.3846829686036449, -0.864793338457455, -0.7058953075102014]),
                         'Wrong solution computed!')

        p1 = HyperPlane(normal_vector=Vector([0.786, 0.786, 8.123, 1.111, -8.363]),
                        constant_term=-9.955)
        p2 = HyperPlane(normal_vector=Vector([0.131, -0.131, 7.05, -2.813, 1.19]),
                        constant_term=-1.991)
        p3 = HyperPlane(normal_vector=Vector([9.015, -5.873, -1.105, 2.013, -2.802]),
                        constant_term=-3.982)

        system = LinearSystem([p1, p2, p3])
        self.assertEqual(system.compute_solution(), 'Infinitely many solutions', 'Wrong solution computed!')

if __name__ == '__main__':
    unittest.main()