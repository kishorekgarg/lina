from lina.lina.vector import Vector


def main():
    vector1 = Vector([8.218, -9.341])
    vector2 = Vector([-1.129, 2.111])
    print vector1 + vector2
    vector3 = Vector([7.119, 8.215])
    vector4 = Vector([-8.223, 0.878])
    print vector3 - vector4
    vector5 = Vector([1.671, -1.012, -0.318])
    vector5.scalar(7.41)
    print vector5
if __name__ == '__main__':
    main()
