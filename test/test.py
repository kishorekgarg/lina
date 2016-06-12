from lina.lina.vector import Vector


def main():
    # Add vectors
    vector1 = Vector([8.218, -9.341])
    vector2 = Vector([-1.129, 2.111])
    print vector1 + vector2

    # Subtraction
    vector3 = Vector([7.119, 8.215])
    vector4 = Vector([-8.223, 0.878])
    print vector3 - vector4

    # Scalar
    vector5 = Vector([1.671, -1.012, -0.318])
    vector5.scalar(7.41)
    print vector5

    # Magnitude
    vector6 = Vector([-0.221, 7.437])
    print vector6.magnitude()
    vector7 = Vector([8.813, -1.331, -6.247])
    print vector7.magnitude()

    # Normalization
    vector8 = Vector([5.581, -2.136])
    print vector8.normalized()
    vector9 = Vector([1.996, 3.108, -4.554])
    print vector9.normalized()

    # Dot-product
    vector10 = Vector([7.887, 4.138])
    vector11 = Vector([-8.802, 6.776])
    print vector10.dot_product(vector11)

    vector12 = Vector([-5.955, -4.904, -1.874])
    vector13 = Vector([-4.496, -8.755, 7.103])
    print vector12.dot_product(vector13)

    # Angle in radian
    vector14 = Vector([3.183, -7.627])
    vector15 = Vector([-2.668, 5.319])
    print vector14.get_angle_in_radian(vector15)

    # Angle in degree
    vector16 = Vector([7.35, 0.221, 5.188])
    vector17 = Vector([2.751, 8.259, 3.985])
    print vector16.get_angle_in_degree(vector17)

if __name__ == '__main__':
    main()
