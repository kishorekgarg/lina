import unittest
from lina.vector import Vector


class VectorTestCase(unittest.TestCase):
    # Add vectors
    def test_add_vectors(self):
        vector1 = Vector([8.218, -9.341])
        vector2 = Vector([-1.129, 2.111])
        self.assertEqual(vector1 + vector2, Vector([7.089, -7.229999999999999]), "Incorrect sum")

    # Subtraction
    def test_sub_vectors(self):
        vector1 = Vector([7.119, 8.215])
        vector2 = Vector([-8.223, 0.878])
        self.assertEqual(vector1 - vector2, Vector([15.342, 7.337]), "Incorrect subtraction")

    # Scalar
    def test_scalar(self):
        vector = Vector([1.671, -1.012, -0.318])
        vector.scalar(7.41)
        self.assertEqual(vector, Vector([1.671, -1.012, -0.318]), "Incorrect scalar")

    # Magnitude
    def test_magnitude(self):
        vector = Vector([-0.221, 7.437])
        self.assertAlmostEqual(vector.magnitude(), 7.44028292473, 5, "Incorrect magnitude")
        vector = Vector([8.813, -1.331, -6.247])
        self.assertAlmostEqual(vector.magnitude(), 10.8841875673, 5, "Incorrect magnitude")

    # Normalization
    def test_normalization(self):
        vector = Vector([5.581, -2.136])
        self.assertEqual(vector.normalized(), Vector([0.9339352140866403, -0.35744232526233]),
                         "Incorrect normalized vector")
        vector = Vector([1.996, 3.108, -4.554])
        self.assertEqual(vector.normalized(), Vector([0.3404012959433014, 0.5300437012984873, -0.7766470449528028]),
                         "Incorrect normalized vector")

    # Dot-product
    def test_dot_product(self):
        vector1 = Vector([7.887, 4.138])
        vector2 = Vector([-8.802, 6.776])
        self.assertAlmostEqual(vector1.dot_product(vector2), -41.382286, 5, "Incorrect dot product")
        vector1 = Vector([-5.955, -4.904, -1.874])
        vector2 = Vector([-4.496, -8.755, 7.103])
        self.assertAlmostEqual(vector1.dot_product(vector2), 56.397178, 5, "Incorrect dot product")

    # Angle in radian
    def test_angle_in_radian(self):
        vector1 = Vector([3.183, -7.627])
        vector2 = Vector([-2.668, 5.319])
        self.assertAlmostEqual(vector1.angle_in_radian(vector2), 3.07202289163, 5, "Incorrect angle in radian")

    # Angle in degree
    def test_angle_in_degree(self):
        vector1 = Vector([7.35, 0.221, 5.188])
        vector2 = Vector([2.751, 8.259, 3.985])
        self.assertAlmostEqual(vector1.angle_in_degree(vector2), 60.2758335058, 5, "Incorrect angle in degree")

    # Parallel and orthogonal vectors
    def test_parallel_and_orthogonal(self):
        vector1 = Vector([-7.579, -7.88])
        vector2 = Vector([22.737, 23.64])
        self.assertIs(vector1.is_parallel(vector2), True, "Vectors are parallel")
        self.assertIs(vector1.is_orthogonal(vector2), False, "Vectors are not orthogonal")
        vector1 = Vector([-2.029, 9.97, 4.172])
        vector2 = Vector([-9.231, -6.639, -7.245])
        self.assertIs(vector1.is_parallel(vector2), False, "Vectors are not parallel")
        self.assertIs(vector1.is_orthogonal(vector2), False, "Vectors are not orthogonal")
        vector1 = Vector([-2.328, -7.284, -1.214])
        vector2 = Vector([-1.821, 1.072, -2.94])
        self.assertIs(vector1.is_parallel(vector2), False, "Vectors are not parallel")
        self.assertIs(vector1.is_orthogonal(vector2), True, "Vectors are orthogonal")
        vector1 = Vector([2.118, 4.827])
        vector2 = Vector([0, 0])
        self.assertIs(vector1.is_parallel(vector2), True, "Vectors are parallel")
        self.assertIs(vector1.is_orthogonal(vector2), True, "Vectors are orthogonal")

    # Projection
    def test_projection(self):
        vector1 = Vector([3.039, 1.879])
        vector2 = Vector([0.825, 2.036])
        self.assertEqual(vector1.projection_parallel_component(vector2),
                         Vector([1.0826069624844668, 2.671742758325302]), "Incorrect projection parallel component")
        vector1 = Vector([-9.88, -3.264, -8.159])
        vector2 = Vector([-2.155, -9.353, -9.473])
        self.assertEqual(vector1.projection_orthogonal_component(vector2),
                         Vector([-8.350081043195763, 3.376061254287722, -1.4337460427811841]),
                         "Incorrect projection orthogonal component")
        vector1 = Vector([3.009, -6.172, 3.692, -2.51])
        vector2 = Vector([6.404, -9.144, 2.759, 8.718])
        self.assertEqual(vector1.projection_parallel_component(vector2),
                         Vector([1.9685161672140898, -2.8107607484393564, 0.8480849633578503, 2.679813233256158]),
                         "Incorrect projection parallel component")
        self.assertEqual(vector1.projection_orthogonal_component(vector2),
                         Vector([1.04048383278591, -3.3612392515606433, 2.8439150366421497, -5.189813233256158]),
                         "Incorrect projection orthogonal component")

    def test_cross_product(self):
        vector1 = Vector([8.462, 7.893, -8.187])
        vector2 = Vector([6.984, -5.975, 4.778])
        self.assertEqual(vector1.cross_product(vector2), Vector([-11.204570999999994, -97.609444, -105.68516199999999]),
                         "Incorrect cross product")

    def test_parallelogram_area(self):
        vector1 = Vector([-8.987, -9.838, 5.031])
        vector2 = Vector([-4.268, -1.861, -8.866])
        self.assertAlmostEqual(vector1.parallelogram_area(vector2), 142.122221402, 5, "Incorrect parallelogram area")

    def test_triangle_area(self):
        vector1 = Vector([1.5, 9.547, 3.691])
        vector2 = Vector([-6.007, 0.124, 5.772])
        self.assertAlmostEqual(vector1.triangle_area(vector2), 42.5649373994, 5, "Incorrect triangle area")

if __name__ == '__main__':
    unittest.main()
