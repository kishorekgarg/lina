import unittest
from lina.vector import Vector
from lina.plane import Plane


class PlaneTestCase(unittest.TestCase):

    def test_is_parallel1(self):
        plane1 = Plane(normal_vector=Vector([-0.412, 3.806, 0.728]), constant_term=-3.46)
        plane2 = Plane(normal_vector=Vector([1.03, -9.515, -1.82]), constant_term=8.65)
        self.assertEqual(plane1.is_parallel(plane2), True, "Planes are parallel")
        self.assertEqual(plane1 == plane2, True, "Planes are equal")

    def test_is_parallel2(self):
        plane1 = Plane(Vector([2.611, 5.528, 0.283]), 4.6)
        plane2 = Plane(Vector([7.715, 8.306, 5.342]), 3.76)
        self.assertEqual(plane1.is_parallel(plane2), False, "Planes are not parallel")
        self.assertEqual(plane1 == plane2, False, "Planes are not equal")

    def test_is_parallel3(self):
        plane1 = Plane(Vector([-7.926, 8.625, -7.212]), -7.95)
        plane2 = Plane(Vector([-2.642, 2.875, -2.404]), 2.44)
        self.assertEqual(plane1.is_parallel(plane2), True, "Planes are not parallel")
        self.assertEqual(plane1 == plane2, False, "Planes are not equal")


if __name__ == '__main__':
    unittest.main()
