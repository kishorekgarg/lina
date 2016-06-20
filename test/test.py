from lina.vector import Vector


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
    print vector14.angle_in_radian(vector15)

    # Angle in degree
    vector16 = Vector([7.35, 0.221, 5.188])
    vector17 = Vector([2.751, 8.259, 3.985])
    print vector16.angle_in_degree(vector17)

    # Parallel and orthogonal vectors
    vector18 = Vector([-7.579, -7.88])
    vector19 = Vector([22.737, 23.64])
    print vector18.is_parallel(vector19)
    print vector18.is_orthogonal(vector19)

    vector20 = Vector([-2.029, 9.97, 4.172])
    vector21 = Vector([-9.231, -6.639, -7.245])
    print vector20.is_parallel(vector21)
    print vector20.is_orthogonal(vector21)

    vector22 = Vector([-2.328, -7.284, -1.214])
    vector23 = Vector([-1.821, 1.072, -2.94])
    print vector22.is_parallel(vector23)
    print vector22.is_orthogonal(vector23)

    vector24 = Vector([2.118, 4.827])
    vector25 = Vector([0, 0])
    print vector24.is_parallel(vector25)
    print vector24.is_orthogonal(vector25)

    # Projection
    vector26 = Vector([3.039, 1.879])
    vector27 = Vector([0.825, 2.036])
    print vector26.projection_parallel_component(vector27)

    vector28 = Vector([-9.88, -3.264, -8.159])
    vector29 = Vector([-2.155, -9.353, -9.473])
    print vector28.projection_orthogonal_component(vector29)

    vector30 = Vector([3.009, -6.172, 3.692, -2.51])
    vector31 = Vector([6.404, -9.144, 2.759, 8.718])
    print vector30.projection_parallel_component(vector31)
    print vector30.projection_orthogonal_component(vector31)

    vector32 = Vector([8.462, 7.893, -8.187])
    vector33 = Vector([6.984, -5.975, 4.778])
    print vector32.cross_product(vector33)

    vector34 = Vector([-8.987, -9.838, 5.031])
    vector35 = Vector([-4.268, -1.861, -8.866])
    print vector34.parallelogram_area(vector35)

    vector36 = Vector([1.5, 9.547, 3.691])
    vector37 = Vector([-6.007, 0.124, 5.772])
    print vector36.triangle_area(vector37)
if __name__ == '__main__':
    main()
