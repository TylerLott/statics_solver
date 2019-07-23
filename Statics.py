import numpy as np
from numpy.linalg import inv
import math

SUPPORTS = 1
NUMBER_OF_FORCES = 1
NUMBER_OF_MOMENTS = 1


class Force:
    # direction = 'down' or 'up'
    # magnitude = float
    # angle from axis = angle in degrees from pos x, counter clockwise
    # x location is in units of length
    # list_of_Forces = list
    def __init__(self, direction, magnitude, list_of_Forces, angle_from_axis=0, x_location=0, y_location=0):
        self.direction = direction
        self.magnitude = magnitude
        self.angle_from_axis = angle_from_axis
        self.x_location = x_location
        self.y_location = y_location
        self.list_of_Forces = list_of_Forces

        self.get_direction_sign()
        self.create_new_force_x()

    def get_x_location(self):
        return self.x_location

    def get_y_location(self):
        return self.y_location

    def get_magnitude(self):
        return self.magnitude

    def get_direction_sign(self):
        if self.direction == 'down':
            self.direction = -1
        else:
            self.direction = 1

    def create_new_force_x(self):
        self.list_of_Forces = self.list_of_Forces.append(self)
        return self.list_of_Forces

    def find_x_comp(self):
        x_comp = -1 * np.cos(math.radians(self.angle_from_axis))
        return x_comp

    def find_y_comp(self):
        y_comp = self.direction * np.sin(math.radians(self.angle_from_axis))
        return y_comp


# this is only for reactionary  or applied moments
class Moment:
    # + is counter-clockwise, - is clockwise
    def __init__(self, direction, magnitude):
        self.direction = direction
        self.magnitude = magnitude

        self.find_mag_with_dir()

    def get_magnitude(self):
        return self.magnitude

    def find_mag_with_dir(self):
        if self.direction == '-':
            self.magnitude = -1 * self.magnitude
        return self.magnitude


class Force_Area:
    def __init__(self, direction, magnitude_equation, x_left, x_right):
        self.direction = direction
        self.magnitude_equation = magnitude_equation
        self.x_left = x_left
        self.x_right = x_right


class Pin_Connection:
    # reaction_x and reaction_y should be objects of Force
    def __init__(self, reaction_x, reaction_y, x_point, y_point):
        self.reaction_x = reaction_x
        self.reaction_y = reaction_y
        self.x_point = x_point
        self.y_point = y_point


class Roller_Connection:
    # reaction_y should be object of Force
    def __init__(self, reaction_y, x_point, y_point):
        self.reaction_y = reaction_y
        self.x_point = x_point
        self.y_point = y_point


class Fixed_Connection:
    # reaction_x and reaction_y should be objects of Force
    # reaction_moment should be objects of Moment
    def __init__(self, reaction_x, reaction_y, reaction_moment, x_point, y_point):
        self.reaction_x = reaction_x
        self.reaction_y = reaction_y
        self.reaction_moment = reaction_moment
        self.x_point = x_point
        self.y_point = y_point


def sum_forces_x(list_of_Forces):
    sum_x = 0
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() == 'find':
            continue
        else:
            sum_x += list_of_Forces[i].get_magnitude() * list_of_Forces[i].find_x_comp()
    return -sum_x


def sum_forces_y(list_of_Forces):
    sum_y = 0
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() == 'find':
            continue
        else:
            sum_y += list_of_Forces[i].get_magnitude() * list_of_Forces[i].find_y_comp()
    return -sum_y


