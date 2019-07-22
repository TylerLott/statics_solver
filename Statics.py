import numpy as np
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
    for i in list_of_Forces:
        if list_of_Forces[i].get_magnitude == 'find':
            continue
        else:
            sum_x += list_of_Forces[i].get_magnitude * list_of_Forces[i].find_x_comp
    return sum_x


def sum_forces_y(list_of_Forces):
    sum_y = 0
    for i in list_of_Forces:
        if list_of_Forces[i].get_magnitude == 'find':
            continue
        else:
            sum_y += list_of_Forces[i].get_magnitude * list_of_Forces[i].find_y_comp
    return sum_y


def sum_moments_at_point(x_point, y_point, list_of_Moments, list_of_Forces):
    sum_m = 0
    for i in list_of_Forces:
        if list_of_Forces[i].magnitude == 'find':
            continue
        else:
            if list_of_Forces[i].find_x_comp and list_of_Forces[i].find_y_comp != 0:
                sum_m += ((list_of_Forces.find_x_comp * list_of_Forces.get_magnitude)
                          * (list_of_Forces[i].get_x_location - x_point))
            elif list_of_Forces[i].find_x_comp == 0:
                sum_m += ((list_of_Forces.find_y_comp * list_of_Forces.get_magnitude)
                           * (list_of_Forces[i].get_y_location - y_point))
            elif list_of_Forces[i].find_y_comp == 0:
                sum_m += ((list_of_Forces.find_x_comp * list_of_Forces.get_magnitude)
                          * (list_of_Forces[i].get_x_location - x_point))
    for i in list_of_Moments:
        if list_of_Moments[i].get_magnitude == 'find':
            continue
        else:
            sum_m += list_of_Moments[i].find_mag_with_dir

    return sum_m


def forces_x(list_of_Forces):
    list_of_forces_x = []
    for i in list_of_Forces:
        if list_of_Forces[i].get_magnitude != 'find':
            list_of_forces_x.append(0)
            continue
        else:
            value = list_of_Forces[i].find_x_comp
            list_of_forces_x.append(value)
        list_of_forces_x.append(0)

    return list_of_forces_x


def forces_y(list_of_Forces):
    list_of_forces_y = []
    for i in list_of_Forces:
        list_of_forces_y.append(0)
        if list_of_Forces[i].get_magnitude != 'find':
            list_of_forces_y.append(0)
            continue
        else:
            value = list_of_Forces[i].find_y_comp
            list_of_forces_y.append(value)

    return list_of_forces_y


def moment_eq_at_point(x_location, y_location, list_of_Forces, list_of_Moments):
    list_of_moments = []
    for i in list_of_Forces:
        if list_of_Forces[i].get_x_location == x_location and list_of_Forces[i].get_y_location == y_location:
            list_of_moments.append(0)
            list_of_moments.append(0)
            continue
        elif list_of_Forces[i].get_magnitude != 'find':
            list_of_moments.append(0)
            list_of_moments.append(0)
            continue
        elif list_of_Forces[i].get_magnitude == 'find':
            if list_of_Forces[i].find_x_comp and list_of_Forces[i].find_y_comp != 0:
                value = list_of_Forces[i].find_x_comp * list_of_Forces[i].get_x_location
                list_of_moments.append(value)
                list_of_moments.append(0)
                continue
            elif list_of_Forces[i].find_x_comp == 0:
                value = list_of_Forces[i].find_y_comp * list_of_Forces[i].get_y_location
                list_of_moments.append(0)
                list_of_moments.append(value)
                continue
            elif list_of_Forces[i].find_y_comp == 0:
                value = list_of_Forces[i].find_x_comp * list_of_Forces[i].get_x_location
                list_of_moments.append(value)
                list_of_moments.append(0)
                continue
    for i in list_of_Moments:
        if list_of_Moments[i].get_magnitude != 'find':
            list_of_moments.append(0)
            continue
        elif list_of_Moments[i]:
            # assumes unknown moments are going counter-clockwise
            list_of_moments.append(1)
    return list_of_moments


def find_equations(list_of_Forces, list_of_Moments):
    a_matrix = np.array([forces_x(list_of_Forces)], [forces_y(list_of_Forces)])

    for i in list_of_Forces:
        new_moment_eq = moment_eq_at_point(list_of_Forces[i].get_x_location,
                                           list_of_Forces[i].get_y_location,
                                           list_of_Forces,
                                           list_of_Moments)
        np.append(a_matrix, new_moment_eq)
    return a_matrix

def find_b_matrix(list_of_Forces, list_of_Moments):
    


list_of_Forces = []
list_of_Moments = []

new_force = Force('down', 40, list_of_Forces, angle_from_axis=91, x_location=6)

new_force1 = Force('down', 34, list_of_Forces, angle_from_axis=45, x_location=5)

new_force2 = Force('down', 5, list_of_Forces, angle_from_axis=45, x_location=4)
# print(new_force.x_component)
# print(new_force.y_component)
# [print(object.x_component) for object in list_of_Forces]
# [print(object.x_location) for object in list_of_Forces]
#
# sm = sum_moments_at_point(0, 0, list_of_Moments, list_of_Forces)
# print(sm)

