import unittest
from lina.linear_system import LinearSystem
from lina.plane import Plane
from lina.vector import Vector


class LinearSystemTestCase(unittest.TestCase):

    def test_linear_system(self):
        p0 = Plane(normal_vector=Vector([1.0, 1.0, 1.0]), constant_term='1')
        p1 = Plane(normal_vector=Vector([0.0, 1.0, 0.0]), constant_term='2')
        p2 = Plane(normal_vector=Vector([1.0, 1.0, -1.0]), constant_term='3')
        p3 = Plane(normal_vector=Vector([1.0, 0.0, -2.0]), constant_term='2')

        s = LinearSystem([p0,p1,p2,p3])

        self.assertEqual(s.indices_of_first_nonzero_terms_in_each_row(), [0, 1, 0, 0], 'Index should match')
        self.assertEqual('{},{},{},{}'.format(s[0],s[1],s[2],s[3]),
                         'x_1 + x_2 + x_3 = 1,x_2 = 2,x_1 + x_2 - x_3 = 3,x_1 - 2x_3 = 2', 'Equations should be same')
        self.assertEqual(len(s), 4, 'Number of planes are not the same')
        # print s
        # s[0] = p1
        # print s

if __name__ == '__main__':
    unittest.main()