def sum_moments_at_point(x_point, y_point, list_of_Forces, list_of_Moments):
    sum_m = 0
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() == 'find':
            continue
        else:
            if list_of_Forces[i].find_x_comp() >= .001 and list_of_Forces[i].find_y_comp() >= .001:
                sum_m += ((list_of_Forces[i].find_x_comp() * list_of_Forces[i].get_magnitude())
                          * (list_of_Forces[i].get_x_location() - x_point))
            elif list_of_Forces[i].find_x_comp() <= .001:
                sum_m += ((list_of_Forces[i].find_y_comp() * list_of_Forces[i].get_magnitude())
                          * (list_of_Forces[i].get_x_location() - x_point))
            elif list_of_Forces[i].find_y_comp() <= .001:
                sum_m += ((list_of_Forces[i].find_x_comp() * list_of_Forces[i].get_magnitude())
                          * (list_of_Forces[i].get_y_location() - y_point))
    for i in range(len(list_of_Moments)):
        if list_of_Moments[i].get_magnitude() == 'find':
            continue
        else:
            sum_m += list_of_Moments[i].find_mag_with_dir()

    return -sum_m


def forces_x(list_of_Forces):
    list_of_forces_x = []
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() != 'find':
            list_of_forces_x.append(0)
        else:
            value = list_of_Forces[i].find_x_comp()
            list_of_forces_x.append(value)

    return list_of_forces_x


def forces_y(list_of_Forces):
    list_of_forces_y = []
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() != 'find':
            list_of_forces_y.append(0)
            continue
        else:
            value = list_of_Forces[i].find_y_comp()
            list_of_forces_y.append(value)

    return list_of_forces_y


def moment_eq_at_point(x_location, y_location, list_of_Forces, list_of_Moments):
    list_of_moments = []
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_x_location() == x_location and list_of_Forces[i].get_y_location() == y_location:
            list_of_moments.append(0)
            continue
        elif list_of_Forces[i].get_magnitude() != 'find':
            list_of_moments.append(0)
            continue
        elif list_of_Forces[i].get_magnitude() == 'find':
            if list_of_Forces[i].find_x_comp() <= .001 and list_of_Forces[i].find_y_comp() <= 0.001:
                value = list_of_Forces[i].find_x_comp() * (list_of_Forces[i].get_y_location() - y_location)
                list_of_moments.append(value)
                continue
            elif list_of_Forces[i].find_x_comp() <= 0.001:
                value = list_of_Forces[i].find_y_comp() * (list_of_Forces[i].get_x_location() - x_location)
                list_of_moments.append(value)
                continue
            elif list_of_Forces[i].find_y_comp() <= 0.001:
                value = list_of_Forces[i].find_x_comp() * (list_of_Forces[i].get_y_location() - y_location)
                list_of_moments.append(value)
                continue
    for i in range(len(list_of_Moments)):
        if list_of_Moments[i].get_magnitude() != 'find':
            list_of_moments.append(0)
            continue
        elif list_of_Moments[i]:
            # assumes unknown moments are going counter-clockwise
            list_of_moments.append(1)
    return list_of_moments


def find_a_matrix(list_of_Forces, list_of_Moments):
    a_matrix = [forces_x(list_of_Forces), forces_y(list_of_Forces)]

    for i in range(len(list_of_Forces)):
        new_moment_eq = moment_eq_at_point(list_of_Forces[i].get_x_location(),
                                           list_of_Forces[i].get_y_location(),
                                           list_of_Forces,
                                           list_of_Moments)
        a_matrix.append(new_moment_eq)


    return a_matrix


def find_b_matrix(list_of_Forces, list_of_Moments):
    b_matrix = [[sum_forces_x(list_of_Forces)], [sum_forces_y(list_of_Forces)]]

    moment_locations = []

    for i in range(len(list_of_Forces)):
        new_moment_sum = [sum_moments_at_point(list_of_Forces[i].get_x_location(),
                                               list_of_Forces[i].get_y_location(),
                                               list_of_Forces,
                                               list_of_Moments)]
        current_location = (list_of_Forces[i].get_x_location(), list_of_Forces[i].get_y_location())

        b_matrix.append(new_moment_sum)
        moment_locations.append((list_of_Forces[i].get_x_location(), list_of_Forces[i].get_y_location()))

    return b_matrix


