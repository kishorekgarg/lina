import unittest
from lina.linear_system import LinearSystem
from lina.plane import Plane
from lina.vector import Vector


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

if __name__ == '__main__':
    unittest.main()