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
##################################################
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
#########################################


def StepEuler(t, x, h, func):
    """ Fonction renvoyant l'approximation l'integrale de f à l'instant t+h"""
    return x + h * func(t, x)


def MyEuler(t0, x0, T, N, func):
    """ Fonction renvoyant l'approximation l'integrale de f dans un interval t0 - t0+T """
    x = np.zeros(N + 1, dtype='float')
    x[0] = x0  # On définit le x0 initial

    h = T / N
    time = np.linspace(t0, t0 + T, N + 1, dtype='float')  # On définit les intervalles

    # On calcule x(t) pour tout les t grace à StepEuler
    for idx in range(N):
        x[idx + 1] = StepEuler(time[idx], x[idx], h, func)

    return time, x


def func1(t, x):
    return np.cosh(x ** 2 * t) + 50 * np.tanh(t / (np.abs(x) + 1))


def func2(t, x):
    return np.exp(x+2*t)


def func3(t, x):
    return x ** t - t ** x


def func4(t, x):
    return t ** 2 - x ** 2


def func5(t, x):
    return np.ceil(t - x) - (t - x)


test_euler1 = [[0, 1, 0.01, 100, func1], MyEuler(0, 1, 1, 100, func1)]
test_euler2 = [[0.1, 0, 0.1, 10, func2], MyEuler(0.1, 0, 1, 10, func2)]
test_euler3 = [[1, 3, 0.001, 42, func3], MyEuler(1, 3, 0.001, 42, func3)]
test_euler4 = [[0, 0, 0.0001, 2000, func4], MyEuler(0, 0, 0.0001, 2000, func4)]
test_euler5 = [[1, 0, 1, 9310023, func5], MyEuler(1, 0, 1, 9310023, func5)]

TESTS_EULER = [test_euler1, test_euler2, test_euler3, test_euler4, test_euler5]

#####################################


def f(t, x):
    return np.sin(t**2)


def progtir(b):
    # Find numerical solution to the equation y''=fy simplified as two odes of order 1.
    # Iterations number and Cauchy conditions are hard coded
    y = np.zeros(1000001, dtype='float')  # y[t]
    z = np.zeros(1000001, dtype='float')  # y'[t]
    y[0] = 1  # y[0]
    z[0] = b  # y'[0]
    h = 5 / 1000000
    time = np.linspace(0, 5, 1000000, dtype='float')  # On définit les intervalles

    # On calcule y(t),y'(t) pour tout les t utilisons la système formé par y''=fy
    for idx in range(1000000):
        z[idx + 1] = z[idx] + h * f(time[idx], y[idx]) * y[idx]
        y[idx + 1] = y[idx] + h * z[idx]

    return y[1000000]


def methtir(eps):
    # A bisection method solution finding a value b for which progtir(b) = 0 on [-1,0] with error eps.
    # Iteration number and initial constants are hard coded.
    left_b = -1
    right_b = 0
    iteration = 0
    curr_val = 0

    while iteration < 100000:
        avg = (left_b + right_b) / 2
        curr_val = progtir(avg)
        if (left_b - right_b < eps) or curr_val == 0:
            break

        iteration += 1
        if curr_val * progtir(left_b) > 0:
            left_b = avg
        else:
            right_b = avg

    return curr_val


random_epsilons = np.random.rand(1, 15)
random_ints = np.random.randint(-20212021, 20212021, 15)
TESTS_PROGTIR = [[b, progtir(b)] for b in random_ints[0]]
TESTS_METHTIR = [[eps, methtir(eps)] for eps in random_epsilons[0]]