def solve(a_matrix, b_matrix):

    # creates a new matrix with out any zero equations
    index = []
    new_a_matrix = []
    for i in range(len(a_matrix)):
        for ii in range(len(a_matrix[i])):
            # print(a_matrix[i][ii])
            if abs(a_matrix[i][ii]) > .001:
                index.append(i)
                new_a_matrix.append(a_matrix[i])
                break

    # creates new b matrix to match a matrix
    new_b_matrix = []
    for i in index:
        new_b_matrix.append(b_matrix[i])

    # creates an equation with no repeat equations
    index_2 = []
    new_a_matrix_2 = []
    for i in range(len(new_a_matrix)):
        if new_a_matrix[i] not in new_a_matrix_2:
            index_2.append(i)
            new_a_matrix_2.append(new_a_matrix[i])

    # creates new b matrix to match a matrix again
    new_b_matrix_2 = []
    for i in index_2:
        new_b_matrix_2.append(new_b_matrix[i])


    empty_columns = []
    for i in range(len(new_a_matrix_2)):
        counter = 0
        for ii in range(len(new_a_matrix_2[i])):
            if new_a_matrix_2[ii][i] in new_a_matrix_2[:][i]:
                counter += 1
                if counter == len(new_a_matrix_2[i]):
                    empty_columns.append(i)

    print(empty_columns)
    for i in sorted(empty_columns, reverse=True):
        for ii in range(len(new_a_matrix_2)):
            for iii in range(len(new_a_matrix_2[ii])):
                print(i)
                new_a_matrix_2[ii].pop(i)
                break

    for i in sorted(empty_columns, reverse=True):
        new_b_matrix_2.pop(i)
        new_a_matrix_2.pop(i)



    list_of_answers = np.matmul(inv(new_a_matrix_2), new_b_matrix_2)
    return list_of_answers

list_of_Forces = []
list_of_Moments = []

new_force = Force('down', 100, list_of_Forces, angle_from_axis=90, x_location=1)

new_force1 = Force('up', 90, list_of_Forces, angle_from_axis=90, x_location=2)

new_force4 = Force('down', 40, list_of_Forces, angle_from_axis=90, x_location=.5)

new_force2 = Force('up', 'find', list_of_Forces, angle_from_axis=90, x_location=0)

new_force3 = Force('up', 'find', list_of_Forces, angle_from_axis=90, x_location=2)
# print(new_force.x_component)
# print(new_force.y_component)
# [print(object.x_component) for object in list_of_Forces]
# [print(object.x_location) for object in list_of_Forces]
#
# sm = sum_moments_at_point(0, 0, list_of_Moments, list_of_Forces)
# print(sm)
# print(sum_moments_at_point(list_of_Forces[1].get_x_location(), list_of_Forces[1].get_y_location, list_of_Forces, list_of_Moments))
# print(list_of_Forces[2].get_x_location())



# print(sum_forces_y(list_of_Forces))
# print(sum_forces_x(list_of_Forces))
#
b = find_b_matrix(list_of_Forces, list_of_Moments)
a = find_a_matrix(list_of_Forces, list_of_Moments)

print(solve(a,b))
#print(a)
# print(b)

'''
b_matrix

x forces
y forces
moments about 1
moments about 2
moments about 0
moments about 2
'''

'''
a_matrix

[f0] [f1] [f2] [f3] [sum in x or y or moment]
'''

# print(forces_x(list_of_Forces))
# print(forces_y(list_of_Forces))
# print(moment_eq_at_point(list_of_Forces[2].get_x_location(), list_of_Forces[2].get_y_location(), list_of_Forces, list_of_Moments))

#
# print(moment_eq_at_point(list_of_Forces[1].get_x_location(),
#                                            list_of_Forces[1].get_y_location(),
#                                            list_of_Forces,
#                                            list_of_Moments))




