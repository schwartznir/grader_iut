import numpy as np

A2 = np.array([[1, 2, 2],
               [2, 1, 1],
               [1, 2, 1]])
A3p = np.random.rand(90, 90)
A3 = A3p*A3p + 0.0000001 * np.eye(90)
A4 = np.array([[1, 2],
               [2, 8]])
A5 = np.array([[2020]])

test_inv1 = [np.eye(2020), np.eye(2020)]
test_inv2 = [A2, np.linalg.inv(A2)]
test_inv3 = [A3, np.linalg.inv(A3)]
test_inv4 = [A4, np.linalg.inv(A4)]
test_inv5 = [A5, np.linalg.inv(A5)]

TESTS_INV = [
    test_inv1, test_inv2, test_inv3, test_inv4, test_inv5
]

e1 = np.zeros(2020)
e1[0] = 1
test1_gauss = [[np.eye(2020), e1], e1.transpose()]
vec2 = np.array([[1], [2], [4]])
A2inv = np.linalg.inv(A2)
test2_gauss = [[A2, vec2], A2inv.dot(vec2)]
vec3 = np.random.rand(90, 1)
A3inv = np.linalg.inv(A3)
test3_gauss = [[A3, vec3], A3inv.dot(vec3)]
A4inv = np.linalg.inv(A4)
vec4 = np.array([[3], [9]])
test4_gauss = [[A4, vec4], A4inv.dot(vec4)]
test5_gauss = [[A5, np.array([[1], [1], [1]])], np.array([[1/2020], [1/2020], [1/2020]])]

TESTS_GAUSS_FORM = [
    test1_gauss, test2_gauss, test3_gauss, test4_gauss, test5_gauss
]
