import unittest
from lina.vector import Vector
from lina.line import Line


class LineTestCase(unittest.TestCase):

    def test_line_intersection1(self):
        line1 = Line(normal_vector=Vector([4.046, 2.836]), constant_term=1.21)
        line2 = Line(normal_vector=Vector([10.115, 7.09]), constant_term=3.025)
        self.assertEqual(line1.intersection_point(line2), Vector([0.0, 0.0]), "Both points should be equal")

    def test_line_intersection2(self):
        line1 = Line(Vector([7.204, 3.1882]), 8.68)
        line2 = Line(Vector([8.172, 4.114]), 9.883)
        self.assertEqual(line1.intersection_point(line2), Vector([1.1722591690709803, 0.07372340066892474]),
                         "Both points should be equal")

    def test_line_intersection3(self):
        line1 = Line(Vector([1.182, 5.562]), 6.744)
        line2 = Line(Vector([1.773, 8.343]), 9.525)
        self.assertIsNone(line1.intersection_point(line2), "There is no intersection between these two lines")

if __name__ == '__main__':
    unittest.main()
